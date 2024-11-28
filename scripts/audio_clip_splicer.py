import os
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm

def splice_audio(input_file, output_file, start_time, end_time):
    """
    Splice an audio file from start_time to end_time.
    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the spliced audio.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
    """
    try:
        audio = AudioSegment.from_file(input_file)
        duration = len(audio) / 1000.0  # Get the total duration of the audio in seconds
        
        # Ensure padding does not exceed the audio duration
        adjusted_start = max(0, start_time - 0.1)
        adjusted_end = min(duration, end_time + 0.1)
        
        spliced_audio = audio[adjusted_start * 1000:adjusted_end * 1000]  # Convert to milliseconds
        spliced_audio.export(output_file, format="mp3")
    except Exception as e:
        print(f"Error processing {output_file}: {e}")

def process_audio_clips(input_dir, output_dir, csv_file):
    """
    Process audio files based on timestamp ranges in the CSV file.
    Args:
        input_dir (str): Directory containing input audio files.
        output_dir (str): Directory to save output clips.
        csv_file (str): Path to the CSV file with filenames and timestamp ranges.
    """
    # Load the CSV file
    data = pd.read_csv(csv_file)
    if 'File' not in data.columns:
        print("The CSV file must contain a 'File' column.")
        return
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each row in the CSV
    for _, row in tqdm(data.iterrows(), total=len(data), desc="Processing files"):
        base_filename = row['File']
        input_path = os.path.join(input_dir, f"{base_filename}.mp3")
        
        if not os.path.exists(input_path):
            print(f"File {input_path} not found. Skipping.")
            continue
        
        # Iterate over the timestamp columns
        for col in row.index[1:]:
            if pd.notna(row[col]):
                try:
                    # Parse start and end times
                    start_time, end_time = map(float, row[col].split(':'))
                    # Generate output filename
                    output_path = os.path.join(output_dir, f"{base_filename}_{start_time:.3f}-{end_time:.3f}.mp3")
                    # Splice the audio with padding
                    splice_audio(input_path, output_path, start_time, end_time)
                except ValueError:
                    print(f"Invalid timestamp format in column {col}: {row[col]}")

# Define directories and CSV file
input_directory = "../data/audio_clips"
output_directory = "../output/audio_clips"
csv_file = "../data/timestamps.csv"

# Run the processing function
process_audio_clips(input_directory, output_directory, csv_file)