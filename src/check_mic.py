import sounddevice as sd

print("--- Listing Audio Devices ---")
try:
    print(sd.query_devices())
    print("\n--- Default Input Device ---")
    print(sd.query_devices(kind='input'))
except Exception as e:
    print(f"An error occurred: {e}")