import os
import json
import whisper_timestamped as whisper

# Function to adjust start and end times (optional, kept for consistency)
def adjust_start_time(start_time):
    return int(start_time) - 0.2

def adjust_end_time(end_time):
    return int(end_time) + 0.75

# Specify the input directory containing your videos
input_directory = "../data/0531-new healthy"

# Specify the output directory for the transcripts
output_directory = "../output/transcripts/0531-new healthy"
os.makedirs(output_directory, exist_ok=True)

# List of supported video/audio file extensions
supported_extensions = ('.mp4', '.mp3', '.wav', '.m4a')

# Get a list of all video/audio files in the input directory
video_files = [
    f for f in os.listdir(input_directory)
    if f.lower().endswith(supported_extensions)
]

# Load the Whisper model once before processing
model = whisper.load_model("tiny", device="cpu")

# Process each video file
for video_file in video_files:
    input_path = os.path.join(input_directory, video_file)
    print(f"Processing {input_path}")
    
    try:
        # Load the audio from the video file
        audio = whisper.load_audio(input_path)
        
        # Transcribe the audio
        result = whisper.transcribe(model, audio, language="en")
        
        # Save the transcript to a JSON file
        transcript_filename = f"{os.path.splitext(video_file)[0]}_transcript.json"
        transcript_output_path = os.path.join(output_directory, transcript_filename)
        with open(transcript_output_path, 'w') as json_file:
            json.dump(result, json_file, indent=2, ensure_ascii=False)
        
        print(f"Transcript saved at {transcript_output_path}")
    except Exception as e:
        print(f"An error occurred while processing {video_file}: {e}")

print("All transcripts generated successfully!")