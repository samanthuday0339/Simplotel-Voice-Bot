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

## 🛠️ Tech Stack

| Component | Technology | Library Used |
| :--- | :--- | :--- |
| **Core Logic** | Python 3.10+ | `Jupyter Notebook` |
| **ASR (Speech-to-Text)** | OpenAI Whisper | `openai-whisper` |
| **NLU (Embeddings)** | Transformers | `sentence-transformers`, `torch` |
| **TTS (Text-to-Speech)** | Google TTS | `gTTS` |
| **Audio Capture** | PortAudio | `sounddevice`, `scipy` |
| **Backend** | SQL Database | `sqlite3` |
| **Analytics** | Data Science Stack | `pandas`, `seaborn`, `matplotlib` |

---

## ⚙️ Installation & Setup

### 1. System Prerequisites (Critical)
You must have **FFmpeg** installed for Whisper to process audio.

* **macOS:** `brew install ffmpeg`
* **Windows:** `choco install ffmpeg` (or add to PATH)
* **Ubuntu:** `sudo apt install ffmpeg`

### 2. Install Python Dependencies
Run the following command in your terminal to install all required libraries:

```bash
pip install numpy pandas matplotlib seaborn sounddevice scipy openai-whisper sentence-transformers gTTS torch


Here is the final, fully formatted README.md file code. I have fixed the syntax errors (like open code blocks) and formatted the lists and tables correctly.

You can copy the code block below and paste it directly into your GitHub repository's README.md file.

Markdown
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

## 🛠️ Tech Stack

| Component | Technology | Library Used |
| :--- | :--- | :--- |
| **Core Logic** | Python 3.10+ | `Jupyter Notebook` |
| **ASR (Speech-to-Text)** | OpenAI Whisper | `openai-whisper` |
| **NLU (Embeddings)** | Transformers | `sentence-transformers`, `torch` |
| **TTS (Text-to-Speech)** | Google TTS | `gTTS` |
| **Audio Capture** | PortAudio | `sounddevice`, `scipy` |
| **Backend** | SQL Database | `sqlite3` |
| **Analytics** | Data Science Stack | `pandas`, `seaborn`, `matplotlib` |

---

## ⚙️ Installation & Setup

### 1. System Prerequisites (Critical)
You must have **FFmpeg** installed for Whisper to process audio.

* **macOS:** `brew install ffmpeg`
* **Windows:** `choco install ffmpeg` (or add to PATH)
* **Ubuntu:** `sudo apt install ffmpeg`

### 2. Install Python Dependencies
Run the following command in your terminal to install all required libraries:

```bash
pip install numpy pandas matplotlib seaborn sounddevice scipy openai-whisper sentence-transformers gTTS torch
📖 How to Run
This project is delivered as a Jupyter Notebook (VOICEBOT.ipynb) for modular execution and visualization.

Step 1: Launch Jupyter

Open your terminal or command prompt and run:

Bash
jupyter notebook
Step 2: Open the Project

Navigate to the folder where you cloned the repo and open VOICEBOT.ipynb.

Step 3: Execute Cells in Order

Run Cell 1: Initializes imports & detects Hardware (MPS/CPU).

Run Cell 2: Connects to SQLite & seeds mock data.

Run Cell 3: Loads the NLU Transformer model (First run will download the model).

Run Cell 4: Initializes Microphone & Speaker systems.

Run Cell 5: Starts the Voice Bot Loop.

Step 4: Interact with the Bot

Wait for the voice prompt: "System online. Welcome back, Samantha."

Speak clearly when you see 🎤 LISTENING... in the output log.

To Finish: Say "Goodbye" to stop the bot and automatically generate the Analytics Graphs.

🤖 Supported Voice Commands
The NLU allows for natural variations, but here are the core intents supported:

Intent	Sample Phrases	Database Action
Check Balance	"How much money do I have?", "Check my balance", "Show funds"	SELECT balance FROM users
Book Hotel	"Book a room", "I want to make a reservation", "Reserve a suite"	INSERT INTO transactions
Support	"I need help", "Connect me to an agent"	Standard Response
Exit	"Goodbye", "Stop", "Exit system"	Triggers Analytics Dashboard
