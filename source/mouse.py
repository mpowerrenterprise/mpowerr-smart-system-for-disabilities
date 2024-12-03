import cv2
import mediapipe as mp
import pyautogui
import matplotlib.pyplot as plt

# Initialize camera and Mediapipe Face Mesh
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise Exception("Error: Camera not accessible. Please check the connection.")

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
screen_w, screen_h = pyautogui.size()

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
