import os

def rename_audio_files(directory):
    """
    Rename audio files in the directory:
    - Convert to lowercase.
    - Replace 'noise' with 'n'.
    - Replace '-' with '_'.
    Args:
        directory (str): Path to the directory containing audio files.
    """
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        # Skip non-audio files
        if not filename.lower().endswith(('.mp3', '.wav', '.aac', '.m4a')):
            continue
        
        # Process the filename
        new_filename = filename.lower().replace("noise", "n").replace("-", "_")
        
        # Rename the file
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        # Rename and print the operation
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

# Directory containing the audio files
audio_directory = "../data/audio_clips"  # Update with the actual directory path
    
# Rename files in the specified directory
rename_audio_files(audio_directory)