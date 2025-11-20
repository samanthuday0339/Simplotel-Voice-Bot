# 🎙️ Intelligent Voice Bot for Customer Interaction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI](https://img.shields.io/badge/AI-OpenAI%20Whisper-green)
![NLU](https://img.shields.io/badge/NLU-Hugging%20Face-yellow)

An AI-powered voice assistant capable of handling banking and hospitality queries in real-time. This project integrates state-of-the-art Speech-to-Text, Semantic Natural Language Understanding (NLU), and Neural Text-to-Speech to create a seamless conversational experience.

---

## 🚀 Key Features

* **🗣️ High-Fidelity Speech Recognition:** Utilizes **OpenAI Whisper (Base Model)** for accurate transcription of user input, robust against background noise.
* **🧠 Semantic Understanding:** Implements **Hugging Face Transformers** (`all-MiniLM-L6-v2`) to understand user *intent* via vector embeddings, rather than brittle keyword matching.
* **🔊 Native Neural TTS:** Generates human-like speech using **Google TTS (gTTS)** and plays it back natively on macOS (`afplay`) and Windows (`start`), bypassing browser widget limitations.
* **💾 SQL Backend Integration:** Simulates a real-world banking system using **SQLite** to fetch account balances and log transactions dynamically.
* **📊 Interaction Analytics:** Automatically generates a performance dashboard (Latency vs. Intent Confidence) using **Pandas** and **Seaborn** upon session termination.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Speech-to-Text:** `openai-whisper`
* **NLU:** `sentence-transformers`
* **Text-to-Speech:** `gTTS`
* **Audio Processing:** `sounddevice`, `scipy`, `numpy`
* **Data & Viz:** `pandas`, `matplotlib`, `seaborn`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Simplotel-Voice-Bot.git](https://github.com/YOUR_USERNAME/Simplotel-Voice-Bot.git)
cd Simplotel-Voice-Bot
