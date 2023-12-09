import pandas as pd

# this is a method to save all the invalid results, so that we can pair input/output data later.

CSVNAME = "splitted_data_list_modified.csv"
OUTPUT_FILE = "invalid_result.csv"

def save_invalid_entries(csv_file_path, output_file_path):
    # Load data from the given CSV file path into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Filter rows where the 'valid' column is False
    invalid_rows = df[df['valid'] == False]

    # Save these invalid rows to the specified output CSV file
    invalid_rows.to_csv(output_file_path, index=False)

save_invalid_entries(CSVNAME, OUTPUT_FILE)

