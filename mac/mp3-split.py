#!/usr/bin/env python
# coding=utf-8

import subprocess
import re
import os

"""
Script: mp3-split.py

Description:
This script splits an MP3 file into multiple segments based on non-silent parts. It uses 'ffmpeg' to detect
silence in the audio file and then splits the file at points where non-silent segments are identified. Each segment
ends at the start of a silence period. The script accepts command-line arguments to specify the MP3 file, the noise
level in dB for silence detection, and the minimum duration of silence. The default settings for silence detection
are -30 dB and 5 seconds.

Usage:
python split_mp3_on_nonsilence.py <input_file.mp3> [-d <silence_noise_level_dB>] [-t <silence_duration_seconds>]

where:
- <input_file.mp3> is the path to the input MP3 file.
- <silence_noise_level_dB> is an optional argument to set the noise level for silence detection (default is -30 dB).
- <silence_duration_seconds> is an optional argument to set the minimum duration of silence (default is 5 seconds).

Requirements:
- 'ffmpeg' and 'ffprobe' should be installed and accessible in the system's PATH.

Output:
The script outputs multiple MP3 files, each corresponding to a non-silent segment in the input file. These files
are named sequentially with the pattern 'inputfilename_nonsilence_01.mp3', 'inputfilename_nonsilence_02.mp3', etc.

Author: Frank + ChatGPT4
Date: 2024/01/15
"""

def split_mp3(input_file, silence_duration=5.0, silence_noise=-30):
    # Step 1: Detect silence and get timestamps
    cmd = [
        'ffmpeg', '-i', input_file, '-af',
        f'silencedetect=noise={silence_noise}dB:d={silence_duration}', '-f', 'null', '-'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stderr.split('\n')

    # Step 2: Parse the timestamps to find non-silent segments
    nonsilence_parts = []
    last_silence_end = 0
    for line in lines:
        if 'silence_end' in line:
            end = float(re.search(r'silence_end: (\d+(\.\d+)?)', line).group(1))
            nonsilence_parts.append([last_silence_end, end])
            last_silence_end = end

    # Adding the last non-silence part if it exists
    if last_silence_end < get_duration(input_file):
        nonsilence_parts.append([last_silence_end, get_duration(input_file)])

    # Step 3: Split the file using the non-silent timestamps
    for i, (start, end) in enumerate(nonsilence_parts):
        output_file = f"{os.path.splitext(input_file)[0]}_nonsilence_{i+1:02d}.mp3"
        cmd = [
            'ffmpeg', '-i', input_file, '-ss', str(start), '-to', str(end),
            '-acodec', 'libmp3lame', '-b:a', '320k', output_file
        ]
        subprocess.run(cmd)

    print("Splitting on non-silence completed.")

def get_duration(filename):
    """Get the duration of the audio file."""
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
           'default=noprint_wrappers=1:nokey=1', filename]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

# Replace 'yourfile.mp3' with your MP3 file's name
split_mp3('Top 5 Cockatiel Whistles.m4a')
