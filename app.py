import streamlit as st
import requests

API_KEY = "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"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Education Tutor App"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return str(result)

st.header("📚The Education Tutor for Remote India")
st.write("Helping students learn anytime, anywhere 💡")
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

subject = st.selectbox("Select Subject:",["Mathematics", "Science","Social", "English", "Computer Basics"])
language = st.selectbox("Select Language:",["English", "Telugu", "Hindi","Tamil","Malayalam","Kannada","Bengali","Marathi","Odia","Gujarati","Punjabi","Nepali","Assamese","Manipuri (Meitei)","Konkani"])

question = st.text_input("Ask your question:")
if question:
    st.session_state.chat_history.append(f"User: {question}")
    context = "\n".join(st.session_state.chat_history)
    prompt = f"""
    You are a friendly tutor for students in rural India.
    IMPORTANT:
    - Answer ONLY in {language}
    - Give the answer in the language selected only
    - Keep explanation very simple
    Subject: {subject}
    Question: {question}
    """
    answer = get_ai_response(prompt)

    st.session_state.chat_history.append(f"AI: {answer}")

    st.write("### 🤖 Tutor Response:")
    st.write(answer)