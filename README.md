# 🎙️ Intelligent Voice Bot (Simplotel Assignment)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI](https://img.shields.io/badge/AI-OpenAI%20Whisper-green)
![NLU](https://img.shields.io/badge/NLU-Sentence%20Transformers-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)

An AI-powered voice assistant capable of handling real-time customer queries for banking and hospitality scenarios. This project integrates state-of-the-art **Speech-to-Text**, **Semantic NLU**, and **Native Text-to-Speech** to create a seamless conversational experience.

---

## 🚀 Key Features

* **🗣️ High-Fidelity Speech Recognition:** Utilizes **OpenAI Whisper (Base Model)** for accurate transcription of user input, robust against background noise and accents.
* **🧠 Semantic Intent Understanding:** Implements **Hugging Face Transformers** (`all-MiniLM-L6-v2`) to understand user *intent* via vector embeddings (Cosine Similarity), rather than brittle keyword matching.
* **🔊 Native Neural TTS:** Generates human-like speech using **Google TTS (gTTS)** and plays it back natively on macOS (`afplay`) and Windows (`start`), ensuring high-quality audio output without browser widget errors.
* **💾 SQL Backend Integration:** Simulates a real-world system using **SQLite** to fetch account balances and log hotel reservations dynamically.
* **📊 Interaction Analytics:** Automatically generates a performance dashboard (Latency vs. Intent Confidence) using **Pandas** and **Seaborn** upon session termination.

---

## 🛠️ Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Speech-to-Text** | `openai-whisper` |
| **NLU / Embeddings** | `sentence-transformers`, `torch` |
| **Text-to-Speech** | `gTTS` (Google Text-to-Speech) |
| **Audio I/O** | `sounddevice`, `scipy`, `numpy` |
| **Data & Visualization** | `sqlite3`, `pandas`, `seaborn`, `matplotlib` |

---

## ⚙️ Installation & Setup

### 1. Prerequisites (Crucial)
This project uses **OpenAI Whisper**, which requires `ffmpeg` to be installed on your system to process audio files.

* **macOS (Homebrew):**
    ```bash
    brew install ffmpeg
    ```
* **Windows (Chocolatey):**
    ```bash
    choco install ffmpeg
    ```
* **Ubuntu/Debian:**
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Simplotel-Voice-Bot.git](https://github.com/YOUR_USERNAME/Simplotel-Voice-Bot.git)
cd Simplotel-Voice-Bot
