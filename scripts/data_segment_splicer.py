import os
import pandas as pd

def save_segment_to_csv(segment, output_folder, filename, segment_number):
    """
    Save a DataFrame segment to a CSV file.
    Args:
        segment (pd.DataFrame): DataFrame containing the segment.
        output_folder (str): Path to the output folder.
        filename (str): Base filename (without extension).
        segment_number (int): Segment number.
    """
    output_file = os.path.join(output_folder, f"{filename}_segment_{segment_number}.csv")
    segment.to_csv(output_file, index=False)
    print(f"Segment {segment_number} saved to {output_file}")


def process_data_file(filepath, timestamp_data, output_root, padding=0.1):
    """
    Process a single .data file, cutting it into segments based on timestamps.
    Args:
        filepath (str): Path to the input .data file.
        timestamp_data (pd.DataFrame): DataFrame containing start and end timestamps.
        output_root (str): Path to the output directory.
        padding (float): Padding to add to the start and end of each segment in seconds.
    """
    # Extract filename without extension
    filename = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, "r") as read_file:
        # Skip header lines until "End_of_Header"
        while True:
            line = read_file.readline()
            if "***End_of_Header***" in line:
                break

        # Read the data rows into a list
        data = []
        for line in read_file:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            line_split = line.split()
            if len(line_split) != 2:  # Skip malformed lines
                continue

            try:
                time = float(line_split[0])
                current = float(line_split[1])
                data.append([time, current])
            except ValueError:
                continue  # Skip lines with invalid numerical values

    # Convert data to a DataFrame
    df = pd.DataFrame(data, columns=["Time", "Current"])

    # Filter the timestamps for the current file
    if filename not in timestamp_data['File'].values:
        print(f"No timestamps found for {filename}. Skipping.")
        return

    file_timestamps = timestamp_data[timestamp_data['File'] == filename]

    # Process each timestamp range
    segment_number = 0
    for _, row in file_timestamps.iterrows():
        start_time = max(0, row['Start'] - padding)
        end_time = row['End'] + padding

        # Extract the segment
        segment = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]

        if not segment.empty:
            save_segment_to_csv(segment, output_root, filename, segment_number)
            segment_number += 1


def process_all_files(input_directory, timestamps_csv, output_directory, padding=0.1):
    """
    Process all .data files in a directory based on timestamps from a CSV file.
    Args:
        input_directory (str): Path to the directory containing .data files.
        timestamps_csv (str): Path to the CSV file with filenames and timestamp ranges.
        output_directory (str): Path to the directory for output CSV files.
        padding (float): Padding to add to the start and end of each segment in seconds.
    """
    # Load the timestamp data
    timestamp_data = pd.read_csv(timestamps_csv)

    # Ensure required columns exist
    if not {'File', 'Start', 'End'}.issubset(timestamp_data.columns):
        print("The CSV file must contain 'File', 'Start', and 'End' columns.")
        return

    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith(".data"):
            filepath = os.path.join(input_directory, filename)
            print(f"Processing {filename}...")
            process_data_file(filepath, timestamp_data, output_directory, padding)

    print("All files processed.")

# Define input and output directories
input_dir = "../data/data_segments"  # Directory containing your .data files
timestamps_csv = "../data/timestamps.csv"  # CSV file with filenames and timestamp ranges
output_dir = "../output/data_segments"  # Directory for output segments

# Process all .data files
process_all_files(input_dir, timestamps_csv, output_dir)