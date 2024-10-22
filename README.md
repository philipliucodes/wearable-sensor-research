# Project Title

Wearable Sensor Research

January 2024 - Present

## Description

This project focuses on processing and analyzing audio and video data from wearable sensors. It involves generating transcripts for media files and extracting clips for every word identified in the transcripts. The tools and scripts provided facilitate research in wearable technology and human-computer interaction.

## Getting Started

### Dependencies

- Operating System: Windows 10, macOS, or Linux
- Conda: Required for managing the Python environment
- Python Version: Python 3.9 (managed via Conda)
- FFmpeg: Must be installed and accessible via Conda

### Installing

1. Install Conda

Download and install Anaconda or Miniconda:

- Anaconda Download
- Miniconda Download

2. Create a Conda Environment

Open your terminal or command prompt and create a new Conda environment:

```
conda create -n whisper_env python=3.9
```

Activate the environment:

```
conda activate whisper_env
```

3. Install PyTorch

Install PyTorch in the Conda environment:

```
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

4. Install Whisper Timestamped

Install the whisper-timestamped package from GitHub:

```
pip install git+https://github.com/linto-ai/whisper-timestamped
```

5. Install FFmpeg

Install FFmpeg via Conda:

```
conda install -c conda-forge ffmpeg
```

6. Install Additional Dependencies

```
pip install numpy
pip install ffmpeg-python
pip install moviepy
```
