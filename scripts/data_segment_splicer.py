import os
import pandas as pd
from PIL import Image

def save_image_segment(image_segment, output_folder, filename, segment_number):
    """
    Save an image segment to the output folder.
    Args:
        image_segment (PIL.Image): The image segment to save.
        output_folder (str): Directory to save the segment.
        filename (str): Original filename (without extension).
        segment_number (int): Segment number.
    """
    output_file = os.path.join(output_folder, f"{filename}_{segment_number}.bmp")
    image_segment.save(output_file)
    print(f"Saved segment: {output_file}")

def process_bmp_files(directory, output_root, csv_file):
    """
    Process .bmp files in the directory based on timestamp ranges in the CSV file.
    Args:
        directory (str): Directory containing .bmp files.
        output_root (str): Directory to save segmented images.
        csv_file (str): Path to the CSV file with filenames and timestamp ranges.
    """
    # Read the CSV file
    data = pd.read_csv(csv_file)
    if 'File' not in data.columns:
        print("The CSV file must contain a 'File' column.")
        return

    # Ensure the output directory exists
    os.makedirs(output_root, exist_ok=True)

    for _, row in data.iterrows():
        base_filename = row['File']
        input_path = os.path.join(directory, f"{base_filename}.bmp")
        
        if not os.path.exists(input_path):
            print(f"File {input_path} not found. Skipping.")
            continue
        
        try:
            # Open the image
            image = Image.open(input_path)
            width, height = image.size

            # Process each timestamp range
            for col in row.index[1:]:
                if pd.notna(row[col]):
                    try:
                        # Parse start and end times (assuming timestamps are in percentage of width)
                        start_percent, end_percent = map(float, row[col].split(':'))
                        start_x = int(start_percent * width)
                        end_x = int(end_percent * width)
                        
                        # Crop the image segment
                        image_segment = image.crop((start_x, 0, end_x, height))
                        
                        # Save the segment
                        segment_number = int(start_percent * 100)  # Use percentage as part of the segment number
                        save_image_segment(image_segment, output_root, base_filename, segment_number)
                    except ValueError:
                        print(f"Invalid timestamp format in column {col}: {row[col]}")
        except Exception as e:
            print(f"Error processing {input_path}: {e}")

# Define input and output directories and the CSV file
input_directory = "../data/bmp_segments"
output_directory = "../output/bmp_segments"
csv_file = "../data/timestamps.csv"

# Process .bmp files
process_bmp_files(input_directory, output_directory, csv_file)