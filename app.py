import uuid

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Academic Agent", page_icon="📚")
st.title("📚 AI Academic Agent")


# ---------- 1. Session state (survives reruns) ----------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- 2. Functions that call the backend ----------
@st.cache_data(ttl=60)
def get_personas():
    response = requests.get(f"{API_URL}/personas", timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=60)
def get_documents():
    response = requests.get(f"{API_URL}/documents", timeout=10)
    response.raise_for_status()
    return response.json()["documents"]


def send_message(message: str, persona: str) -> dict:
    response = requests.post(
        f"{API_URL}/chat",
        json={
            "message": message,
            "thread_id": st.session_state.thread_id,
            "persona": persona,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


# ---------- 3. Sidebar ----------
with st.sidebar:
    st.header("Settings")

    try:
        personas = get_personas()
        documents = get_documents()
    except requests.exceptions.RequestException:
        st.error("Can't reach the backend. Is uvicorn running?")
        st.stop()

    persona = st.selectbox(
        "Persona",
        options=list(personas.keys()),
        format_func=lambda key: f"{key}: {personas[key][:45]}...",
    )

    st.subheader("Your documents")
    for doc in documents:
        st.write(f"• {doc}")

    if st.button("New chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()


# ---------- 4. Show the chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tools_used"):
            st.caption("🔧 Tools used: " + ", ".join(msg["tools_used"]))


# ---------- 5. Handle a new message ----------
prompt = st.chat_input("Ask about your notes...")

if prompt:
    # show the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # get and show the agent's answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = send_message(prompt, persona)
                answer = result["answer"]
                tools_used = result["tools_used"]
            except requests.exceptions.RequestException as e:
                answer = f"⚠️ Error talking to the backend: {e}"
                tools_used = []

        st.markdown(answer)
        if tools_used:
            st.caption("🔧 Tools used: " + ", ".join(tools_used))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "tools_used": tools_used}
    )