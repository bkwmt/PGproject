import pandas as pd

# this file update the value of 'valid' column of target_csv, according to source_csv.
# this must be done each time while there's a result in different stages
  
source_csv = 'modified_unpaired_result.csv'
target_csv = 'splitted_data_list_modified.csv'

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error while reading CSV file: {e}")
        return None

def update_validity_based_on_filenames(source_csv, target_csv):
    # Load data from source and target CSV files
    source_df = load_data(source_csv)
    target_df = load_data(target_csv)

    # Check if either DataFrame failed to load
    if source_df is None or target_df is None:
        return

    # Create a set of filenames from the source DataFrame
    source_filenames = set(source_df['Filename'].tolist())

    # Update the 'valid' column in the target DataFrame based on source filenames
    target_df['valid'] = target_df.apply(lambda row: False if row['Filename'] in source_filenames else row['valid'], axis=1)

    target_df.to_csv(target_csv, index=False)

update_validity_based_on_filenames(source_csv, target_csv)
