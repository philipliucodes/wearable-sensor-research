import os
from pydub import AudioSegment

def convert_m4a_to_mp3(input_dir, output_dir):
    """
    Convert all .m4a files in the input directory to .mp3 format and save them to the output directory.
    Args:
        input_dir (str): Path to the directory containing .m4a files.
        output_dir (str): Path to the directory to save converted .mp3 files.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".m4a"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                # Load the .m4a file
                audio = AudioSegment.from_file(input_path, format="m4a")
                # Export the file as .mp3
                audio.export(output_path, format="mp3")
                print(f"Converted: {filename} -> {output_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    # Define input and output directories
    input_directory = "../data/audio_clips"  # Update with your .m4a files directory
    output_directory = "../data/audio_clips"  # Update with your desired output directory
        
    # Run the conversion function
    convert_m4a_to_mp3(input_directory, output_directory)