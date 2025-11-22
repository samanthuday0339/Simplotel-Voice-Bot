import sqlite3
import json
import os
from openai import OpenAI

# --- 1. Database Class (Lightweight SQLite) ---
class BankingBackend:
    def __init__(self):
        # check_same_thread=False is required for Streamlit
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
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


# --- 2. NLU Class (GPT-4o-mini Powered) ---
class AdvancedNLU:
    def __init__(self, client=None):
        self.client = client

    def predict_intent(self, text, client=None):
        """
        Uses GPT-4o-mini to extract Intent and Entities in one shot.
        This replaces the heavy local 'transformers' model.
        """
        # Use the client passed in method or fall back to class client
        active_client = client or self.client
        
        if not active_client:
            # Fallback if no API key is available yet
            return "unknown", 0.0, {}

        system_prompt = """
        You are an NLU engine. Analyze the user's text.
        1. Detect Intent: 'check_balance', 'book_hotel', 'support', 'greeting', 'goodbye'.
        2. Extract Entities: 'DATE', 'room_type', 'MONEY'.
        3. Return strictly valid JSON: {"intent": "...", "entities": {...}}
        """

        try:
            response = active_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            # Parse JSON response
            data = json.loads(response.choices[0].message.content)
            intent = data.get("intent", "unknown")
            entities = data.get("entities", {})
            
            return intent, 1.0, entities

        except Exception as e:
            print(f"NLU Error: {e}")
            return "unknown", 0.0, {}


# --- 3. Main Bot Engine ---
class VoiceBot:
    def __init__(self, api_key=None):
        self.backend = BankingBackend()
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if api_key else None
        # Initialize NLU with the same client
        self.nlu = AdvancedNLU(self.client)

    def update_api_key(self, api_key):
        """Updates the API key dynamically from the UI"""
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.nlu.client = self.client

    def transcribe_audio(self, file_path):
        """Uses OpenAI Whisper API (Fast & Light)"""
        if not self.client:
            return "⚠️ Error: OpenAI API Key is missing."

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
        """Generates response using GPT-4o-mini or Logic Fallback"""
        user_details = self.backend.get_user_details("101")
        name = user_details[1] if user_details else "User"
        balance = user_details[2] if user_details else 0.0

        # 1. Rule-Based Handling (Fastest)
        if intent == "check_balance":
            return f"Hi {name}, your current balance is ${balance:,.2f}."
        
        # 2. GPT-4o-mini Response (Natural)
        if self.client:
            try:
                system_prompt = f"""
                You are Aria, a helpful banking assistant.
                User Info: Name={name}, Balance=${balance}.
                Current Intent: {intent}. Entities: {entities}.
                Reply in 1 short, friendly sentence.
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
                pass 

        # 3. Fallback if GPT fails
        if intent == "book_hotel":
            return f"I can help with that. I've noted your request for a {entities.get('room_type', 'room')}."
        elif intent == "goodbye":
            return "Goodbye! Have a wonderful day."
            
        return "I didn't quite catch that. Could you say it again?"
