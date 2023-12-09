import pandas as pd

def save_modified_unpaired_entries(csv_file_path, output_file_path):
    # Load data from the given CSV file path into a DataFrame
    df = pd.read_csv(csv_file_path)
    # Initialize an empty DataFrame for modified unpaired rows
    modified_unpaired_rows = pd.DataFrame()

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        identifier = row['identifier']
        split_index = row['split_index']
        # Determine the opposite type (input/output) for the current row
        opposite_type = 'input' if 'output' in row['Filename'] else 'output'

        # Filter out paired data by checking for the opposite file type, identifier, and split index
        pair_row = df[(df['Filename'].str.contains(opposite_type)) & (df['identifier'] == identifier) & (df['split_index'] == split_index)]

        # Modify and add unpaired data to the new DataFrame
        if pair_row.empty:
            modified_row = row.copy()
            # Switch 'input' with 'output' in the filename and set 'valid' to True
            modified_row['Filename'] = modified_row['Filename'].replace('input', 'XXX').replace('output', 'input').replace('XXX', 'output')
            modified_row['valid'] = True
            modified_unpaired_rows = pd.concat([modified_unpaired_rows, modified_row.to_frame().T])

    # Save the modified unpaired rows to the specified output CSV file
    modified_unpaired_rows.to_csv(output_file_path, index=False)


csv_file_path = 'invalid_result.csv'
output_file_path = 'modified_unpaired_result.csv'

save_modified_unpaired_entries(csv_file_path, output_file_path)
