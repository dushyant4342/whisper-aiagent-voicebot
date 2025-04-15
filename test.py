import speech_recognition as sr

# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("🎙️ Say something...")
#     audio = r.listen(source, timeout=5, phrase_time_limit=5)
#     print("✅ Got audio")

# text = r.recognize_google(audio)
# print("🧠 Text:", text)


from utils.qdrant_client import search_by_realid
from utils.env_loader import get_env_var

realid = int(get_env_var("REALID"))
collection = get_env_var("COLLECTION_NAME")
path = get_env_var("QDRANT_PATH")

print("Searching memory...")
context = search_by_realid(realid, collection, path)
print("Found:", context)
