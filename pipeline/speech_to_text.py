import whisper
#from langdetect import detect
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav

model = whisper.load_model("large")  # use "small" or "medium" for better accuracy

#✅ Use one of: "tiny", "base", "small", "medium", "large"


def record_audio(duration=5, samplerate=16000):
    print("🎤 Listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    audio = np.squeeze(audio)
    
    # Save to temp WAV for Whisper
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, samplerate, audio.astype(np.int16))
        return f.name

def transcribe_and_detect_lang(duration=5):
    #wav_file = record_audio(duration)
    wav_file = record_until_speech_ends()
    result = model.transcribe(wav_file)
    text = result["text"].strip()
    lang = result["language"]
    print(f"🧠 Recognized: {text}  🌐 Language: {lang}")
    return text, lang

import webrtcvad
import pyaudio
import collections
import os
import wave
import tempfile

vad = webrtcvad.Vad(1)  # Aggressiveness: 0 (least) to 3 (most)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAME_DURATION = 30  # ms
MAX_SILENCE_FRAMES = 120  #  (each frame ~30ms → MAX_SILENCE_FRAMES 60 = ~2s silence)
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)


def record_until_speech_ends():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=FRAME_SIZE)

    print("🎤 Listening (VAD enabled)...")
    frames = collections.deque()
    silence_counter = 0
    triggered = False

    while True:
        frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
        is_speech = vad.is_speech(frame, RATE)

        if not triggered:
            if is_speech:
                triggered = True
                frames.append(frame)
        else:
            frames.append(frame)
            if not is_speech:
                silence_counter += 1
            else:
                silence_counter = 0
            if silence_counter > MAX_SILENCE_FRAMES:
                print("🛑 Silence detected. Stopping recording.")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wf = wave.open(f.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"✅ Audio saved to: {f.name}")
        return f.name
