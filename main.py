#from pipeline.input_capture import capture_audio_and_save
#from pipeline.vector_search import get_similar_docs
from pipeline.prompt_builder import build_prompt
from pipeline.gpt_request import call_gpt
from pipeline.text_to_speech import speak
from utils.env_loader import get_env_var
from utils.qdrant_client import upload_csv_to_qdrant, search_by_realid
from sentence_transformers import SentenceTransformer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from utils.qdrant_client import store_memory, get_memory_context
from pipeline.speech_to_text import transcribe_and_detect_lang
import os
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU*")
warnings.filterwarnings("ignore", message=".*GenerationMixin.*")
#warnings.filterwarnings("ignore", message=".*GPT2InferenceModel.*")

qdrant_path = get_env_var("QDRANT_HOST")
collection = get_env_var("COLLECTION_NAME")
csv_path = get_env_var("CSV_PATH")
realid = str(get_env_var("REALID", 101))  # You can override this in .env

model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 1: Load memory vectors from CSV (once at start)
#upload_csv_to_qdrant(csv_path, collection, qdrant_path)

last_query = ""

while True:
    query, lang = transcribe_and_detect_lang()

    if not query.strip():
        print("⚠️ No speech detected. Listening again...")
        continue #Skip the rest of the loop and start the next iteration immediately

    if query.strip() == last_query:
        print("⚠️ Duplicate input detected. Waiting for new speech...")
        continue

    last_query = query.strip()  # ✅ Update last spoken query

    # Save user query in memory
    store_memory(
        query,
        person_id=realid,
        role="user",
        memory_type="chat",
        collection_name=collection,
        qdrant_path=qdrant_path,
        language=lang
    )

    # Fetch memory context
    context = get_memory_context(str(realid), collection, qdrant_path)

    # Build full prompt
    prompt = f"{context}\n\nUser: {query}\nAssistant:"
    print(f'Prompt: {prompt}')

    response = call_gpt(prompt)
    print(f'GPT Response: {response}')

    # Save assistant response
    store_memory(
        response,
        person_id=realid,
        role="assistant",
        memory_type="chat",
        collection_name=collection,
        qdrant_path=qdrant_path,
        language=lang
    )
    print("🧠 Memory Updated")

    # Speak the response
    print("Speaking Response")
    speak(response)
    
    #speak(response, lang=lang)

