# Security_Camera_System
Simple security solution designed to monitor environments in real-time for the presence of individuals through face and body detection. 

**Overview**  
In creating this project for inclusion in a portfolio, the aim was to highlight the practical implications of computer vision and machine learning in real-world applications.The project thereby acts as a research exploration into the operations of OpenCV with Machine Learning. 
This project is a simple security solution designed to monitor environments in real-time for the presence of individuals through face and body detection technologies. Using OpenCV for video capture and processing, along with MediaPipe for face and pose detection, this program initiates video recording upon detecting a person and maintains the recording for a specified duration after the last detection. It operates requiring minimal user intervention, and stores recorded footage and event logs in a specified directory.

**Program Description:**  
Upon execution, the program prompts the user to specify a directory path for saving videos and reports. It checks for the existence of the directory, creating it if necessary, then activates the camera to begin monitoring. Utilizing MediaPipe's face detection and pose estimation models, the program continuously analyzes the video feed. When a person is detected, it starts recording the footage into an MP4 file, named with the current date and time for easy reference. The recording continues for a minimum duration after the last detection to ensure coverage of the event. Throughout its operation, the program logs all significant events, including system activation, start and stop times of recordings, and system deactivation. Upon the user's command or termination, it generates a detailed report in PDF format, encapsulating all logged events, and saves it alongside the recorded videos in the specified directory.

**Key Functions**
- Real-Time Monitoring and Detection: Leverages MediaPipe for efficient and accurate detection of faces and body in real-time.
- Automated Recording: Initiates video recording upon detection of a person.   
- Event Logging: Maintains a detailed log of all significant security events, including timestamps for system activation, detections, and recordings.
- Report Generation: Compiles an event log into a PDF report, providing a concise overview of the surveillance period.

**Limitation**
- Single Camera Support: Although it can be easily modified, the current implementation is limited to a single camera input. 
