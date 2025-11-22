# app.py
import streamlit as st
import os
from backend import AdvancedNLU, VoiceBotLogic
import whisper

# Page Config
st.set_page_config(page_title="Voice Banking Bot", page_icon="🎙️")

# --- 1. Load Models (Cached) ---
@st.cache_resource
def load_models():
    nlu = AdvancedNLU()
    whisper_model = whisper.load_model("tiny")
    return nlu, whisper_model

nlu, whisper_model = load_models()

# --- 2. API Key Setup ---
api_key = st.secrets.get("OPENAI_API_KEY", None)
bot = VoiceBotLogic(api_key=api_key)

st.title("🎙️ AI Banking Voice Bot")

# --- 3. Audio Input (Browser Native) ---
# This widget records audio directly in the browser
audio_value = st.audio_input("Record your voice command")

if audio_value:
    st.audio(audio_value)
    
    with st.spinner("Transcribing..."):
        # Save temp file for Whisper
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_value.read())
        
        # Transcribe
        result = whisper_model.transcribe("temp_audio.wav")
        text = result["text"]
        st.success(f"You said: {text}")

    # Process Intent
    intent, conf, entities = nlu.predict_intent(text)
    
    # Display Analysis
    with st.expander("Analysis Details"):
        st.write(f"**Intent:** {intent} ({conf:.2f})")
        st.write(f"**Entities:** {entities}")

    # Generate Response
    response = bot.generate_response(intent, entities, text)
    st.chat_message("assistant").write(response)

    # Cleanup
    os.remove("temp_audio.wav")
