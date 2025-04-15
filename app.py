import gradio as gr
print("✅ Gradio is working!")
import tempfile
from pipeline.speech_to_text import transcribe_and_detect_lang
from pipeline.text_to_speech import speak
from pipeline.gpt_request import call_gpt
from utils.qdrant_client import get_memory_context, store_memory
from utils.env_loader import get_env_var

qdrant_path = get_env_var("QDRANT_HOST")
collection = get_env_var("COLLECTION_NAME")
realid = str(get_env_var("REALID", 101))

def voice_agent(audio_path):
    if audio_path is None:
        return "No input", None

    # Transcribe & detect language
    text, lang = transcribe_and_detect_lang(audio_path)

    # Store user message
    store_memory(text, person_id=realid, role="user", memory_type="chat",
                 collection_name=collection, qdrant_path=qdrant_path, language=lang)

    # Build prompt
    context = get_memory_context(realid, collection, qdrant_path)
    prompt = f"{context}\\n\\nUser: {text}\\nAssistant:"
    response = call_gpt(prompt)

    # Store and generate TTS
    store_memory(response, person_id=realid, role="assistant", memory_type="chat",
                 collection_name=collection, qdrant_path=qdrant_path, language=lang)

    audio_out_path = speak(response)
    return response, audio_out_path

gr.Interface(fn=voice_agent,
             inputs=gr.Audio(label="🎙️ Speak now", type="filepath"),
             outputs=[gr.Textbox(label="🧠 GPT Response"), gr.Audio(label="🔊 Assistant Says")],
             title="🗣️ Real-Time AI Voice Agent",
             live=True).launch()
