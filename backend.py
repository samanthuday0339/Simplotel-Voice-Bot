# backend.py
import sqlite3
import pandas as pd
import whisper
from transformers import pipeline
import spacy
from openai import OpenAI
import os
import time

# --- 1. Database Class ---
class BankingBackend:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT, name TEXT, balance REAL)''')
        self.cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", [('101', 'Samantha', 24500.50)])
        self.conn.commit()

    def get_user_details(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

# --- 2. NLU Class ---
class AdvancedNLU:
    def __init__(self):
        # Load models once to save memory
        self.classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
        self.nlp = spacy.load("en_core_web_sm")
        self.intent_labels = ["check_balance", "book_hotel", "support", "greeting"]

    def predict_intent(self, text):
        result = self.classifier(text, self.intent_labels)
        intent = result["labels"][0]
        doc = self.nlp(text)
        entities = {ent.label_: ent.text for ent in doc.ents}
        return intent, result["scores"][0], entities

# --- 3. Bot Logic ---
class VoiceBotLogic:
    def __init__(self, api_key=None):
        self.backend = BankingBackend()
        self.client = OpenAI(api_key=api_key) if api_key else None

    def generate_response(self, intent, entities, user_text):
        # ... [Copy your generate_response logic here] ...
        # Ensure fallback logic exists if self.client is None
        if intent == "check_balance":
            user = self.backend.get_user_details("101")
            return f"Your balance is ${user[2]:,.2f}."
        return f"Processed intent: {intent}"
