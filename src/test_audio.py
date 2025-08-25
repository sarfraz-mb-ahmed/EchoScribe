import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import os

# --- Configuration ---
# This is the corrected sample rate for your microphone
SAMPLE_RATE = 44100
DURATION = 5  # seconds
OUTPUT_FILENAME = "temp_audio.wav"

def record_audio():
    """Records audio from the default microphone."""
    print(f"Recording for {DURATION} seconds at {SAMPLE_RATE} Hz... Speak now!")
    
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    
    write(OUTPUT_FILENAME, SAMPLE_RATE, recording)
    print(f"Audio saved as '{OUTPUT_FILENAME}'")
    return OUTPUT_FILENAME

def transcribe_audio(file_path):
    """Transcribes the audio file using Whisper."""
    print("Loading Whisper model (tiny.en)...")
    model = whisper.load_model("tiny.en")
    print("Model loaded. Transcribing...")
    
    result = model.transcribe(file_path)
    transcribed_text = result["text"]

    print("\n--- Transcription Result ---")
    print(transcribed_text)
    return transcribed_text

def main():
    """Main function to run the full audio recording and transcription test."""
    try:
        audio_file = record_audio()
        transcribe_audio(audio_file)
        os.remove(audio_file)
        print(f"\nTemporary file '{audio_file}' removed.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    main()