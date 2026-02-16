import os
import sys
import argparse
import threading 
import time
import subprocess
from dotenv import load_dotenv

# Load OS-specific modules
if os.name == 'nt':  # Windows
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Windows"))
else:
    sys.path.insert(0, os.path.dirname(__file__))

from core.voice import speak, listen
from core.registry import SkillRegistry
from core.engine import JarvisEngine

# Load Env
load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    print("Error: GROQ_API_KEY not found.")
    sys.exit(1)


def jarvis_loop(pause_event, registry, args):
    """
    Main loop for JARVIS. If args.voice is True, uses voice I/O; otherwise uses text I/O.
    """
    jarvis = JarvisEngine(registry)

    if args.voice:
        speak("Jarvis Online. Ready for command.")
    else:
        print("JARVIS: Jarvis Online. Ready for command (Text Mode).")

    while True:
        if pause_event.is_set():
            time.sleep(0.5)
            continue

        if args.voice:
            user_query = listen()
        else:
            try:
                user_query = input("YOU: ").lower()
            except EOFError:
                break

        if pause_event.is_set():
            continue

        if user_query == "none" or not user_query:
            continue

        if "quit" in user_query:
            print("Shutting down JARVIS loop...")
            if args.voice:
                speak("Shutting down.")
            break

        direct_commands = [
            "open", "volume", "search", "create", "write", "read", "make",
            "who", "what", "when", "where", "how", "why", "thank", "hello"
        ]
        is_direct = any(cmd in user_query for cmd in direct_commands)

        if "jarvis" not in user_query and not is_direct:
            print(f"Ignored: {user_query}")
            continue

        clean_query = user_query.replace("jarvis", "").strip()

        try:
            print(f"Thinking: {clean_query}")
            response = jarvis.run_conversation(clean_query)
            if pause_event.is_set():
                continue

            if response:
                if args.voice:
                    speak(response)
                else:
                    print(f"JARVIS: {response}")
        except Exception as e:
            print(f"Main Loop Error: {e}")
            if args.voice:
                speak("System error.")
            else:
                print("JARVIS: System error.")


def main():
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant")
    # Default to text mode; enable voice with --voice
    parser.add_argument("--voice", action="store_true", help="Run in voice mode (enable voice I/O)")
    args = parser.parse_args()

    # Only auto-open browser for GUI/voice usage to avoid interfering with CLI
    if args.voice:
        try:
            subprocess.Popen("start brave", shell=True)
        except Exception:
            pass

    pause_event = threading.Event()
    context = {"pause_event": pause_event}

    registry = SkillRegistry()
    # Load skills from OS-specific directory if on Windows, otherwise use default
    if os.name == 'nt':  # Windows
        skills_dir = os.path.join(os.path.dirname(__file__), "Windows", "skills")
        registry.load_skills(skills_dir)  # Windows registry doesn't support context param
    else:
        skills_dir = os.path.join(os.path.dirname(__file__), "skills")
        registry.load_skills(skills_dir, context=context)

    # For text mode, no GUI; run loop in main thread
    if not args.voice:
        jarvis_loop(pause_event, registry, args)
        return

    # Voice mode: try GUI; fallback to console on failure
    try:
        from gui.app import run_gui as run_gui_app
        t = threading.Thread(target=jarvis_loop, args=(pause_event, registry, args), daemon=True)
        t.start()
        run_gui_app(pause_event)
    except Exception as e:
        print(f"GUI unavailable ({e}). Falling back to console mode.")
        jarvis_loop(pause_event, registry, argparse.Namespace(voice=True))


if __name__ == "__main__":
    main()
