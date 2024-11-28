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
    output_file = os.path.join(output_folder, f"{filename}_{segment_number}.csv")
    segment.to_csv(output_file, index=False)
    print(f"Segment {segment_number} saved to {output_file}")


def process_data_file(filepath, timestamps, output_root, padding_before=0.2, padding_after=0.2, offset=0.35):
    """
    Process a single .data file, cutting it into segments based on timestamps.
    Args:
        filepath (str): Path to the input .data file.
        timestamps (list): List of tuples with start and end times.
        output_root (str): Path to the output directory.
        padding_before (float): Padding to add before the start of each segment in seconds.
        padding_after (float): Padding to add after the end of each segment in seconds.
        offset (float): Offset to apply to all timestamps in seconds.
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

    # Process each timestamp range
    segment_number = 0
    for start, end in timestamps:
        # Apply offset and padding
        start_time = max(0, start + offset - padding_before)
        end_time = end + offset + padding_after

        # Extract the segment
        segment = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]

        if not segment.empty:
            save_segment_to_csv(segment, output_root, filename, segment_number)
            segment_number += 1


def process_all_files(input_directory, timestamps_csv, output_directory, padding_before=0.2, padding_after=0.2, offset=0.35):
    """
    Process all .data files in a directory based on timestamps from a CSV file.
    Args:
        input_directory (str): Path to the directory containing .data files.
        timestamps_csv (str): Path to the CSV file with filenames and timestamp ranges.
        output_directory (str): Path to the directory for output CSV files.
        padding_before (float): Padding to add before the start of each segment in seconds.
        padding_after (float): Padding to add after the end of each segment in seconds.
        offset (float): Offset to apply to all timestamps in seconds.
    """
    # Load the timestamp data
    timestamp_data = pd.read_csv(timestamps_csv)

    # Ensure the first column is 'File'
    if 'File' not in timestamp_data.columns:
        print("The CSV file must contain a 'File' column.")
        return

    os.makedirs(output_directory, exist_ok=True)

    # Process each .data file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".data"):
            filepath = os.path.join(input_directory, filename)
            print(f"Processing {filename}...")

            # Get the corresponding timestamps for this file
            file_name_no_ext = os.path.splitext(filename)[0]
            if file_name_no_ext not in timestamp_data['File'].values:
                print(f"No timestamps found for {file_name_no_ext}. Skipping.")
                continue

            # Extract timestamps for the current file
            file_timestamps = timestamp_data[timestamp_data['File'] == file_name_no_ext]
            timestamp_ranges = []
            for col in file_timestamps.columns[1:]:
                for entry in file_timestamps[col].dropna():
                    try:
                        start, end = map(float, entry.split(":"))
                        timestamp_ranges.append((start, end))
                    except ValueError:
                        print(f"Invalid timestamp format: {entry}. Skipping.")

            # Process the file with the extracted timestamps
            process_data_file(filepath, timestamp_ranges, output_directory, padding_before, padding_after, offset)

    print("All files processed.")


if __name__ == "__main__":
    # Define input and output directories
    input_dir = "../data/data_segments"  # Directory containing your .data files
    timestamps_csv = "../data/timestamps.csv"  # CSV file with filenames and timestamp ranges
    output_dir = "../output/data_segments"  # Directory for output segments

    # Process all .data files
    process_all_files(input_dir, timestamps_csv, output_dir)