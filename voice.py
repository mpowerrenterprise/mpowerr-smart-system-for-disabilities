import cv2
import mediapipe as mp
import pyautogui
import matplotlib.pyplot as plt
import speech_recognition as sr
import pyttsx3
import datetime
import random
import sys
import webbrowser
import threading
import os
import subprocess

# Initialize Face Mesh and Speech Components
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set up voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

# Screen dimensions
screen_w, screen_h = pyautogui.size()


def speak(audio):
    """Function to speak a given text."""
    print("Assistant:", audio)
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    """Greet the user based on the time of day."""
    currentH = int(datetime.datetime.now().hour)
    if currentH < 12:
        speak("Good Morning! I am your assistant Temarias.")
    elif currentH < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How may I help you?")


def listen_command():
    """Function to listen for a command and return it as text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio).lower()
            print("User:", text)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble with the speech service.")
            return ""


def execute_command(command):
    """Function to execute commands based on recognized speech."""
    if "what is your name" in command:
        speak("Temarias!")

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
    elif "open settings" in command:
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

    elif "open bluetooth settings" in command:
        speak("Opening Bluetooth settings...")
        os.system("start ms-settings:bluetooth")

    elif "connect bluetooth" in command:
        device_name = "Your Bluetooth Device Name"  # Change with your device name
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

    elif "bye" in command or "stop" in command:
        speak("Goodbye! Have a nice day.")
        sys.exit()


def voice_assistant():
    """Run the voice assistant in a separate thread."""
    greetMe()
    while True:
        command = listen_command()
        if command:
            execute_command(command)


def eye_controlled_mouse():
    """Eye-Controlled Mouse Functionality."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Error: Camera not accessible. Please check the connection.")

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame from camera. Exiting...")
                break

            # Flip and preprocess the frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            frame_h, frame_w, _ = frame.shape

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark

                # Cursor control using specific landmarks
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)

                    if id == 1:  # Control the mouse using this landmark
                        screen_x = int(screen_w * landmark.x)
                        screen_y = int(screen_h * landmark.y)
                        pyautogui.moveTo(screen_x, screen_y, duration=0.1)

                # Blink detection for left eye
                left_eye = [landmarks[145], landmarks[159]]
                if abs(left_eye[0].y - left_eye[1].y) < 0.004:  # Adjust threshold if necessary
                    pyautogui.click()
                    pyautogui.sleep(1)  # Prevent multiple rapid clicks

            # Display the frame using Matplotlib
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.show(block=False)
            plt.pause(0.01)
            plt.clf()  # Clear the figure for the next frame

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cam.release()
        print("Camera released.")


if __name__ == "__main__":
    # Run voice assistant in a separate thread
    threading.Thread(target=voice_assistant, daemon=True).start()

    # Run eye-controlled mouse in the main thread
    eye_controlled_mouse()
