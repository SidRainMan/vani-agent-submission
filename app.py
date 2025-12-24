import streamlit as st
import os
import base64
from google.cloud import texttospeech
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from agent_graph import app_graph

# AUTHENTICATION
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
vertexai.init(location="us-central1")

st.set_page_config(page_title="VANI", layout="wide")
st.title("🗣️ VANI (Voice Agent for Native Interaction)")

# --- STATE SETUP ---
if "messages" not in st.session_state: st.session_state.messages = []
if "profile" not in st.session_state: st.session_state.profile = {}
if "last_audio" not in st.session_state: st.session_state.last_audio = None
if "conflict_active" not in st.session_state: st.session_state.conflict_active = False

# --- SIDEBAR WITH PLACEHOLDERS (The Fix) ---
with st.sidebar:
    st.header("🛠️ Agent Internals")
    
    # 1. Create Empty Slots (Placeholders)
    alert_box = st.empty()   # For Red Alert
    profile_box = st.empty() # For JSON Data
    
    # Initial Render (Shows current state before update)
    if st.session_state.conflict_active:
        alert_box.error("🚨 CONTRADICTION DETECTED!")
    profile_box.json(st.session_state.profile)
    
    if st.button("Reset Memory"):
        st.session_state.profile = {}
        st.session_state.messages = []
        st.session_state.conflict_active = False
        st.rerun()

# --- AUDIO FUNCTIONS ---
def synthesize_speech_google(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="bn-IN", name="bn-IN-Wavenet-A")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content

def autoplay_audio(audio_content):
    b64 = base64.b64encode(audio_content).decode()
    md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(md, unsafe_allow_html=True)

def transcribe_audio(audio_bytes):
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([
        Part.from_data(audio_bytes, mime_type="audio/wav"),
        "Transcribe this audio to text exactly. If it is Bengali, write in Bengali script."
    ])
    return response.text

# --- MAIN FLOW ---
# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Capture Audio
st.write("### 🎙️ Tap the Mic & Speak")
audio_value = st.audio_input("Record your voice")

if audio_value and audio_value != st.session_state.last_audio:
    st.session_state.last_audio = audio_value
    
    # 1. Transcribe
    with st.spinner("👂 Listening..."):
        audio_bytes = audio_value.read()
        user_text = transcribe_audio(audio_bytes)
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.write(user_text)

    # 2. Agent Brain
    with st.spinner("🧠 VANI is thinking..."):
        state_input = {
            "history": [m["content"] for m in st.session_state.messages if m["role"] == "user"],
            "user_profile": st.session_state.profile,
            "schemes_found": [],
            "next_step": "",
            "conflict_msg": None # Reset conflict check for this turn
        }
        
        result = app_graph.invoke(state_input)
        
        # Update State
        st.session_state.profile = result.get("user_profile", {})
        bot_reply = result["history"][-1]
        
        # Check Conflict for UI
        if result.get("conflict_msg"):
            st.session_state.conflict_active = True
        else:
            st.session_state.conflict_active = False
            
        # --- INSTANT UI UPDATE (The Fix) ---
        # We overwrite the placeholders immediately with new data
        profile_box.json(st.session_state.profile)
        
        if st.session_state.conflict_active:
            alert_box.error("🚨 CONTRADICTION DETECTED!")
        else:
            alert_box.empty() # Clear the alert if resolved
            
        # Add bot message
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.write(bot_reply)

    # 3. Speak
    audio_out = synthesize_speech_google(bot_reply)
    autoplay_audio(audio_out)