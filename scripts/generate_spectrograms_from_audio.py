import os
import librosa
import librosa.display
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt


def mp3_to_wav(input_file, output_file):
    """
    Convert an MP3 file to a WAV file.
    Args:
        input_file (str): Path to the input MP3 file.
        output_file (str): Path to save the WAV file.
    """
    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_file)

    # Export as WAV
    audio.export(output_file, format="wav")
    print(f"Converted {input_file} to WAV: {output_file}")


def generate_spectrograms(mp3_dir, wav_output_dir, spectrogram_output_dir, frame_size=2048, hop_size=512):
    """
    Generate spectrograms from MP3 files and save them as images.
    Args:
        mp3_dir (str): Directory containing MP3 files.
        wav_output_dir (str): Directory to save WAV files.
        spectrogram_output_dir (str): Directory to save spectrogram images.
        frame_size (int): Frame size for STFT.
        hop_size (int): Hop size for STFT.
    """
    os.makedirs(wav_output_dir, exist_ok=True)
    os.makedirs(spectrogram_output_dir, exist_ok=True)

    # Process each MP3 file
    mp3_files = [os.path.join(mp3_dir, f) for f in os.listdir(mp3_dir) if f.endswith(".mp3")]
    for i, mp3_file in enumerate(mp3_files, start=1):
        try:
            # Generate the WAV file name
            base_name = os.path.splitext(os.path.basename(mp3_file))[0]
            wav_file = os.path.join(wav_output_dir, f"{base_name}.wav")

            # Convert MP3 to WAV
            mp3_to_wav(mp3_file, wav_file)

            # Extract the keyword (assumes keyword is before the first underscore '_')
            keyword = base_name.split('_')[0]

            # Create a subdirectory for the keyword in the spectrogram output directory
            keyword_dir = os.path.join(spectrogram_output_dir, keyword)
            os.makedirs(keyword_dir, exist_ok=True)

            # Load the WAV file for spectrogram generation
            signal, sr = librosa.load(wav_file, sr=None)

            # Compute the STFT and spectrogram
            S = librosa.stft(signal, n_fft=frame_size, hop_length=hop_size)
            Y = np.abs(S) ** 2
            Y_log_scale = librosa.power_to_db(Y)

            # Plot the spectrogram
            plt.figure(figsize=(10, 6))
            plt.axis('off')  # Hide axes
            plt.pcolormesh(librosa.times_like(S, sr=sr, hop_length=hop_size),
                           librosa.fft_frequencies(sr=sr, n_fft=frame_size),
                           Y_log_scale, shading='gouraud', cmap='inferno')

            # Save the spectrogram in the keyword-specific subdirectory
            spectrogram_path = os.path.join(keyword_dir, f"{base_name}_spectrogram.png")
            plt.savefig(spectrogram_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"Spectrogram saved: {spectrogram_path}")

        except Exception as e:
            print(f"Error processing {mp3_file}: {e}")


if __name__ == "__main__":
    # Directories
    mp3_dir = "../output/audio_clips"  # Directory containing MP3 files
    wav_output_dir = "../output/audio_wav_files"  # Directory to save WAV files
    spectrogram_output_dir = "../output/audio_spectrograms"  # Directory to save spectrogram images

    # Generate WAV files and spectrograms
    generate_spectrograms(mp3_dir, wav_output_dir, spectrogram_output_dir)