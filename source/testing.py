import cv2
import mediapipe as mp
import pyautogui
import datetime
import random
import sys
import webbrowser
import threading
import os
import googletrans
from deepface import DeepFace
import subprocess

# Initialize Face Mesh and Translation Components
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
translator = googletrans.Translator()

# Screen dimensions
screen_w, screen_h = pyautogui.size()

# Motivational quotes
motivational_quotes = {
    "happy": [
        "Keep smiling, life is beautiful.",
        "Happiness is the key to success.",
        "Spread positivity and joy!"
    ],
    "sad": [
        "Tough times never last, but tough people do.",
        "Every day may not be good, but there's something good in every day.",
        "Believe in yourself and all that you are."
    ],
    "neutral": [
        "Stay focused and stay positive.",
        "Success is the sum of small efforts repeated day in and day out.",
        "Make today amazing!"
    ]
}

def display_message(message):
    """Display a message to the user."""
    print(f"System: {message}")

def get_user_input(prompt_message):
    """Get user input."""
    return input(f"User ({prompt_message}): ").strip().lower()

def greet_user():
    """Greet the user based on the time of day."""
    current_hour = int(datetime.datetime.now().hour)
    if current_hour < 12:
        display_message("Good Morning!")
    elif current_hour < 18:
        display_message("Good Afternoon!")
    else:
        display_message("Good Evening!")
    display_message("How may I assist you today?")

def translate_text(text, target_language="en"):
    """Translate text to the target language using Google Translate."""
    try:
        translated = translator.translate(text, dest=target_language).text
        return translated
    except Exception as e:
        display_message(f"Translation error: {e}")
        return "Translation unavailable."

def detect_emotion(frame):
    """Detect emotion from the given frame using DeepFace."""
    try:
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        return result["dominant_emotion"]
    except Exception as e:
        display_message(f"Emotion detection error: {e}")
        return "neutral"

def execute_command(command):
    """Function to execute commands based on user input."""
    if "translate" in command:
        display_message("Please type the text you want to translate.")
        text_to_translate = get_user_input("Text to translate")
        display_message("Which language should I translate to?")
        target_language = get_user_input("Target language (e.g., en, fr, es)")
        translated_text = translate_text(text_to_translate, target_language)
        display_message(f"The translation is: {translated_text}")

    elif "open google" in command:
        display_message("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "emergency contact" in command:
        display_message("Calling emergency contact...")
        # Replace with appropriate emergency action, e.g., sending a message or call.

    elif "daily planner" in command:
        display_message("What task should I add to your daily planner?")
        task = get_user_input("Task")
        with open("daily_planner.txt", "a") as planner:
            planner.write(f"{datetime.datetime.now()} - {task}\n")
        display_message("Task added to your daily planner.")

    elif "what is my emotion" in command:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            emotion = detect_emotion(frame)
            display_message(f"I think you are feeling {emotion}.")
            if emotion in motivational_quotes:
                display_message(random.choice(motivational_quotes[emotion]))
        else:
            display_message("I couldn't access your camera.")
        cam.release()

    elif "goodbye" in command or "stop" in command:
        display_message("Goodbye! Have a nice day.")
        sys.exit()

def typing_assistant():
    """Run the assistant in a typing-based manner."""
    greet_user()
    while True:
        command = get_user_input("Command")
        if command:
            execute_command(command)

def eye_controlled_mouse():
    """Eye-Controlled Mouse Functionality."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Camera not accessible.")

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            frame_h, frame_w, _ = frame.shape

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    if id == 1:
                        screen_x = int(screen_w * landmark.x)
                        screen_y = int(screen_h * landmark.y)
                        pyautogui.moveTo(screen_x, screen_y, duration=0.1)

                left_eye = [landmarks[145], landmarks[159]]
                if abs(left_eye[0].y - left_eye[1].y) < 0.004:
                    pyautogui.click()
                    pyautogui.sleep(1)
    except Exception as e:
        display_message(f"Error in eye-controlled mouse: {e}")
    finally:
        cam.release()

if __name__ == "__main__":
    threading.Thread(target=typing_assistant, daemon=True).start()
    eye_controlled_mouse()
