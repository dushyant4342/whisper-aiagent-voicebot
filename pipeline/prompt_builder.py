def build_prompt(user_input, context_docs):
    context_text = "\n".join(context_docs)
    system_instruction = (
        "You are a helpful assistant. Try to convince the user to pay their bill and always reply in the user's last used language. "
        "Be polite, empathetic, and persuasive and keep it very short in less than 20 words,please reply in Hinglish (like minimum not न्यूनतम or payment not चुकाने) whenever user said in hindi language. Make sure to speak EMI as E M EYE, Do not respond with customer name every time"
    )
    return f"{system_instruction}\n\nUser said: {user_input}\n\nContext:\n{context_text}\n\nAnswer:"
