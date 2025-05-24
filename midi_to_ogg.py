#!/usr/bin/env python3
import os
import sys
import subprocess
from pydub import AudioSegment
from pydub.utils import which

def midi_to_wav(name):
    base = os.path.dirname(os.path.abspath(__file__))
    fs_exe     = r"C:\Program Files\fluidsynth-2.4.6-win10-x64\bin\fluidsynth.exe"
    sf2        = os.path.join(base, "FluidR3_GM.sf2")
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

if __name__=="__main__":
    name = sys.argv[1] if len(sys.argv)>1 else "albania"
    wav = midi_to_wav(name)
    ogg = wav_to_ogg(wav)
    print("Done:", wav, "→", ogg)
