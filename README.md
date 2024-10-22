# Wearable Sensor Research

**Audio Analyzer and Splicer**  
_January 2024 - Present_

## Description

This project focuses on processing and analyzing audio and video data collected from wearable sensors. It involves generating transcripts from media files and extracting video or audio clips for each word identified in the transcripts. The provided tools and scripts support research in **wearable technology** and **human-computer interaction**.

---

## Getting Started

### Dependencies

- **Operating System:** Windows 10, macOS, or Linux
- **Conda:** Required for managing the Python environment
- **Python Version:** Python 3.9 (managed via Conda)
- **FFmpeg:** Must be installed and accessible via Conda

---

## Installation

### 1. Install Conda

Download and install Anaconda or Miniconda:

- [Anaconda Distribution](https://www.anaconda.com/products/distribution)
- [Miniconda Installer](https://docs.conda.io/en/latest/miniconda.html)

### 2. Create a Conda Environment

Open your terminal or command prompt and create a new Conda environment:

```bash
conda create -n whisper_env python=3.9
```

Activate the environment:

```bash
conda activate whisper_env
```

### 3. Install PyTorch

Install PyTorch in the Conda environment:

```bash
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

### 4. Install Whisper Timestamped

Install the `whisper-timestamped` package from GitHub:

```bash
pip install git+https://github.com/linto-ai/whisper-timestamped
```

### 5. Install FFmpeg

Install FFmpeg via Conda:

```bash
conda install -c conda-forge ffmpeg
```

### 6. Install Additional Dependencies

Run the following commands to install additional packages:

```bash
pip install numpy
pip install ffmpeg-python
pip install moviepy
```

---

## Usage

After setting up the environment, activate the `whisper_env` environment before running your scripts:

```bash
conda activate whisper_env
```

You can then use the scripts to generate transcripts and extract word-level clips from your audio or video files.

---

## Conclusion

This project enables advanced analysis of wearable sensor data through speech transcription and media processing. Make sure to keep your Conda environment activated when working on related scripts to ensure all dependencies are properly loaded.
