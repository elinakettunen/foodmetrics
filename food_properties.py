import pandas as pd

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

def update_db():
    new = read(UPDATE_FNAME)
    if new.isna().any().any():
        raise Exception('Enter all values in food_properties_new_codes.csv before merging.')

    db = read(DB_FNAME)
    if not db.columns.equals(new.columns):
        raise Exception('Ensure food_properties_new_codes.csv has the same columns as the database.')

    combined = db.combine_first(new).sort_index()
    combined.to_csv(DB_FNAME)
    return combined.index.difference(db.index)

if __name__ == "__main__":
    try:
        idx_diff = update_db()
        l = len(idx_diff)
        print(f'Added {l} new codes to database.')
        if l < 10:
            for c in idx_diff: print(c)

    except Exception as e:
        print(str(e))