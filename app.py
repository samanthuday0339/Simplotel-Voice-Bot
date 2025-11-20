import streamlit as st
import pandas as pd
import numpy as np
import time
import sqlite3
import os
import io
import re
from datetime import datetime

# Import the necessary component for microphone input
from streamlit_mic_recorder import mic_recorder 

# ML Libraries
from sentence_transformers import SentenceTransformer
from gtts import gTTS
import whisper

# --- CONFIGURATION ---
DB_PATH = 'voice_bot_data.db'
# Note: Whisper requires a lot of memory. Using the base model for faster deployment.
WHISPER_MODEL = "base" 
NLU_MODEL = 'all-MiniLM-L6-v2'
SIMILARITY_THRESHOLD = 0.65

# --- HELPER CLASSES ---

class DBManager:
    """Handles SQLite database connections and transactions."""
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Creates tables if they don't exist and seeds sample data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Accounts table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                balance REAL
            )
            """)
            
            # Reservations table (for hotel scenario)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                room_type TEXT,
                check_in TEXT
            )
            """)

            # Seed sample data using INSERT OR IGNORE
            accounts_data = [
                ('12345678', 54200.75),
                ('98765432', 1200.00),
            ]
            # FIX APPLIED HERE: Using INSERT OR IGNORE
            cursor.executemany("INSERT OR IGNORE INTO accounts VALUES (?, ?)", accounts_data)
            
            conn.commit()
            
    def get_account_balance(self, account_id):
        """Fetches the balance for a given account ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def create_hotel_reservation(self, name, room_type, check_in):
        """Logs a new hotel reservation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reservations (customer_name, room_type, check_in) VALUES (?, ?, ?)", 
                           (name, room_type, check_in))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_interactions(self):
        """Returns all logged interactions from the log stored in session state."""
        return st.session_state.get('interaction_log', [])


class NlUEngine:
    """Uses Sentence-Transformers for semantic intent matching."""
    def __init__(self, model_name, db_manager):
        self.model = SentenceTransformer(model_name)
        self.db = db_manager
        self.intents = self._define_intents()
        self.intent_labels = list(self.intents.keys())
        self.intent_embeddings = self.model.encode(self.intent_labels)

    def _define_intents(self):
        """Defines intent keywords and their response handlers."""
        return {
            "Greeting": self.handle_greeting,
            "CheckBalance": self.handle_check_balance,
            "HotelReservation": self.handle_hotel_reservation,
            "ThankYou": self.handle_thank_you,
            "Goodbye": self.handle_goodbye,
            "GeneralQuery": self.handle_general_query # Fallback
        }

    def get_intent(self, query):
        """Calculates the semantic similarity to find the best matching intent."""
        query_embedding = self.model.encode(query)
        # Calculate cosine similarity (dot product of normalized vectors)
        similarities = np.dot(query_embedding, self.intent_embeddings.T)
        
        best_match_index = np.argmax(similarities)
        confidence = similarities[best_match_index]
        best_intent = self.intent_labels[best_match_index]
        
        if confidence < SIMILARITY_THRESHOLD:
            return "GeneralQuery", 0.0

        return best_intent, confidence
    
    def get_response(self, query):
        """Routes the query to the appropriate handler and returns the response."""
        intent, confidence = self.get_intent(query)
        
        # Log the interaction
        if 'interaction_log' not in st.session_state:
            st.session_state['interaction_log'] = []
            
        st.session_state['interaction_log'].append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User Query": query,
            "Detected Intent": intent,
            "Confidence": f"{confidence:.2f}",
            "Latency (sec)": 0.0 # Will be updated in the main loop
        })

        handler = self.intents.get(intent)
        if handler:
            return handler(query), intent, confidence
        
        return "I apologize, I didn't understand that. Can you please rephrase your request?", "Unknown", 0.0

    # --- INTENT HANDLERS ---
    
    def handle_greeting(self, query):
        return "Hello! Thank you for calling. I can check your bank balance or help you make a hotel reservation. How may I assist you?"

    def handle_thank_you(self, query):
        return "You're very welcome! Is there anything else I can help you with today?"

    def handle_goodbye(self, query):
        return "Thank you for using our service. Have a wonderful day! Goodbye."

    def handle_check_balance(self, query):
        # Simple entity extraction for account ID (looking for 8 consecutive digits)
        account_id_match = re.search(r'\b\d{8}\b', query)
        if not account_id_match:
            return "I need your 8-digit account ID to check your balance. Please state it clearly."

        account_id = account_id_match.group(0)
        balance = self.db.get_account_balance(account_id)

        if balance is not None:
            return f"The current balance for account number ending in {account_id[-4:]} is ${balance:,.2f}."
        else:
            return f"I could not find an account with the ID {account_id}."

    def handle_hotel_reservation(self, query):
        # Simple entity extraction for name and date
        name_match = re.search(r'(for|under)\s+the\s+name\s+of\s+(\w+)', query, re.IGNORECASE)
        date_match = re.search(r'\b(today|tomorrow|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))', query, re.IGNORECASE)
        room_type = "Standard" # Simplification for this demo

        name = name_match.group(2) if name_match else "Guest"
        check_in = date_match.group(0) if date_match else "an unspecified date"

        reservation_id = self.db.create_hotel_reservation(name, room_type, check_in)

        return (f"I have successfully booked a {room_type} room for {name}, checking in on {check_in}. "
                f"Your reservation ID is {reservation_id}.")
        
    def handle_general_query(self, query):
        return "I am a specialized bot for bank and hotel queries. I can check your account balance or make a reservation. Can you ask me about one of those topics?"


class VoiceBot:
    """The main application engine combining STT, NLU, and TTS."""
    def __init__(self, db_manager, nlu_engine):
        self.db = db_manager
        self.nlu_engine = nlu_engine
        
        # Initialize Whisper (only once)
        st.info(f"Loading Whisper model: {WHISPER_MODEL} and NLU model: {NLU_MODEL}...")
        self.stt_model = whisper.load_model(WHISPER_MODEL)
        st.success("Models loaded successfully!")

    def transcribe_audio(self, audio_data):
        """Transcribes the audio data buffer using OpenAI Whisper."""
        try:
            # Write the raw bytes data to a temporary file
            temp_path = "temp_recorded_audio.wav"
            with open(temp_path, "wb") as f:
                f.write(audio_data)

            # Use whisper to transcribe the temporary file
            result = self.stt_model.transcribe(temp_path)
            
            # Clean up the temporary file
            os.remove(temp_path)
            
            return result["text"]
        except Exception as e:
            st.error(f"Error during transcription: {e}")
            return None

# --- STREAMLIT UI/ENTRY POINT ---

# Initialize state variables
if 'db' not in st.session_state:
    st.session_state['db'] = DBManager(DB_PATH)
if 'nlu' not in st.session_state:
    st.session_state['nlu'] = NlUEngine(NLU_MODEL, st.session_state['db'])

@st.cache_resource
def initialize_bot():
    """Initializes the heavy Whisper model and VoiceBot class once."""
    return VoiceBot(st.session_state['db'], st.session_state['nlu'])

# Main function to run the Streamlit App
def main():
    st.set_page_config(layout="wide")
    st.title("🎙️ AI Voice Bot (Simplotel Assignment)")
    st.markdown("---")

    # Sidebar for Analytics
    with st.sidebar:
        st.header("Interaction Analytics")
        if st.button("Generate/Update Dashboard"):
            generate_dashboard()
        
        st.markdown("---")
        st.caption(f"DB Path: `{DB_PATH}`")
        st.caption(f"NLU Model: `{NLU_MODEL}`")
        st.caption(f"Whisper Model: `{WHISPER_MODEL}`")


    # Initialize the VoiceBot (only loads heavy models once)
    bot = initialize_bot()

    st.subheader("1. Record your Query")
    
    # Use mic_recorder for direct microphone input
    # 'bytes' returns the audio data as a bytes object after recording stops
    audio_input = mic_recorder(
        start_prompt="Start Recording", 
        stop_prompt="Stop Recording",
        key='mic_recorder_key',
        just_once=True,
        format='wav',
        callback=None
    )
    
    # Optional: Allow file upload as a fallback
    st.markdown("---")
    st.subheader("... or Upload a File (Fallback)")
    uploaded_file = st.file_uploader(
        "Upload a voice file (.wav, .mp3)", 
        type=['wav', 'mp3']
    )

    audio_data = None
    if audio_input and audio_input['bytes']:
        audio_data = audio_input['bytes']
    elif uploaded_file is not None:
        # FIX APPLIED HERE: Use the robust .read() method to get all file contents as bytes.
        uploaded_file.seek(0)
        audio_data = uploaded_file.read()


    if audio_data is not None:
        
        # --- 2. TRANSCRIPTION (STT) ---
        start_time = time.time()
        with st.spinner("Transcribing audio using Whisper..."):
            # Pass the raw bytes/buffer to the transcribe function
            transcribed_text = bot.transcribe_audio(audio_data)
        stt_latency = time.time() - start_time
        
        if transcribed_text:
            st.info(f"**Transcription:** {transcribed_text}")
            
            # --- 3. NLU & RESPONSE GENERATION ---
            start_time = time.time()
            with st.spinner("Analyzing intent and generating response..."):
                response_text, intent, confidence = bot.nlu_engine.get_response(transcribed_text)
            nlu_latency = time.time() - start_time
            
            # Update the latency in the last logged interaction
            # Ensure log exists before accessing index -1
            if st.session_state.get('interaction_log'):
                log = st.session_state['interaction_log'][-1]
                log['Latency (sec)'] = f"{stt_latency + nlu_latency:.2f}"
            
            st.markdown("### 🤖 Bot Response")
            st.success(response_text)
            st.markdown(f"**Intent Detected:** `{intent}` (Confidence: {confidence:.2f})")
            
            # --- 4. TEXT-TO-SPEECH (TTS) ---
            try:
                with st.spinner("Generating audio response (TTS)..."):
                    # Use gTTS to create the MP3 file in memory
                    tts = gTTS(text=response_text, lang='en')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)

                # Use st.audio to play the response in the browser
                st.audio(audio_fp.getvalue(), format="audio/mp3", autoplay=True)
                
            except Exception as e:
                st.error(f"TTS Error: Could not generate audio. Details: {e}")
        else:
            st.error("Could not transcribe the audio. Please try another recording or file.")


def generate_dashboard():
    """Generates and displays the performance dashboard."""
    interactions = st.session_state['db'].get_all_interactions()
    if not interactions:
        st.sidebar.warning("No interactions logged yet to generate a dashboard.")
        return

    df = pd.DataFrame(interactions)
    df['Latency (sec)'] = pd.to_numeric(df['Latency (sec)'], errors='coerce')
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce')

    st.sidebar.markdown("---")
    st.sidebar.subheader("Dashboard Results")

    # Display raw data
    st.sidebar.dataframe(df[['Timestamp', 'User Query', 'Detected Intent', 'Confidence', 'Latency (sec)']], height=200)

    # Simple aggregated metrics
    avg_latency = df['Latency (sec)'].mean()
    avg_confidence = df['Confidence'].mean()
    
    st.sidebar.metric("Average Latency", f"{avg_latency:.2f} s")
    st.sidebar.metric("Average Confidence", f"{avg_confidence:.2f}")

    # Plot 1: Latency by Intent
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=df, x='Detected Intent', y='Latency (sec)', ax=ax1, palette='viridis')
    ax1.set_title('Latency Performance by Detected Intent')
    ax1.set_xlabel('Intent')
    ax1.set_ylabel('Latency (seconds)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.sidebar.pyplot(fig1)

    # Plot 2: Confidence vs. Latency Scatter
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=df, x='Confidence', y='Latency (sec)', hue='Detected Intent', ax=ax2, palette='Set1', s=100)
    ax2.set_title('Confidence vs. Latency')
    ax2.set_xlabel('NLU Confidence')
    ax2.set_ylabel('Total Latency (seconds)')
    plt.tight_layout()
    st.sidebar.pyplot(fig2)


if __name__ == '__main__':
    main()
