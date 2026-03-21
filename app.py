import streamlit as st
import requests

my_API_KEY = st.secrets["OPENROUTER_API_KEY"]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_tutor_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {my_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🧠 Build full conversation memory
    messages = [
        {"role": "system", "content": "You are a friendly tutor for students in rural India."}
    ]

    for chat in st.session_state.chat_history:
        role = "user" if chat.startswith("User") else "assistant"
        content = chat.replace("User: ", "").replace("AI: ", "")
        messages.append({"role": role, "content": content})

    # Add current prompt
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": "openai/gpt-4o-mini",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return str(result)

st.header("📚The Education Tutor for Remote India")
st.write("Helping students learn anytime, anywhere 💡")
if st.button("🧹Clear Chat"):
    st.session_state.chat_history = []

subject = st.selectbox("Select Subject:", ["Mathematics", "Science", "Social", "English", "Computer Basics"])
language = st.selectbox("Select Language:", ["English", "Telugu", "Hindi", "Tamil", "Malayalam", "Kannada", "Bengali", "Marathi", "Odia", "Gujarati", "Punjabi", "Nepali", "Assamese", "Manipuri (Meitei)", "Konkani"])

question = st.text_input("Ask your question:")

for chat in st.session_state.chat_history:
    if chat.startswith("User"):
        st.markdown(f"🧑 {chat}")
    else:
        st.markdown(f"🤖 {chat}")

if question and (
    "last_question" not in st.session_state 
    or st.session_state.last_question != question
):
    st.session_state.last_question = question

    st.session_state.chat_history.append(f"User: {question}")

    prompt = f"""
    You are a friendly tutor for students in rural India.

    Rules:
    - Explain in very simple words
    - Use real-life examples from villages or daily life
    - Answer ONLY in {language}
    - Keep answers short (3–6 lines)
    - If math, show step-by-step solution

    Subject: {subject}
    Question: {question}
    """

    with st.spinner("Thinking... 🤔"):
        answer = get_tutor_response(prompt)

    st.session_state.chat_history.append(f"AI: {answer}")

    st.rerun()