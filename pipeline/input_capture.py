import speech_recognition as sr

def capture_audio_and_save(filepath="recorded.wav"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening (timeout=5s, limit=10s)...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected.")
            return None

    with open(filepath, "wb") as f:
        f.write(audio.get_wav_data())
    
    return filepath



# import speech_recognition as sr

# def capture_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎤 Listening (timeout=5s, limit=10s)...")
#         try:
#             audio = r.listen(source, timeout=5, phrase_time_limit=5)
#             print("✅ Audio captured.")
#         except sr.WaitTimeoutError:
#             print("⏱️ No speech detected. Try again.")
#             return ""

#     try:
#         text = r.recognize_google(audio)
#         print("🧠 Recognized:", text)
#         return text
#     except Exception as e:
#         print("❌ Error recognizing speech:", e)
#         return ""



# def capture_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         return r.recognize_google(audio)
#     except Exception as e:
#         print("Error:", e)
#         return ""


# def capture_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         try:
#             audio = r.listen(source, timeout=5, phrase_time_limit=10)
#         except sr.WaitTimeoutError:
#             print("⏱️ No speech detected. Try again.")
#             return ""
#     try:
#         return r.recognize_google(audio)
#     except Exception as e:
#         print("❌ Recognition error:", e)
#         return ""