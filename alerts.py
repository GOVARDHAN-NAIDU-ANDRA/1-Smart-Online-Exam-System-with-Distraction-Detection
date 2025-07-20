import pyttsx3
import threading
import time
import os
from playsound import playsound

# Initialize TTS engine (only used on server side for testing)
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # Adjust voice speed

def speak(text):
    """Speak the alert text using pyttsx3 (optional on server side)."""
    def _speak():
        engine.say(text)
        engine.runAndWait()

    t = threading.Thread(target=_speak)
    t.start()

def play_alarm():
    """Play an alarm sound from an mp3 file (e.g., alarm.mp3 in root)."""
    def _play():
        try:
            # Adjust path if needed
            alarm_path = os.path.join(os.getcwd(), 'alarm.mp3')
            if os.path.exists(alarm_path):
                playsound(alarm_path)
            else:
                print("🚫 Alarm file not found:", alarm_path)
        except Exception as e:
            print("Error playing alarm:", e)

    t = threading.Thread(target=_play)
    t.start()
