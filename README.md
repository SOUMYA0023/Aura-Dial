# ✨ Aura Dial — Hand-Tracked Tone Shifter 🎯

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-00D9FF?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

## 🌟 Overview

Aura Dial is an **interactive hand-gesture-controlled demo** that transforms how you interact with LLM prompts! 🤖 Using real-time webcam input and hand tracking, you can dynamically adjust the tone of AI responses by simply moving your finger across different "aura zones."

## ✨ Features

🖐️ **Hand Tracking** - Tracks your index fingertip using MediaPipe's advanced hand landmark detection

🎨 **Four Aura Blobs** - Visual representation of different tones:
- 📚 **Academic** - Scholarly and formal
- 💼 **Professional** - Business-appropriate
- 💬 **Conversational** - Casual and friendly  
- 🎮 **Playful** - Fun and creative

📝 **Dynamic Text Updates** - Real-time prompt panel showing tone-specific responses

👁️ **Visual Feedback** - Two white dots and connecting line track your finger position

🔊 **Text-to-Speech** - Optional voice feedback for tone changes (using pyttsx3)

## 🚀 Quick Start

### 📋 Requirements

- 🐍 Python 3.8 or higher
- 📷 Webcam access
- 💻 macOS, Windows, or Linux

### 📦 Installation

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/SOUMYA0023/Aura-Dial.git
cd Aura-Dial
```

2️⃣ **Create and activate virtual environment:**

**For macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**For Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

💡 **Troubleshooting:** If MediaPipe installation fails:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install mediapipe
```

### ▶️ Run

```bash
python main.py
```

## 🎮 How to Use

1. 👋 Hold your hand in front of the camera
2. ☝️ Point your index finger toward different colored aura zones
3. 👀 Watch the text panel update with tone-specific responses
4. 🔄 Move between zones to blend different tones
5. ⌨️ Press `q` or `Esc` to exit

## 🛠️ Technology Stack

- **MediaPipe** - Hand landmark detection and tracking
- **OpenCV** - Real-time video processing and visualization
- **NumPy** - Numerical computations and array operations
- **pyttsx3** - Text-to-speech synthesis (optional)

## 📂 Project Structure

```
Aura-Dial/
├── 📄 main.py              # Main application code
├── 📋 requirements.txt     # Python dependencies
├── 📖 README.md           # Project documentation
└── 📜 LICENSE             # MIT License
```

## 🔮 Future Enhancements

- 🤖 Live LLM API integration (Gemini, OpenAI, etc.)
- 🎛️ GUI for adjusting aura positions dynamically
- 🎙️ Multiple TTS voice profiles
- 🌈 Custom tone creation
- 📊 Tone usage analytics
- 🎨 Customizable visual themes

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/SOUMYA0023/Aura-Dial/issues).

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Soumya Suman Kar**
- 🐙 GitHub: [@SOUMYA0023](https://github.com/SOUMYA0023)
- 📧 Email: soumyasumankar23@gmail.com

## ⭐ Show Your Support

Give a ⭐️ if this project helped you or you found it interesting!

---

<div align="center">

**Made with ❤️ and Python**

</div>

