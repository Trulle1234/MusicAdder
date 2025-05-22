from midi2audio import FluidSynth
import os
import sys
import shutil

def midi_to_wav(name):
    # ─── 0) Tell Python where your fluidsynth.exe lives ─────────────────────────────
    fs_bin = r"C:\Users\leona\Downloads\fluidsynth-2.4.6-win10-x64"
    os.environ["PATH"] = fs_bin + os.pathsep + os.environ.get("PATH", "")

    # ─── 1) Full path to your SoundFont (.sf2) ────────────────────────────────────
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_font = os.path.join(script_dir, "FluidR3_GM.sf2")
    if not os.path.isfile(sound_font):
        sys.exit(f"Error: SoundFont not found ➞ {sound_font}")

    # ─── 2) Verify fluidsynth is on the PATH ──────────────────────────────────────
    if shutil.which("fluidsynth") is None:
        sys.exit("Error: 'fluidsynth.exe' not found on PATH. Check fs_bin above.")

    # ─── 3) Initialize FluidSynth (uses the 'fluidsynth' command) ────────────────
    fs = FluidSynth(sound_font)

    # ─── 4) Build input/output filenames ─────────────────────────────────────────
    input_midi  = os.path.join(script_dir, f"{name}.mid")
    output_wav  = os.path.join(script_dir, f"{name}.wav")

    if not os.path.isfile(input_midi):
        sys.exit(f"Error: MIDI file not found ➞ {input_midi}")

    # ─── 5) Render MIDI → WAV ───────────────────────────────────────────────────
    fs.midi_to_audio(input_midi, output_wav)

    # ─── 6) Report success ───────────────────────────────────────────────────────
    print("Converted:")
    print("  MIDI:", input_midi)
    print("   WAV:", output_wav)

if __name__ == "__main__":
    midi_to_wav("albania")
