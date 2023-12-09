import pandas as pd
import matplotlib.pyplot as plt
import json

CSVNAME = "splitted_data_list.csv"
# Define a lower threshold constant for calculate_label_statistics()
THRESHOLD_LOW = 0.0

# Define a higher threshold constant for identify_extreme_cases()
THRESHOLD_HIGH = 0.5

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error while reading CSV file: {e}")
        return None
    
def save_to_csv(df, filename, index=True):
    df = pd.DataFrame.from_dict(df, orient='index')
    df.to_csv(str(filename)+'.csv', index=index)

def save_to_json(data, filename, indent_num=4):
    with open(str(filename)+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent_num)

def filter_valid_rows(df):
    # Check if 'valid' column exists in the DataFrame
    if 'valid' in df.columns:
        # Return rows where 'valid' column is True
        return df[df['valid']]
    else:
        # If 'valid' column does not exist, return the original DataFrame
        return df

def calculate_label_statistics(df, min_prob=0.01):
    # Initialize a dictionary to store label data
    label_data = {}

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

            # Process the label if its probability is greater than or equal to min_prob
            if label_prob >= min_prob:
                if label_name not in label_data:
                    # Initialize label data for new label
                    label_data[label_name] = {'probs': [], 'max': label_prob, 'min': label_prob}
                # Update label data with current label's probability
                label_data[label_name]['probs'].append(label_prob)
                label_data[label_name]['max'] = max(label_data[label_name]['max'], label_prob)
                label_data[label_name]['min'] = min(label_data[label_name]['min'], label_prob)

    # Calculate statistics for each label
    label_stats = {
        label: {
            "count": len(info['probs']),  # Total count of label appearance
            "max": info['max'],           # Maximum probability of label
            "min": info['min']            # Minimum probability of label
        } for label, info in label_data.items()
    }

    return label_stats



def visualize_label_distribution(label_stats, save_path):
    # Extract label names and their counts, and sort them by count in ascending order
    items = [(label, stats['count']) for label, stats in label_stats.items()]
    sorted_items = sorted(items, key=lambda x: x[1], reverse=False)
    labels, counts = zip(*sorted_items)

    # Create a figure with specific size and resolution
    plt.figure(figsize=(12, 60), dpi=300)

    # Create horizontal bar chart with khaki color bars
    bars = plt.barh(labels, counts, color='khaki')

    # Set labels for x and y axes and adjust font size for y-ticks
    plt.xlabel('Count')
    plt.ylabel('Label')
    plt.yticks(fontsize=8)

    # Add text labels on each bar showing the count
    for bar in bars:
        xval = bar.get_width()
        plt.text(xval, bar.get_y() + bar.get_height()/2, round(xval, 2), va='center', ha='left', fontsize=8)

    # Set the title of the chart and adjust layout for tight packing
    plt.title('Label Distribution')
    plt.tight_layout()

    # Save the figure to the provided path and close the plot
    plt.savefig(save_path)
    plt.close()


def analyze_label_not_main(df, main_category='Music'):
    # Initialize a dictionary to store count of non-main category labels
    diversity_data = {}

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        label_entry = row['Label']

        # Skip the iteration if label entry is not a string or is NaN
        if not isinstance(label_entry, str) or pd.isna(label_entry):
            continue

        # Split the label entry into individual labels
        labels = label_entry.split('; ')
        for label in labels:
            label_name, _ = label.split(': ')
            # Increment the count of label if it is not the main category
            if label_name != main_category:
                if label_name in diversity_data:
                    diversity_data[label_name] += 1
                else:
                    diversity_data[label_name] = 1

    # Return the dictionary containing counts of non-main category labels
    return diversity_data

def identify_extreme_cases(df, threshold=0.5):
    # Initialize a list to store extreme cases
    extreme_cases = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        label_entry = row['Label']

        # Skip the iteration if label entry is not a string or is NaN
        if not isinstance(label_entry, str) or pd.isna(label_entry):
            continue

        # Split the label entry into individual labels
        labels = label_entry.split('; ')
        for label in labels:
            label_name, label_prob = label.split(': ')
            label_prob = float(label_prob)

            # Add the label to extreme cases if its probability is greater than or equal to the threshold
            if label_prob >= threshold:
                extreme_cases.append((index, label_name, label_prob))

    # Return the list of extreme cases
    return extreme_cases


def extract_file_info(file_path):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Initialize a dictionary to store file information
    file_info_dict = {}

    # Iterate over each filename in the DataFrame
    for filename in df['Filename']:
        # Extract the first 24 characters as the UUID identifier
        identifier = filename[:24]

        # Determine whether the file is an 'input' or 'output' based on the filename
        in_or_out = 'input' if 'input' in filename else 'output'

        # Extract the split index from the filename
        split_index = filename.split('_')[-1].split('.')[0]

        # Store the extracted information in the dictionary
        file_info_dict[filename] = {
            'identifier': identifier,
            'type': in_or_out,
            'split_index': int(split_index)
        }

    # Return the dictionary containing file information
    return file_info_dict



rawdatafile = load_data(CSVNAME)
datafile = filter_valid_rows(rawdatafile)

labels_dict = calculate_label_statistics(datafile, THRESHOLD_LOW)
# identifier = extract_file_info(CSVNAME)
# visualize_label_distribution(labels_dict, "9_label_distribution.png")
diversity_dict = analyze_label_not_main(datafile)
# extreme_case_list = identify_extreme_cases(datafile, THRESHOLD_HIGH)
# save_to_json(diversity_dict, "9_not_music")
# save_to_json(extreme_case_list, "3_extreme")
save_to_csv(labels_dict, "label_distribution11")
# save_to_json(identifier, "identifier")

