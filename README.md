# JARVIS AI Assistant

A modular, voice-controlled AI assistant featuring a futuristic HUD interface, advanced automation skills, and a "living" responsiveness. Built with Python, PyQt6, and Groq's LLM engine.



## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- A [Groq API Key](https://console.groq.com/) for the LLM brain.

### Installation

1. **Clone the Repository**
   ```bash
   git clone <YOUR_REPO_URL>
   cd JARVIC
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This project relies on `PyQt6` for the GUI and `ultralytics` for vision.*

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_key_here
   # Add other keys as needed by specific skills
   ```

## 💻 Usage

**Standard Voice Mode (with GUI)**
```bash
python main.py
```
- The HUD will launch.
- Speak naturally to interact.
- Click the center reactor to **Pause/Resume** listening.

**Text-Only Mode**
```bash
python main.py --text
```
- Runs in the terminal without voice I/O. Ideal for debugging or quiet environments.

## 📂 Project Structure

- `core/`: The brain (Engine), voice processing, and skill registry.
- `gui/`: PyQt6 application logic and rendering.
- `skills/`: Individual capability modules.
- `assets/`: Images and resources.


