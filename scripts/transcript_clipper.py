import os
import json
from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Set the directories
transcripts_directory = "../output/transcripts/0531-new healthy"  # Directory containing your transcript JSON files
media_directory = "../data/0531-new healthy"  # Directory containing your original video/audio files
output_directory = "../output/clips"  # Directory where the clips will be saved
os.makedirs(output_directory, exist_ok=True)

# List of supported media file extensions
supported_extensions = ('.mp4', '.mp3', '.wav', '.m4a')

# Get a list of all transcript files
transcript_files = [
    f for f in os.listdir(transcripts_directory)
    if f.lower().endswith('_transcript.json')
]

# Process each transcript file
for transcript_file in transcript_files:
    transcript_path = os.path.join(transcripts_directory, transcript_file)
    media_filename = transcript_file.replace('_transcript.json', '')
    
    # Find the corresponding media file
    media_file = None
    for ext in supported_extensions:
        possible_media_path = os.path.join(media_directory, media_filename + ext)
        if os.path.isfile(possible_media_path):
            media_file = possible_media_path
            break
    
    if media_file is None:
        print(f"No corresponding media file found for {transcript_file}")
        continue  # Skip to the next transcript if no media file is found
    
    print(f"Processing transcript: {transcript_path}")
    print(f"Corresponding media file: {media_file}")
    
    # Load the transcript data
    with open(transcript_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Process each word in the transcript
    words = []
    if 'words' in data:
        # For newer versions of whisper_timestamped that include 'words' at the top level
        words = data['words']
    else:
        # For older versions, need to extract words from segments
        for segment in data.get('segments', []):
            words.extend(segment.get('words', []))
    
    for idx, word_info in enumerate(words):
        word_text = word_info['text'].strip()
        start_time = word_info['start']
        end_time = word_info['end']
        
        # Construct a unique output filename
        output_filename = f"{media_filename}_word_{idx}_{word_text.replace(' ', '_')}.mp4"  # Default to .mp4
        output_path = os.path.join(output_directory, output_filename)
        
        try:
            if media_file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                # For video files
                video = VideoFileClip(media_file)
                video_clip = video.subclip(start_time, end_time)
                video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
                print(f"Video clip saved at {output_path}")
                video_clip.close()
                video.close()
            elif media_file.lower().endswith(('.mp3', '.wav', '.m4a', '.aac', '.flac')):
                # For audio files
                audio = AudioFileClip(media_file)
                audio_clip = audio.subclip(start_time, end_time)
                # Change the output extension to .mp3
                output_filename = f"{media_filename}_word_{idx}_{word_text.replace(' ', '_')}.mp3"
                output_path = os.path.join(output_directory, output_filename)
                audio_clip.write_audiofile(output_path)
                print(f"Audio clip saved at {output_path}")
                audio_clip.close()
                audio.close()
            else:
                print(f"Unsupported media file format: {media_file}")
        except Exception as e:
            print(f"Error processing word '{word_text}' in {media_file}: {e}")
            continue  # Skip to the next word

print("All clips generated successfully!")
