# 🎙️ Intelligent Voice Bot (Simplotel Assignment)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![AI](https://img.shields.io/badge/AI-OpenAI%20Whisper-green?logo=openai)
![NLU](https://img.shields.io/badge/NLU-Sentence%20Transformers-yellow?logo=huggingface)
![Status](https://img.shields.io/badge/Status-Assignment%20Completed-success)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

> **Assignment:** Software Engineer - Assignment 2 (Voice Bot Development)  
> **Submission Type:** Jupyter Notebook (`.ipynb`) Integration

An end-to-end AI voice assistant capable of handling real-time customer queries for banking and hospitality scenarios. Unlike simple rule-based bots, this project leverages **Semantic NLU** to understand user intent accurately, integrates a **SQLite Backend** for dynamic data fetching, and utilizes **OpenAI Whisper** for high-fidelity transcription.

---

## 🎯 Assignment Compliance Checklist

This project was built to strictly adhere to the requirements outlined in the **AI Intern Project Assignment** PDF.

| # | Requirement | Implementation Detail (in `VOICEBOT.ipynb`) | Status |
|:-:|:---|:---|:---:|
| **1** | **Speech-to-Text** | **Cell 4:** Integrated `openai-whisper` (Base Model) for robust transcription. | ✅ |
| **2** | **Natural Language Understanding** | **Cell 3:** Uses **Hugging Face Transformers** (`all-MiniLM-L6-v2`) for semantic similarity matching (Cosine Similarity) instead of keywords. | ✅ |
| **3** | **Response Generation** | **Cell 5:** Context-aware logic for Banking (`check_balance`) and Hospitality (`book_hotel`). | ✅ |
| **4** | **Text-to-Speech** | **Cell 4:** **Google TTS (gTTS)** with native OS playback drivers (`afplay` for Mac, `start` for Windows) for low-latency response. | ✅ |
| **5** | **Database Integration** | **Cell 2:** **SQLite3 Backend** that dynamically fetches user balances and logs transactions into `voice_bot_data.db`. | ✅ |
| **6** | **Analytics Dashboard** | **Cell 5:** **Seaborn/Pandas** dashboard that visualizes Latency and Intent Confidence after the session ends. | ✅ |

---

## 🚀 Key Features

### 1. 🧠 Semantic Intelligence (NLU)
The bot uses vector embeddings to understand meaning, not just words.
* *User says:* "I want to save a room." -> *Bot understands:* `book_hotel` (even though the word "book" wasn't used).
* *User says:* "What are my funds?" -> *Bot understands:* `check_balance`.

### 2. 💾 Dynamic SQL Backend
The system does not just chat; it performs actions using a local SQLite database.
* **Simulated User:** "Samantha" (ID: 101).
* **Capabilities:**
    * `get_user_details()`: Fetches real-time balance.
    * `log_transaction()`: Inserts reservation records into the DB.

### 3. ⚡ Hardware Acceleration
The code includes a hardware check (Cell 1) to automatically optimize inference:
* **Apple Silicon (M1/M2/M3):** Uses **MPS** (Metal Performance Shaders).
* **Standard PC:** Uses **CPU** or **CUDA** (if available).

### 4. 📊 Admin Analytics
Upon saying **"Goodbye"**, the bot shuts down and triggers a visual dashboard showing:
* **Latency Report:** How long each query took to process.
* **Confidence Score:** How sure the AI was about the user's intent.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Speech-to-Text** | OpenAI Whisper |
| **NLU** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Text-to-Speech** | gTTS |
| **Database** | SQLite |
| **Runtime** | Python + Jupyter Notebook |
| **Audio I/O** | `sounddevice`, `scipy` |
| **Analytics** | Pandas, Matplotlib, Seaborn |

---

## ⚙️ Installation & Setup

### 1. System Prerequisites (Critical)
You must have **FFmpeg** installed for Whisper to process audio.

* **macOS:** `brew install ffmpeg`
* **Windows:** `choco install ffmpeg` (or add to PATH)
* **Ubuntu:** `sudo apt install ffmpeg`

### 2. Clone Repository
```bash
git clone https://github.com/samanthuday0339/Simplotel-Voice-Bot.git
cd Simplotel-Voice-Bot
```

###  Install Python Dependencies

```bash
pip install numpy pandas matplotlib seaborn sounddevice scipy openai-whisper sentence-transformers gTTS torch
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
| **Cell 3** | Load NLU model |
| **Cell 4** | Whisper STT + TTS initialization |
| **Cell 5** | Voice bot loop |
| **Cell 6** | Analytics dashboard |

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

-----

## 6 👤 Author

**Samanth**

[GitHub Profile](https://github.com/samanthuday0339)

```
```
