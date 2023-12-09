import pandas as pd

# Check TOP_N predict labels whether they are in the given labels

CSVNAME = "splitted_data_list_modified.csv"
RESULT_CSV = "result_other.csv"
TOP_N = 2
CONTAIN_IN_SET = True
# Set of specific labels to check
CHECK_LABEL = {'Ringtone', 'Air horn, truck horn', 'Domestic animals, pets', 'Heart murmur', 'Singing bowl',
               'Single-lens reflex camera', 'Brass instrument', 'Neigh, whinny', 'Television', 'Bell',
               'Mains hum', 'Hoot', 'Squeak', 'Banjo', 'Didgeridoo', 'Beep, bleep', 'Crowing, cock-a-doodle-doo',
               'Creak', 'Ding-dong', 'Bang', 'Tick', 'Video game music', 'Scrape', 'Engine', 'Tick-tock',
               'Chicken, rooster', 'Fly, housefly', 'Accordion', 'Water', 'Plop', 'Rain', 'Insect', 'Grunt',
               'Sheep', 'Owl', 'Theremin', 'Fowl', 'Stomach rumble', 'Mechanisms', 'Knock', 'Roaring cats (lions, tigers)',
               'Siren', 'Cash register', 'Spray', 'Meow', 'Turkey', 'Electronic tuner', 'Timpani', 'Quack', 'Mosquito',
               'Heart sounds, heartbeat', 'Vehicle', 'Jingle bell', 'White noise', 'Frog', 'Lullaby', 'Whistling',
               'Dog', 'Keyboard (musical)', 'Static', 'Zipper (clothing)', 'Busy signal', 'Bass guitar',
               'Vehicle horn, car horn, honking', 'Electric piano', 'Clang', 'Violin, fiddle', 'Cattle, bovinae',
               'Trumpet', 'Explosion', 'Sine wave', 'Church bell', 'Chirp tone', 'Echo', 'Male singing',
               'Synthetic singing', 'Buzzer', 'Animal', 'Electronic music', 'Mandolin', 'Bleat', 'Ukulele',
               'Doorbell', 'Reverberation', 'Emergency vehicle', 'Speech', 'Boing', 'Roar', 'Zither', 'Silence',
               'Clatter', 'Double bass', 'Saxophone', 'Gong', 'Piano', 'Whip', 'Door', 'Synthesizer', 'Hum', 'Cat',
               'Humming', 'Hiss', 'Slam', 'Ratchet, pawl', 'Foghorn', 'Gobble', 'Rain on surface', 'Cacophony',
               'Fart', 'Burst, pop', 'Croak', 'Moo', 'Ding', 'Sound effect', 'Purr', 'Scratch', 'Trombone'}

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error while reading CSV file: {e}")
        return None

def filter_valid_rows(df):
    # Check if 'valid' column exists and return rows where 'valid' is True
    if 'valid' in df.columns:
        return df[df['valid']]
    else:
        # If 'valid' column does not exist, return the original DataFrame
        return df

def extract_labels(df, n=1):
    # Extract the top 'n' labels from the 'Label' column of the DataFrame
    return [
        row['Label'].split('; ')[:n]
        for index, row in df.iterrows()
        if isinstance(row['Label'], str) and not pd.isna(row['Label'])
    ]

def save_labels(df, n, S, exist=True):
    # Extract valid labels based on the top 'n' labels
    valid_labels = extract_labels(df, n)
    # Filter rows based on whether their labels exist in the set 'S'
    if exist:
        valid_rows = df.iloc[[i for i, labels in enumerate(valid_labels) if any(label.split(': ')[0] in S for label in labels)]]
    else:
        valid_rows = df.iloc[[i for i, labels in enumerate(valid_labels) if not any(label.split(': ')[0] in S for label in labels)]]

    # Save the filtered rows to a CSV file
    valid_rows.to_csv(RESULT_CSV, index=False)


rawdatafile = load_data(CSVNAME)
datafile = filter_valid_rows(rawdatafile)
save_labels(datafile, TOP_N, S=CHECK_LABEL, exist=CONTAIN_IN_SET)
