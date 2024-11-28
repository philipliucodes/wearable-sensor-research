import os
import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import librosa
import librosa.display
import matplotlib.pyplot as plt


def csv_to_wav(input_csv, output_wav, sample_rate=44100):
    """
    Convert a CSV (Time, Current) file to a WAV file.
    Args:
        input_csv (str): Path to the input CSV file.
        output_wav (str): Path to save the output WAV file.
        sample_rate (int): Sampling rate for the WAV file.
    """
    # Read the CSV file
    data = pd.read_csv(input_csv)
    if 'Current' not in data.columns:
        print(f"No 'Current' column in {input_csv}. Skipping.")
        return

    # Normalize the current values to fit in the range [-1, 1]
    current = data['Current'].values
    normalized_current = current / np.max(np.abs(current))

    # Convert to 16-bit PCM format
    pcm_data = np.int16(normalized_current * 32767)

    # Write the WAV file
    write(output_wav, sample_rate, pcm_data)
    print(f"WAV file saved: {output_wav}")


def generate_spectrograms(wav_files, output_folder, frame_size=2048, hop_size=512):
    """
    Generate spectrograms from a list of WAV files and save them as images.
    Args:
        wav_files (list): List of paths to WAV files.
        output_folder (str): Folder to save the spectrogram images.
        frame_size (int): Frame size for STFT.
        hop_size (int): Hop size for STFT.
    """
    os.makedirs(output_folder, exist_ok=True)

    for wav_file in wav_files:
        try:
            # Load the WAV file
            signal, sr = librosa.load(wav_file, sr=None)

            # Compute the spectrogram
            S = librosa.stft(signal, n_fft=frame_size, hop_length=hop_size)
            Y = np.abs(S) ** 2
            Y_log_scale = librosa.power_to_db(Y)

            # Plot the spectrogram
            plt.figure(figsize=(10, 5))
            librosa.display.specshow(Y_log_scale, sr=sr, hop_length=hop_size, x_axis="time", y_axis="linear")
            plt.axis('off')  # Remove axis
            plt.colorbar(format="%+2.f").remove()  # Remove color bar

            # Save the spectrogram image with the same name as the WAV file
            base_name = os.path.basename(wav_file).replace("segment", "").replace(".wav", "")
            spectrogram_path = os.path.join(output_folder, f"{base_name}.jpg")
            plt.savefig(spectrogram_path, format="jpg", bbox_inches="tight")
            plt.close()
            print(f"Spectrogram saved: {spectrogram_path}")
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")


# Directories
input_csv_dir = "../output/data_segments"  # Directory containing spliced CSV files
wav_output_dir = "../output/wav_files"  # Directory to save WAV files
spectrogram_output_dir = "../output/spectrograms"  # Directory to save spectrogram images

# Create output directories if they don't exist
os.makedirs(wav_output_dir, exist_ok=True)
os.makedirs(spectrogram_output_dir, exist_ok=True)

# Step 1: Convert CSV files to WAV files
csv_files = [os.path.join(input_csv_dir, f) for f in os.listdir(input_csv_dir) if f.endswith(".csv")]
wav_files = []
for csv_file in csv_files:
    wav_file = os.path.join(wav_output_dir, os.path.splitext(os.path.basename(csv_file))[0] + ".wav")
    csv_to_wav(csv_file, wav_file)
    wav_files.append(wav_file)

# Step 2: Generate spectrograms from WAV files
generate_spectrograms(wav_files, spectrogram_output_dir)