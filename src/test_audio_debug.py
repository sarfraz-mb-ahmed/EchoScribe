import sounddevice as sd
from scipy.io.wavfile import write
import traceback

# --- Configuration ---
# We are changing this to match your microphone's default sample rate.
SAMPLE_RATE = 44100
DURATION = 5  # seconds
OUTPUT_FILENAME = "test_recording.wav"

def main():
    """Main function to run the audio recording test."""
    try:
        print("--- Audio Debug Script ---")
        
        print(f"1. Settings: {DURATION} seconds, {SAMPLE_RATE} Hz")
        print("2. Attempting to start recording...")
        
        # Record audio using the corrected sample rate
        recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        
        print("3. Recording in progress...")
        
        # Wait for the recording to finish
        sd.wait()
        
        print("4. Recording finished.")
        print(f"5. Saving file as '{OUTPUT_FILENAME}'...")
        
        # Save the recording as a WAV file
        write(OUTPUT_FILENAME, SAMPLE_RATE, recording)
        
        print(f"6. Success! File saved. Check your 'echoscribe' folder.")

    except Exception:
        print("\n--- AN ERROR OCCURRED ---")
        # This will print the full error message
        traceback.print_exc()

if __name__ == '__main__':
    main()