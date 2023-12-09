import pandas as pd

# after surveying of the predicted labels, this is the first step I do for cleaning up the data set

POSSIBLE_SET = {"Music"}

def set_validity(df, S):
    # Initialize all rows in DataFrame as valid
    df['valid'] = True

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        label_entry = row['Label']

        # Continue to next iteration if label entry is not a string or is NaN
        if not isinstance(label_entry, str) or pd.isna(label_entry):
            continue

        # Split the label entry into individual labels
        labels = label_entry.split('; ')
        for label in labels:
            label_name, label_prob = label.split(': ')
            label_prob = float(label_prob)

            # Mark row as invalid if label probability is greater than 0.7 and not in set S
            # (exclud 'Music'; this task has its reason according to a little survey)
            if label_prob > 0.7 and label_name not in S:
                df.at[index, 'valid'] = False
                break

    return df

df = pd.read_csv('splitted_data_list.csv')

df = set_validity(df, POSSIBLE_SET)
df.to_csv('splitted_data_list_modified.csv', index=False)

