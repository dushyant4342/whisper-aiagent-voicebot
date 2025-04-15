import sounddevice as sd
import soundfile as sf

def record_speaker_voice(filename="speaker.wav", duration=6):
    print("🎤 Recording your voice for 6 seconds...")
    audio = sd.rec(int(duration * 22050), samplerate=22050, channels=1)
    sd.wait()
    sf.write(filename, audio, 22050)
    print(f"✅ Saved speaker reference as {filename}")

#record_speaker_voice("speaker.wav", 30)

#The speaker.wav file is used by Coqui XTTS to:
#🎙️ Clone the speaker's voice — it extracts voice features and uses them to generate new speech in that same voice, across supported languages.

# tts_model.tts_to_file(
#     text="Your message",
#     speaker_wav="speaker.wav",
#     language="en",
#     file_path="output.wav"
# )
