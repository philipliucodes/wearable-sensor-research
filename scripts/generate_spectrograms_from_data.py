import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.io.wavfile import write


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


def generate_spectrograms(input_csv_dir, wav_output_dir, spectrogram_output_dir, sampling_frequency_override=None):
    """
    Generate spectrograms from CSV files and save them as images.
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

            # Load the CSV data
            data = pd.read_csv(csv_file)
            if 'Time' not in data.columns or 'Current' not in data.columns:
                print(f"Invalid columns in {csv_file}. Skipping.")
                continue

            # Extract time and current values
            time = data['Time'].values
            current = data['Current'].values

            # Define the sampling frequency based on time intervals
            if sampling_frequency_override:
                fs = sampling_frequency_override
            else:
                fs = 1 / (time[1] - time[0])  # Assuming uniform sampling

            # Compute the spectrogram
            frequencies, times, Sxx = spectrogram(current, fs)

            # Define intensity limits for the color map
            intensity_min = -310  # Adjust based on your requirements
            intensity_max = 10 * np.log10(Sxx.max())  # Maximum intensity in dB

            # Create a unique name for the WAV file
            wav_output_path = os.path.join(wav_output_dir, f"{base_name}_wav.wav")
            csv_to_wav(csv_file, wav_output_path)

            # Plot and save the spectrogram
            plt.figure(figsize=(10, 6))
            plt.ylim(0, 8000)  # Limit the y-axis to 8 kHz
            plt.axis('off')  # Hide axes
            plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud', cmap='inferno',
                           vmin=intensity_min, vmax=intensity_max)

            spectrogram_output_path = os.path.join(spectrogram_output_dir, f"{base_name}_spectrogram.png")
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

    # Step 1: Convert CSV files to WAV files
    csv_files = [os.path.join(input_csv_dir, f) for f in os.listdir(input_csv_dir) if f.endswith(".csv")]
    for csv_file in csv_files:
        wav_file = os.path.join(wav_output_dir, os.path.splitext(os.path.basename(csv_file))[0] + ".wav")
        csv_to_wav(csv_file, wav_file)

    # Step 2: Generate spectrograms from CSV files
    generate_spectrograms(input_csv_dir, wav_output_dir, spectrogram_output_dir)