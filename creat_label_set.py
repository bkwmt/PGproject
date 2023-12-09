import pandas as pd

# This code creats/prints SET built with labels, which can be used for other methods for clean up
# It would be better to make another label_SET, which may contain labels that should not be clean up,
#       for example: 'Music', 'Guitar', ...etc.
#       However, I do it manually.

THRESHOLD = 0.1
CSVNAME = "label_distribution9.csv"

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error while reading CSV file: {e}")
        return None


def create_set_from_column_index(df, column_index=0):
    # Initialize an empty set for labels
    label_set = set()
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the specified column index is valid and 'max' value meets the threshold
        if column_index < len(row) and not pd.isna(row[column_index]) and row['max'] >= THRESHOLD:
            # Add the value from the specified column to the label set
            label_set.add(row[column_index])
    return label_set


rawdatafile = load_data(CSVNAME)
result_set = create_set_from_column_index(rawdatafile)
print(result_set)