#!/usr/bin/env python3
import os
import sys
import subprocess
from pydub import AudioSegment
from pydub.utils import which

def midi_to_wav(name):

    base = os.getcwd()
    fs_exe     = r"C:\Program Files\fluidsynth-2.4.6-win10-x64\bin\fluidsynth.exe"
    sf2        = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FluidR3_GM.sf2")
    mid_path   = os.path.join(base, f"{name}.mid")
    wav_path   = os.path.join(base, f"{name}.wav")
    for p,d in [(fs_exe,"fluidsynth"),(sf2,"SoundFont"),(mid_path,"MIDI")]:
        if not os.path.isfile(p):
            sys.exit(f"Missing {d}: {p}")
    subprocess.run([fs_exe,"-ni","-F",wav_path,"-r","44100",sf2,mid_path], check=True)
    return wav_path

def wav_to_ogg(wav_path):
    # ensure ffmpeg is found
    ff = which("ffmpeg")
    if not ff or not os.path.isfile(ff):
        sys.exit("Error: ffmpeg.exe not found on PATH")
    AudioSegment.converter = ff

    ogg = os.path.splitext(wav_path)[0] + ".ogg"
    AudioSegment.from_wav(wav_path).export(ogg, format="ogg")
    return ogg

def batch_midi_to_ogg(midi_names, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    ogg_files = []
    for name in midi_names:
        wav = midi_to_wav(name)
        ogg_name = f"{name}.ogg"
        ogg_path = os.path.join(output_folder, ogg_name)
        # Convert WAV to OGG in the output folder
        ff = which("ffmpeg")
        if not ff or not os.path.isfile(ff):
            sys.exit("Error: ffmpeg.exe not found on PATH")
        AudioSegment.converter = ff
        AudioSegment.from_wav(wav).export(ogg_path, format="ogg")
        ogg_files.append(ogg_path)
        # Remove temporary WAV
        os.remove(wav)
    return ogg_files

if __name__ == "__main__":
    midi_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oceania_anthems")
    midi_files = [f for f in os.listdir(midi_folder) if f.endswith(".mid")]
    midi_names = [os.path.splitext(f)[0] for f in midi_files]
    print("Found MIDI files:", midi_files)
    # Temporarily change working directory so midi_to_wav finds the files
    old_cwd = os.getcwd()
    os.chdir(midi_folder)
    batch_midi_to_ogg(midi_names, os.path.join(old_cwd, "output_oggs"))
    os.chdir(old_cwd)