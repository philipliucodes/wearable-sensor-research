import os
import numpy as np
import pandas as pd
import librosa
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

def csv_to_wav(input_csv, output_wav, sample_rate=44100):
    """
    Convert a CSV (Time, Current) file to a WAV file.
    Args:
        input_csv (str): Path to the input CSV file.
        output_wav (str): Path to save the WAV file.
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

def generate_spectrograms(input_csv_dir, wav_output_dir, spectrogram_output_dir, sampling_frequency_override=None):
    """
    Generate spectrograms from CSV files and save them as images in subdirectories based on keywords.
    Args:
        input_csv_dir (str): Directory containing input CSV files.
        wav_output_dir (str): Directory to save WAV files.
        spectrogram_output_dir (str): Directory to save spectrogram images.
        sampling_frequency_override (float): Override for sampling frequency, if desired.
    """
    os.makedirs(wav_output_dir, exist_ok=True)
    os.makedirs(spectrogram_output_dir, exist_ok=True)

    # Process each CSV file
    csv_files = [os.path.join(input_csv_dir, f) for f in os.listdir(input_csv_dir) if f.endswith(".csv")]
    for csv_file in csv_files:
        try:
            # Extract the base name of the CSV file (without extension)
            base_name = os.path.splitext(os.path.basename(csv_file))[0]

            # Extract the keyword from the file name (e.g., the first part before the underscore)
            keyword = base_name.split('_')[0]

            # Create a subdirectory for the keyword inside the spectrogram output directory
            keyword_dir = os.path.join(spectrogram_output_dir, keyword)
            os.makedirs(keyword_dir, exist_ok=True)

            # Create the WAV file name
            wav_output_path = os.path.join(wav_output_dir, f"{base_name}.wav")

            # Convert CSV to WAV
            csv_to_wav(csv_file, wav_output_path)

            # Load the WAV file for spectrogram generation
            signal, sr = librosa.load(wav_output_path, sr=None)

            # Compute the spectrogram
            S = librosa.stft(signal, n_fft=2048, hop_length=512)
            Y = np.abs(S) ** 2
            Y_log_scale = librosa.power_to_db(Y)

            # Plot the spectrogram
            plt.figure(figsize=(10, 6))
            plt.axis('off')  # Hide axes
            plt.pcolormesh(librosa.times_like(S, sr=sr, hop_length=512),
                           librosa.fft_frequencies(sr=sr, n_fft=2048),
                           Y_log_scale, shading='gouraud', cmap='inferno')

            # Save the spectrogram as an image in the keyword directory
            spectrogram_output_path = os.path.join(keyword_dir, f"{base_name}_spectrogram.png")
            plt.savefig(spectrogram_output_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"Spectrogram saved: {spectrogram_output_path}")

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")


if __name__ == "__main__":
    # Directories
    input_csv_dir = "../output/data_segments"  # Directory containing spliced CSV files
    wav_output_dir = "../output/data_wav_files"  # Directory to save WAV files
    spectrogram_output_dir = "../output/data_spectrograms"  # Directory to save spectrogram images

    # Create output directories if they don't exist
    os.makedirs(wav_output_dir, exist_ok=True)
    os.makedirs(spectrogram_output_dir, exist_ok=True)

    generate_spectrograms(input_csv_dir, wav_output_dir, spectrogram_output_dir)