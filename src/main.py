import os
import sys

# This is the fix: It handles the missing console in the packaged .exe
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import threading
import customtkinter as ctk
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import ollama
import traceback

# --- Audio Configuration ---
SAMPLE_RATE = 44100
DURATION = 5  # seconds
TEMP_FILENAME = "temp_audio.wav"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # --- Window Setup ---
        self.title("EchoScribe - Linguistic Analyzer")
        self.geometry("800x650")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Widgets ---
        self.title_label = ctk.CTkLabel(self, text="EchoScribe", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.record_button = ctk.CTkButton(self, text="Click to Record for 5 Seconds and Analyze", command=self.on_record_button_click, height=40)
        self.record_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.output_textbox = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("Arial", 12))
        self.output_textbox.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # --- Initial Text ---
        self.update_textbox("Welcome to EchoScribe!\n\nClick the button above to begin.")

    def on_record_button_click(self):
        """Starts the analysis process in a new thread."""
        self.record_button.configure(state="disabled", text="Processing...")
        analysis_thread = threading.Thread(target=self.run_full_analysis)
        analysis_thread.start()

    def run_full_analysis(self):
        """The main logic for recording, transcribing, and analyzing."""
        try:
            # 1. Record and Transcribe
            self.update_textbox(f"Recording for {DURATION} seconds... Speak now!")
            recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
            sd.wait()
            write(TEMP_FILENAME, SAMPLE_RATE, recording)
            
            self.update_textbox("Recording complete. Transcribing with 'base.en' model...")
            model = whisper.load_model("base.en")
            result = model.transcribe(TEMP_FILENAME)
            transcribed_text = result["text"].strip()

            if not transcribed_text:
                self.update_textbox("Could not detect any speech. Please try again.")
                return

            # 2. Analyze with LLM
            self.update_textbox(f"Transcription:\n{transcribed_text}\n\nAnalyzing with local LLM...")
            prompt = f"""
            You are a linguistic analyst. A user has spoken a sentence. Provide a creative, hypothetical grammatical breakdown.
            Sentence: "{transcribed_text}"
            Your Hypothetical Analysis:
            """
            response = ollama.chat(model='llama3:8b', messages=[{'role': 'user', 'content': prompt}])
            analysis_result = response['message']['content']

            # 3. Display Final Result
            final_text = f"Transcription:\n{transcribed_text}\n\n--- Linguistic Analysis ---\n{analysis_result}"
            self.update_textbox(final_text)

        except Exception:
            error_message = traceback.format_exc()
            self.update_textbox(f"An error occurred:\n\n{error_message}")
        finally:
            self.record_button.configure(state="normal", text="Click to Record for 5 Seconds and Analyze")
            if os.path.exists(TEMP_FILENAME):
                os.remove(TEMP_FILENAME)

    def update_textbox(self, text):
        """Helper function to safely update the textbox from any thread."""
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", text)
        self.output_textbox.configure(state="disabled")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()