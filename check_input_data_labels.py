import pandas as pd

#check "INPUT" data only, for it's supposed to be "clean tone".

CSVNAME = "splitted_data_list_modified.csv"
RESULT_CSV = "result_input_distortion.csv"
TOP_N = 3
CHECK_LABEL = {"Distortion"}

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error while reading CSV file: {e}")
        return None

def filter_valid_rows(df):
    # Filter and return rows where 'valid' column is True, if 'valid' column exists
    if 'valid' in df.columns:
        return df[df['valid']]
    else:
        # Return the original DataFrame if 'valid' column does not exist
        return df

def filter_input_files(df):
    # Filter and return rows where the 'Filename' column contains 'input'
    return df[df['Filename'].str.contains('input')]

def extract_labels(df, n=1):
    # Extract the top 'n' labels from each row in the 'Label' column of the DataFrame
    return [
        row['Label'].split('; ')[:n]
        for index, row in df.iterrows()
        if isinstance(row['Label'], str) and not pd.isna(row['Label'])
    ]

def save_labels(df, n, S, exist=True):
    # Extract valid labels and filter rows based on the existence of labels in set 'S'
    valid_labels = extract_labels(df, n)
    if exist:
        valid_rows = df.iloc[[i for i, labels in enumerate(valid_labels) if any(label.split(': ')[0] in S for label in labels)]]
    else:
        valid_rows = df.iloc[[i for i, labels in enumerate(valid_labels) if not any(label.split(': ')[0] in S for label in labels)]]

    # Save the filtered rows to a CSV file
    valid_rows.to_csv(RESULT_CSV, index=False)



rawdatafile = load_data(CSVNAME)
datafile = filter_valid_rows(rawdatafile)
input_datafile = filter_input_files(datafile)
save_labels(input_datafile, TOP_N, S=CHECK_LABEL, exist=True)
