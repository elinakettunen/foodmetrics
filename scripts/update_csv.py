import pandas as pd
import re
from pathlib import Path

from foodmetrics import FOOD_PROP_DTYPES

UPDATE_FILE_PATH = '../food_properties_new_codes.csv'
DB_FILE_NAME = "../food_properties.csv"

def add_codes_from_local_file():
    new = read(UPDATE_FILE_PATH)
    if new.isna().any().any():
        raise Exception('Enter all values in food_properties_new_codes.csv before merging.')
    
    db = read(DB_FILE_NAME)
    if not db.columns.equals(new.columns):
        raise Exception('Ensure food_properties_new_codes.csv has the same columns as the database.')

    combined = db.combine_first(new).sort_index()

    combined.to_csv(DB_FILE_NAME)
    return combined.index.difference(db.index)

def update_from_google_sheet():
    url = input('Paste in the URL of your google sheet. Enter to skip:\n')

    if url:
        sheet_id = re.search(r'/d/([a-zA-Z0-9-_]+)', url).group(1)
        gid = re.search(r'[#&]gid=([0-9]+)', url)
        gid = gid.group(1) if gid else '0'

        csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
        columns = list(FOOD_PROP_DTYPES.keys() - {'code'})
        gsheet_df = pd.read_csv(
            csv_url,
            index_col='code',
            dtype=FOOD_PROP_DTYPES,
            na_values=['', ' ', '  ', '\t']
        )[columns]
        db = pd.read_csv(
            DB_FILE_NAME,
            index_col='code',
            dtype=FOOD_PROP_DTYPES
        )

        combined = db.copy()
        combined.update(gsheet_df)
        
        common_columns = db.columns.intersection(gsheet_df.columns)
        filled_mask = db[common_columns].isna() & combined[common_columns].notna()
        overwritten_mask = db[common_columns].notna() & combined[common_columns].notna() & (db[common_columns] != combined[common_columns])

        num_filled = filled_mask.sum().sum()
        num_overwritten = overwritten_mask.sum().sum()
        
        new_columns = [col for col in gsheet_df.columns if col not in db.columns]
        for col in new_columns:
            combined[col] = gsheet_df[col]
        
        num_new_col_values = sum(gsheet_df[col].notna().sum() for col in new_columns)
        num_filled += num_new_col_values

        br, bc = db.shape
        ar, ac = combined.shape
        
        combined.to_csv(DB_FILE_NAME)

        print(f'Filled in {num_filled} missing and changed {num_overwritten} values.')
        print(f'Added {ar - br} rows and {ac - bc} columns.')
    else:
        print('Skipped.')

if __name__ == "__main__":
    try:
        if Path(UPDATE_FILE_PATH).exists():
            idx_diff = update_db()
            l = len(idx_diff)
            print(f'Added {l} new codes to database.')
            if l < 10:
                for c in idx_diff: print(c)

        update_from_google_sheet()

    except Exception as e:
        print(str(e))