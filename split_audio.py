import torchaudio
import os
import glob

# Used for spilt original audio data set

INPUTPATH = "./data/cloudbank-amp-only"
OUTPUTPATH = "/media/mountain/Data"

def split_and_save_audio(file_path, output_dir, total_segments=60):
    waveform, sample_rate = torchaudio.load(file_path)

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    samples_per_segment = len(waveform[0]) // total_segments

    for i in range(total_segments):
        start_sample = i * samples_per_segment
        end_sample = (i + 1) * samples_per_segment

        if end_sample > len(waveform[0]):
            end_sample = len(waveform[0])

        segment = waveform[:, start_sample:end_sample]

        segment_file_name = f"{name}_{i:02d}{ext}"
        segment_file_path = os.path.join(output_dir, segment_file_name)

        torchaudio.save(segment_file_path, segment, sample_rate)

def split_audio_files_in_folder(folder_path, output_dir, total_segments=60):
    files = glob.glob(os.path.join(folder_path, '*'))
    
    for file_path in files:
        split_and_save_audio(file_path, output_dir, total_segments)


folder_path = INPUTPATH
output_dir = OUTPUTPATH
split_audio_files_in_folder(folder_path, output_dir)
