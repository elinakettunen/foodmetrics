import pandas as pd
import re
from pathlib import Path

FOOD_PROP_DTYPES = {
    'animal_proportion': 'Float32',
    'fao_subgroup_code': 'Int64',
    'has_fish': 'boolean',
    'has_meat_or_poultry': 'boolean',
    'has_seafood': 'boolean',
}
DB_FNAME = 'food_properties.csv'
UPDATE_FNAME = 'food_properties_new_codes.csv'

def read(file_name):
    return pd.read_csv(file_name,index_col='code', dtype=FOOD_PROP_DTYPES)

def add_codes_from_local_file():
    new = read(UPDATE_FNAME)
    if new.isna().any().any():
        raise Exception('Enter all values in food_properties_new_codes.csv before merging.')
    
    db = read(DB_FNAME)
    if not db.columns.equals(new.columns):
        raise Exception('Ensure food_properties_new_codes.csv has the same columns as the database.')

    combined = db.combine_first(new).sort_index()

    combined.to_csv(DB_FNAME)
    return combined.index.difference(db.index)

def update_from_google_sheet():
    url = input('Paste in the URL of your google sheet. Enter to skip:\n')

    if url:
        try:
            sheet_id = re.search(r'/d/([a-zA-Z0-9-_]+)', url).group(1)
            gid = re.search(r'[#&]gid=([0-9]+)', url)
            gid = gid.group(1) if gid else '0'

            csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
            gsheet_df = pd.read_csv(
                csv_url,
                index_col='code'
            )
            db = read(DB_FNAME)
            combined = db.combine_first(gsheet_df)

            br, bc = db.shape
            ar, ac = combined.shape
            combined.to_csv(DB_FNAME)
            print(f'Added {ar - br} rows and {ac - bc} columns.')
        except Exception as e:
            print(f'Could read {url} as a csv.',e)
    else:
        print('Skipped.')

if __name__ == "__main__":
    try:
        if Path(UPDATE_FNAME).exists():
            idx_diff = update_db()
            l = len(idx_diff)
            print(f'Added {l} new codes to database.')
            if l < 10:
                for c in idx_diff: print(c)

        update_from_google_sheet()

    except Exception as e:
        print(str(e))