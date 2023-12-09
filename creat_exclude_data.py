import pandas as pd
from tqdm import tqdm

# a simple method to exlcude data which are in the SET (after suveying labels and their probability)

CSVNAME = "splitted_data_list_modified.csv"
OUTPUT_FILE = "8th_exclude_result.csv"

EXCLUDE_LABELS = {'Single-lens reflex camera', 'Mantra', 'Eruption', 'Static',
                  'Livestock, farm animals, working animals', 'Mouse', 'Chirp tone',
                  'Doorbell', 'Tubular bells', 'Hoot', 'Toothbrush', 'Effects unit',
                  'Synthesizer', 'Fart', 'Power windows, electric windows', 'Bleat',
                  'Chop', 'Rub', 'Ding', 'Humming', 'Heart murmur', 'Quack', 'Thunk',
                  'Violin, fiddle', 'Mechanisms', 'Oink', 'Buzzer', 'Reverberation',
                  'Domestic animals, pets', 'Bang', 'Arrow', 'Gasp', 'Beep, bleep',
                  'Cat', 'Burst, pop', 'Heart sounds, heartbeat', 'Piano', 'Silence',
                  'Rattle', 'Telephone bell ringing', 'Scrape', 'Computer keyboard',
                  'Ding-dong', 'Meow', 'Clang', 'Hiss', 'Male singing', 'Steam',
                  'Electric piano', 'Bass guitar', 'Civil defense siren',
                  'Air horn, truck horn', 'Boing', 'Church bell', 'Motorboat, speedboat',
                  'Whip', 'Vehicle', 'Purr', 'Hum', 'Mains hum', 'Singing bowl',
                  'Ringtone', 'Ratchet, pawl', 'Car', 'Electronic tuner', 'Television',
                  'Explosion', 'Tick', 'Bell', 'Animal', 'Gong', 'Knock', 'Plop',
                  'Siren', 'Vehicle horn, car horn, honking', 'Baby cry, infant cry',
                  'Busy signal', 'Foghorn', 'White noise', 'Howl', 'Speech', 'Grunt',
                  'Bicycle bell', 'Tick-tock', 'Telephone dialing, DTMF', 'Frog',
                  'Sine wave', 'Scratch', 'Cattle, bovinae', 'Mosquito', 'Theremin',
                  'Telephone', 'Wind instrument, woodwind instrument', 'Cacophony',
                  'Rumble', 'Owl', 'Zipper (clothing)', 'Door'}

THRESHOLD = 0.2


def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error while reading CSV file: {e}")
        return None

def filter_valid_rows(df):
    if 'valid' in df.columns:
        return df[df['valid']]
    else:
        return df


def save_excluded_rows(file_path, exclude_labels, output_file):
    rawdf = pd.read_csv(file_path)
    excluded_rows = []
    df = filter_valid_rows(rawdf)

    # Iterate over each row in the DataFrame
    for index, row in tqdm(df.iterrows()):
        labels = row['Label'].split('; ')
        for label in labels:
            label_name, label_prob = label.split(': ')
            label_prob = float(label_prob)

            # Check if label is in exclude list and probability is above the threshold
            if label_name in exclude_labels and label_prob >= THRESHOLD:
                excluded_rows.append(row)
                break

    # Create a DataFrame from the excluded rows and save it to a CSV file
    excluded_df = pd.DataFrame(excluded_rows)
    excluded_df.to_csv(output_file, index=False)


save_excluded_rows(CSVNAME, EXCLUDE_LABELS, OUTPUT_FILE)