# Automated Surveillance 
# By R.H. Amezqueta

import cv2 as cv
import mediapipe as mp
import time
import datetime
import os
from fpdf import FPDF

save_directory = input("Enter the directory path where you want to save the videos and report: ")

# Checks if the directory exists and creates it if it doesn't
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Initializes MediaPipe Face Detection and Drawing
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initializes MediaPipe Pose for body silhouette detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Video Capture
captura = cv.VideoCapture(0)
event_log = []

activation_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print()
print('--- SECURITY SYSTEM ACTIVATED ---')
print(activation_time)
print()
event_log.append("---------------------------------------------")
event_log.append(f"SECURITY SYSTEM ACTIVATED: {activation_time}")

detection = False # tracks if there's been a detection 
detection_stopped_time = None # stores the time when the detection process stopped. 
timer_started = False

# Specifies the minimum duration (in seconds) for which the recording should continue once detection has started.
min_recording_time = 5

# Retrieves the width and height of the captured video frames
frame_size = (int(captura.get(3)), int(captura.get(4)))
# Compresses the video into "mp4v"
fourcc = cv.VideoWriter_fourcc(*"mp4v")
out = None

while True:
    success, frame = captura.read()
    if not success:
        break # Breaks the loop if no frame was captured

    # Coverts BGR to RGB (MediaPipe processes images in RGB)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame_rgb.flags.writeable = False # Makes the RGB read-only for a better performance

    # Runs face detection
    results_faces = face_detection.process(frame_rgb)

    # Runs body pose detection
    results_pose = pose.process(frame_rgb)

    # Makes the RGB frame writable
    frame_rgb.flags.writeable = True
    # Converts the RGB frame back to the BGR (OpenCV functions expect BGR)
    frame = cv.cvtColor(frame_rgb, cv.COLOR_RGB2BGR)

    # Starts the recording process when faces are detected in the current frame and recording is not already in progress.
    if results_faces.detections:
        if not detection:
            detection = True
            # current date and time into a string
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            # Saves the video in the current working directory of the script
            video_filename = os.path.join(save_directory, f"{current_time}.mp4")
            out = cv.VideoWriter(video_filename, fourcc, 20, frame_size)
            print()
            print("--- RECORDING ---")
            print(current_time)
            event_log.append(f"Recording Started: {current_time}")

       
    elif detection:
        if not timer_started:
            timer_started = True
            detection_stopped_time = time.time()
        # Checks the minimum time to keep recording after the last detection
        elif time.time() - detection_stopped_time >= min_recording_time:
            detection = False
            timer_started = False
            out.release()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            print("--- RECORDING STOPPED ---")
            print(current_time)
            print()
            event_log.append(f"Recording Stopped: {current_time}")
            
    else:
        # Stops the recording process when no detections have occurred
        if timer_started and time.time() - detection_stopped_time >= min_recording_time:
            # By R.H. Amezqueta
            detection = False
            timer_started = False
            out.release()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            print("--- RECORDING STOPPED ---")
            event_log.append(f"Recording Stopped: {current_time}")
            

    if detection:
        out.write(frame)

    cv.imshow("Camera", frame)
    
    if cv.waitKey(1) == ord('q'):
        system_stop_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        print()
        print('--- SECURITY SYSTEM STOPPED ---')
        print(system_stop_time)
        event_log.append(f"SECURITY SYSTEM STOPPED: {current_time}")
        event_log.append("----------------------------------------")
        break

if out:
    out.release()
captura.release()
cv.destroyAllWindows()

# Generate PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
for event in event_log:
    pdf.cell(0, 10, event, ln=True)
report_filename = os.path.join(save_directory, f"Report_{current_time}.pdf")
pdf.output(report_filename)
