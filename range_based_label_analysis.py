import pandas as pd
import json
from tqdm import tqdm

def filter_and_analyze_labels(df, min_prob, max_prob):
    # Initialize a dictionary to store label statistics
    label_stats = {}

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

            # Filter and update statistics for labels within the probability range
            if min_prob <= label_prob <= max_prob:
                if label_name not in label_stats:
                    label_stats[label_name] = {'count': 0, 'max_prob': label_prob, 'min_prob': label_prob}
                label_stats[label_name]['count'] += 1
                label_stats[label_name]['max_prob'] = max(label_stats[label_name]['max_prob'], label_prob)
                label_stats[label_name]['min_prob'] = min(label_stats[label_name]['min_prob'], label_prob)

    return label_stats

# Load data from CSV
df = pd.read_csv('splitted_data_list.csv')

all_results = {}
min_prob = 0.4
max_prob = 1.0

# Loop through different probability ranges
for p in tqdm(range(int((max_prob - min_prob) / 0.05))):
    current_max_prob = max_prob - p * 0.05
    stats = filter_and_analyze_labels(df, current_max_prob - 0.05, current_max_prob)
    all_results[f'{current_max_prob - 0.05}-{current_max_prob}'] = stats

# Write the results to a JSON file
with open('data_in_different_prob.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)

print("DONE.")
