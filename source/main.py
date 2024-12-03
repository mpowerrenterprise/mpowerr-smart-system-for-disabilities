import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import datetime
import random
import sys
import webbrowser
import threading
import os
import googletrans
from deepface import DeepFace
import subprocess

# Initialize Face Mesh, Speech, and Translation Components
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = googletrans.Translator()

# Voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

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

def speak(audio):
    """Function to speak a given text."""
    print("Assistant:", audio)
    engine.say(audio)
    engine.runAndWait()


def greet_user():
    """Greet the user based on the time of day."""
    current_hour = int(datetime.datetime.now().hour)
    if current_hour < 12:
        speak("Good Morning!")
    elif current_hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How may I assist you today?")


def listen_command():
    """Function to listen for a command and return it as text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("User:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble with the speech service.")
            return ""


def translate_text(text, target_language="en"):
    """Translate text to the target language using Google Translate."""
    try:
        translated = translator.translate(text, dest=target_language).text
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation unavailable."


def detect_emotion(frame):
    """Detect emotion from the given frame using DeepFace."""
    try:
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        return result["dominant_emotion"]
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return "neutral"


def execute_command(command):
    """Function to execute commands based on recognized speech."""
    if "translate" in command:
        speak("Please say the text you want to translate.")
        text_to_translate = listen_command()
        speak("Which language should I translate to?")
        target_language = listen_command()
        translated_text = translate_text(text_to_translate, target_language)
        speak(f"The translation is: {translated_text}")

    elif "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "emergency contact" in command:
        speak("Calling emergency contact...")
        # Replace with appropriate emergency action, e.g., sending a message or call.

    elif "read screen" in command:
        speak("Screen reading is not implemented yet but could be using OCR.")
        # Implement OCR-based screen reading if needed.

    elif "type with eyes" in command:
        speak("Eye-controlled typing activated.")
        # Implement typing functionality as part of eye-controlled mouse logic.

     elif "hello" in command:
        speak("Hello!")

    elif "play tamil song" in command:
        speak("Playing Tamil song on YouTube")
        webbrowser.open("https://www.youtube.com/results?search_query=tamil+songs")

    elif 'open gmail' in command:
        speak('Opening Gmail...')
        webbrowser.open('https://www.gmail.com')

    elif 'open google' in command:
        speak('Opening Google...')
        webbrowser.open('https://www.google.com')

    elif 'open youtube' in command:
        speak('Opening Youtube...')
        webbrowser.open('https://www.youtube.com/')

    elif 'open facebook' in command:
        speak('Opening Facebook...')
        webbrowser.open('https://www.facebook.com')

    # Additional commands
    elif "open setting" in command:
        speak("Opening Windows Settings...")
        os.system("start ms-settings:")

    elif "open control panel" in command:
        speak("Opening Control Panel...")
        os.system("start control")

    elif "open folder" in command:
        speak("Opening Documents folder...")
        os.startfile("C:\\Users\\Public\\Documents")  # You can change this path to a different folder

    elif "change wallpaper" in command:
        speak("Changing desktop wallpaper...")
        # Change wallpaper - You can replace with a specific image file path
        wallpaper_path = "C:/Users/Nithushan Mohan/Desktop/laptop-controller-for-disability/wall-1.jpg"
        script = f"reg add \"HKCU\\Control Panel\\Desktop\" /v Wallpaper /t REG_SZ /d {wallpaper_path} /f"
        subprocess.run(script, shell=True)
        subprocess.run("RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters", shell=True)

    elif "open bluetooth setting" in command:
        speak("Opening Bluetooth settings...")
        os.system("start ms-settings:bluetooth")
    
    elif 'shut down pc' in command:
        speak("Shutting down the laptop.")
        os.system("shutdown /s /t 1")

    elif 'create folder' in command:
        folder_name = "NewFolder"  # Modify as needed
        os.makedirs(folder_name, exist_ok=True)
        speak(f"Folder {folder_name} created successfully.")

    elif 'create file' in command:
        file_name = "NewFile.txt"  # Modify as needed
        with open(file_name, 'w') as f:
            f.write("This is a new file created by Temarias.")
        speak(f"File {file_name} created successfully.")

    elif 'rename folder' in command:
        old_name = "OldFolder"  # Modify as needed
        new_name = "RenamedFolder"  # Modify as needed
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            speak(f"Folder renamed from {old_name} to {new_name}.")
        else:
            speak("Folder does not exist.")

    elif 'increase volume' in command:
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Volume increased.")

    elif 'decrease volume' in command:
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Volume decreased.")

    elif 'capture photo' in command:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            speak("Camera not accessible.")
            return
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            speak("Photo captured and saved as captured_image.jpg.")
        else:
            speak("Failed to capture photo.")
        cam.release()

    elif 'type' in command:
        text_to_type = command.replace("type", "").strip()
        pyautogui.write(text_to_type)
        speak("Typing completed.")

    elif "open camera" in command:
        subprocess.run("start microsoft.windows.camera:", shell=True)

    elif "connect bluetooth" in command:
        device_name = "P47"  # Change with your device name
        speak(f"Connecting to {device_name}...")
        os.system(f"start ms-settings:bluetooth-devices")

    elif "connect to wi-fi" in command:
        wifi_name = "Redmi Note 10 Pro"  # Replace with your Wi-Fi name
        speak(f"Connecting to Wi-Fi network {wifi_name}...")
        # The following command will connect to a saved Wi-Fi network
        os.system(f"netsh wlan connect name={wifi_name}")

    elif "what time is it" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The current time is " + current_time)

    elif "what date is it" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak("Today's date is " + current_date)

    elif "tell me motivation quotes" in command:
        quotes = [
            "Failure will never overtake me if my determination to succeed is strong enough.",
            "The past cannot be changed. The future is yet in your power.",
            "Only I can change my life. No one can do it for me."
        ]
        speak(random.choice(quotes))

    elif "who are you" in command:
        speak("I am Temarias, your virtual assistant.")

    elif "daily planner" in command:
        speak("What task should I add to your daily planner?")
        task = listen_command()
        with open("daily_planner.txt", "a") as planner:
            planner.write(f"{datetime.datetime.now()} - {task}\n")
        speak("Task added to your daily planner.")

    elif "what is my emotion" in command:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            emotion = detect_emotion(frame)
            speak(f"I think you are feeling {emotion}.")
            if emotion in motivational_quotes:
                speak(random.choice(motivational_quotes[emotion]))
        else:
            speak("I couldn't access your camera.")
        cam.release()

    elif "goodbye" in command or "stop" in command:
        speak("Goodbye! Have a nice day.")
        sys.exit()


def voice_assistant():
    """Run the voice assistant in a separate thread."""
    greet_user()
    while True:
        command = listen_command()
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
        print(f"Error in eye-controlled mouse: {e}")
    finally:
        cam.release()


if __name__ == "__main__":
    threading.Thread(target=voice_assistant, daemon=True).start()
    eye_controlled_mouse()
