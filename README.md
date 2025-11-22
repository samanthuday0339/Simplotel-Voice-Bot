# 🎙️ Intelligent Voice Bot (Simplotel Assignment) - **Updated v2.0**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![AI](https://img.shields.io/badge/AI-OpenAI%20Whisper-green?logo=openai)
![NLU](https://img.shields.io/badge/NLU-Hugging%20Face%20Zero-Shot%20%2B%20spaCy-yellow?logo=huggingface)
![LLM](https://img.shields.io/badge/LLM-OpenAI%20GPT-4o-mini-purple?logo=openai)
![Status](https://img.shields.io/badge/Status-Assignment%20Completed%20(100%25%20Compliant)-success)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

> **Assignment:** Software Engineer - Assignment 2 (Voice Bot Development)  
> **Submission Type:** Jupyter Notebook (`.ipynb`) Integration  
> **Key Upgrades (v2.0):** Enhanced NLU with zero-shot intent classification + entity extraction (spaCy), dynamic GPT-4o-mini responses, error-rate tracking in analytics dashboard.

An end-to-end AI voice assistant capable of handling real-time customer queries for banking and hospitality scenarios. Unlike simple rule-based bots, this project leverages **Semantic NLU** (zero-shot classification + entity extraction) to understand user intent accurately, integrates a **SQLite Backend** for dynamic data fetching, and utilizes **OpenAI Whisper** for high-fidelity transcription. **New:** GPT-powered natural responses and full error-rate analytics.

---

## 🎥 Live Demo

Watch the voice bot perform real-time speech-to-text, intent detection with entities (e.g., "Book deluxe room tomorrow" → extracts room_type & DATE), dynamic GPT responses, and database logging:

[Demo Video Link](https://github.com/user-attachments/assets/8ac963cf-e133-44a3-b678-75268005016b)

> **Note:** The video demonstrates the full interaction loop, including hardware checks, dynamic SQL transactions, entity extraction, and the upgraded post-session analytics dashboard with error-rate pie chart.

## 📊 Analytics Dashboard (Upgraded)
<img width="855" height="754" alt="Screenshot 2025-11-22 at 10 50 36 AM" src="https://github.com/user-attachments/assets/fbfbb33f-06d5-456e-b011-1ae95b13d195" />

**New Features:** Confidence histogram, error-rate pie chart (tracks low-confidence/unknown intents), and entity logging.

## 🧩 System Architecture
<img width="296" height="598" alt="Screenshot 2025-11-22 at 11 01 04 AM" src="https://github.com/user-attachments/assets/1c1147b7-45b7-4f61-8194-5c31fa0d9020" />

---

## 🎯 Assignment Compliance Checklist

This project was built to strictly adhere to the requirements outlined in the **AI Intern Project Assignment** PDF. **v2.0 Upgrades:** Added entity extraction, GPT-based responses, and error-rate tracking for 100% alignment.

| # | Requirement | Implementation Detail (in `VOICEBOT.ipynb`) | Status |
|:-:|:---|:---|:---:|
| **1** | **Speech-to-Text** | **Cell 4:** Integrated `openai-whisper` (Tiny Model for low-latency) for robust transcription. | ✅ |
| **2** | **Natural Language Understanding** | **Cell 3:** Uses **Hugging Face Transformers** (`distilbert-base-uncased-mnli` for zero-shot intent classification) + **spaCy NER** for semantic similarity, intent recognition, and entity extraction (e.g., room_type, DATE). | ✅ **(Upgraded)** |
| **3** | **Response Generation** | **Cell 5:** Dynamic **GPT-4o-mini (OpenAI API)** for context-aware, natural responses; fallback rule-based logic for offline mode. Handles banking (`check_balance`) and hospitality (`book_hotel`). | ✅ **(Upgraded)** |
| **4** | **Text-to-Speech** | **Cell 4:** **Google TTS (gTTS)** with native OS playback (`afplay` for Mac, `start` for Windows, `mpg123` for Linux) for low-latency response. | ✅ |
| **5** | **Database Integration** | **Cell 2:** **SQLite3 Backend** that dynamically fetches user balances and logs transactions into in-memory DB (`voice_bot_data.db` optional). | ✅ |
| **6** | **Analytics Dashboard** | **Cell 5:** **Seaborn/Pandas** dashboard visualizes Latency, Confidence Scores, and **Error Rates** (low-confidence intents) after session ends. | ✅ **(Upgraded)** |

---

## 🚀 Key Features

### 1. 🧠 Advanced Semantic Intelligence (NLU)
The bot uses vector embeddings for intent classification and NER for entities—understands meaning beyond keywords.
* *User says:* "I want to save a room tomorrow" → *Bot understands:* `book_hotel` + entities `{room_type: 'Standard', DATE: 'tomorrow'}`.
* *User says:* "What are my funds?" → *Bot understands:* `check_balance` + dynamic balance fetch.

### 2. 💾 Dynamic SQL Backend
Performs real actions using SQLite.
* **Simulated User:** "Samantha" (ID: 101).
* **Capabilities:**
    * `get_user_details()`: Fetches real-time balance.
    * `log_transaction()`: Inserts reservation records.

### 3. ⚡ Hardware Acceleration & Stability
Optimized for low RAM: Whisper-tiny (~75MB), DistilBERT zero-shot (~260MB). No kernel crashes.

### 4. 📊 Enhanced Admin Analytics
On **"Goodbye"**, triggers dashboard showing:
* **Latency Report:** Query processing times.
* **Confidence Score:** NLU certainty.
* **Error Rate:** % of low-confidence/unknown intents (pie chart).
* **Entity Logs:** Extracted details (e.g., room types/dates).

### 5. 🤖 GPT-Powered Natural Responses
Uses OpenAI GPT-4o-mini for varied, human-like replies (e.g., "Great choice on the Deluxe room for tomorrow!"). Offline fallback ensures demo reliability.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Speech-to-Text** | OpenAI Whisper (Tiny) |
| **NLU** | Hugging Face DistilBERT (Zero-Shot) + spaCy NER |
| **Response Generation** | OpenAI GPT-4o-mini |
| **Text-to-Speech** | gTTS (Google TTS) |
| **Database** | SQLite |
| **Runtime** | Python + Jupyter Notebook |
| **Audio I/O** | `sounddevice`, `scipy` |
| **Analytics** | Pandas, Matplotlib, Seaborn |

---

## ⚙️ Installation & Setup

### 1. System Prerequisites
FFmpeg required for Whisper.

* **macOS:** `brew install ffmpeg`
* **Windows:** `choco install ffmpeg`
* **Ubuntu:** `sudo apt install ffmpeg mpg123`

### 2. Clone Repository
```bash
git clone https://github.com/samanthuday0339/Simplotel-Voice-Bot.git
cd Simplotel-Voice-Bot
```

###  Install Python Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

-----

## 3. How to Run the Project (Jupyter)

**Step 1 — Launch Notebook**

```bash
jupyter notebook
```

**Step 2 — Open**
`VOICEBOT.ipynb`

**Step 3 — Run All Cells in Order**

| Cell | Description |
| :--- | :--- |
| **Cell 1** | Hardware detection + imports |
| **Cell 2** | SQLite DB setup |
| **Cell 3** | Advanced NLU load (zero-shot + entities)|
| **Cell 4** | Whisper STT + gTTS init|
| **Cell 5** | Voice bot loop + dashboard|

Optional: Set OPENAI_API_KEY env var for GPT responses

-----

##  4 -🎤 Supported Voice Commands

| Intent | Example Phrases | DB Action |
| :--- | :--- | :--- |
| **Check Balance** | “Show my balance”, “What are my funds?” | SQL `SELECT` |
| **Book Hotel** | “Book a room”, “Reserve a suite” | SQL `INSERT` |
| **Support** | “I need help”, “Talk to support” | Static reply |
| **Exit** | “Goodbye”, “Stop” | Ends session + dashboard |

-----

## 5 📁 Project Structure

```text
📦 Simplotel-Voice-Bot
│
├── VOICEBOT.ipynb             # Main Jupyter Notebook
├── voice_bot_data.db          # SQLite DB (auto-generated)
├── sample_audio/              # Test audio files
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```
------

## 6 👤 Author

**Samanth**

[GitHub Profile](https://github.com/samanthuday0339)

```
```
