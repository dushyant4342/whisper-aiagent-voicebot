from faster_whisper import WhisperModel

# Load model once (tiny / base / small for speed)
model = WhisperModel("small", compute_type="float16")

def transcribe_audio(audio_path: str):
    segments, info = model.transcribe(audio_path, beam_size=5, language=None)

    full_text = " ".join(segment.text.strip() for segment in segments)
    detected_lang = info.language

    return full_text.strip(), detected_lang