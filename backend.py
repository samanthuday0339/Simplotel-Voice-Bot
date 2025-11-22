import sqlite3
import spacy
from transformers import pipeline
from openai import OpenAI
import os

# --- 1. Database Class (Lightweight SQLite) ---
class BankingBackend:
    def __init__(self):
        # check_same_thread=False is needed for Streamlit's multi-threaded environment
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        # Initialize with dummy data for the demo
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                balance REAL
            )
        ''')
        # Seed Mock Data
        data = [('101', 'Samantha', 24500.50), ('102', 'Guest', 0.00)]
        self.cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", data)
        self.conn.commit()

    def get_user_details(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def log_transaction(self, user_id, service_type):
        # Simulating a write operation
        return f"Confirmed. {service_type} has been logged for User {user_id}."


# --- 2. NLU Class (Local Processing) ---
class AdvancedNLU:
    def __init__(self):
        print("🧠 Loading NLU Models...")
        # Zero-shot classification (Runs on CPU, might be slow on Free Tier but works)
        self.classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli"
        )
        
        # Entity Extraction (SpaCy - Lightweight)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model isn't linked correctly, though requirements.txt url fixes this
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

        self.intent_labels = ["check_balance", "book_hotel", "support", "greeting", "goodbye"]

    def predict_intent(self, text):
        # 1. Detect Intent
        result = self.classifier(text, self.intent_labels)
        intent = result["labels"][0]
        confidence = result["scores"][0]

        # 2. Extract Entities
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME", "MONEY", "GPE"]:
                entities[ent.label_] = ent.text
        
        # Custom keyword extraction for hotels
        text_lower = text.lower()
        room_types = {"suite": "Suite", "deluxe": "Deluxe", "standard": "Standard"}
        for key, val in room_types.items():
            if key in text_lower:
                entities["room_type"] = val

        return intent, confidence, entities


# --- 3. Main Bot Engine (API Audio + Logic) ---
class VoiceBot:
    def __init__(self, api_key=None):
        self.backend = BankingBackend()
        # We need the API key for both Transcription (Audio) and Chat (Text)
        self.api_key = api_key
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def transcribe_audio(self, file_path):
        """
        Uses OpenAI API (Whisper-1) to transcribe audio.
        This is much lighter than running local Whisper on Streamlit Cloud.
        """
        if not self.client:
            return "Error: OpenAI API Key missing."

        try:
            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            return f"Transcription Failed: {str(e)}"

    def generate_response(self, intent, entities, user_text):
        """
        Generates a response using GPT-4o-mini (if available) or Rule-Based Fallback.
        """
        user_id = "101"
        user_details = self.backend.get_user_details(user_id)
        name = user_details[1] if user_details else "User"
        balance = user_details[2] if user_details else 0.0

        # OPTION A: GPT-4o-mini Response (Natural)
        if self.client:
            try:
                system_prompt = f"""
                You are Aria, a banking assistant. 
                User: {name}, Balance: ${balance}. 
                Current Intent: {intent}. Entities: {entities}.
                Reply briefly (1 sentence).
                """
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ]
                )
                return response.choices[0].message.content
            except Exception:
                pass # Fail silently to fallback

        # OPTION B: Rule-Based Fallback (Offline Mode)
        if intent == "check_balance":
            return f"Your current balance is ${balance:,.2f}."
        elif intent == "book_hotel":
            room = entities.get("room_type", "room")
            date = entities.get("DATE", "tonight")
            return f"I have booked a {room} for {date}."
        elif intent == "greeting":
            return f"Hello {name}! How can I help you with your banking today?"
        elif intent == "goodbye":
            return "Goodbye! Have a great day."
        
        return "I'm not sure I understood. Could you say that again?"
