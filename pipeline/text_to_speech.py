from TTS.api import TTS
import tempfile
import sounddevice as sd
import soundfile as sf
import os

# #Load once globally
# #tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", gpu=False)
# #> Downloading model to /Users/dushyantsharma/Library/Application Support/tts/tts_models--multilingual--multi-dataset--your_tts

# #Initialize the TTS model
# tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

# #Path to your speaker audio sample
# SPEAKER_WAV_PATH = "/Users/dushyantsharma/Desktop/awsfreetier/Repayments/ai_voice_agent-whisp-coqui/speaker.wav"
# #Speaker reference path (leave empty to use default voice)

# USE_CLONED_VOICE = True  # ✅ Toggle this (USE_CLONED_VOICE = True → uses speaker.wav )

# SUPPORTED_LANGUAGES = {"en", "hi"}

# def speak(text, lang="en"):
#     lang = lang if lang in SUPPORTED_LANGUAGES else "en"

#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
#         try:
#             if USE_CLONED_VOICE and os.path.exists(SPEAKER_WAV_PATH):
#                 tts_model.tts_to_file(
#                     text=text,
#                     file_path=f.name,
#                     language=lang,
#                     speaker_wav=SPEAKER_WAV_PATH
#                 )
#             else:
#                 tts_model.tts_to_file(
#                     text=text,
#                     file_path=f.name,
#                     language=lang
#                 )
#             data, samplerate = sf.read(f.name)
#             sd.play(data, samplerate)
#             sd.wait()
#         finally:
#             os.remove(f.name)



#speak("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ ? ", lang="hi")
#speak("Hello, how can I assist you today?", lang="en")  #Doing Great


# 🧠 Real-Time Factor Explained (CUDA)
# Real-time factor = 2.65
# Means your model took ~2.6x the audio length to generate speech (e.g., 3s audio took ~8s to synthesize).
# ✅ This is normal on CPU.
# ⚡ Want faster? 
# Try:
# Setting gpu=True (if you move to NVIDIA GPU)
# Quantizing the model (advanced)


from gtts import gTTS
import os

def speak(text, filename='response.mp3'):
    tts = gTTS(text=text)
    tts.save(filename)
    os.system(f"afplay {filename}" if os.name == 'posix' else f"start {filename}")



#speak("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ ? ", lang="hi")
#speak("Hello, how can I assist you today?")  #Doing Great
