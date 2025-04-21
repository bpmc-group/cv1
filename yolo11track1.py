'''
Copied from https://docs.ultralytics.com/modes/track/#persisting-tracks-loop
Opens a file, does model.track(frame...) instead of model(frame...), and includes
an ID number for every object that it detects. Note that any time an object stops
being detected, it receives a new number the next time it is detected. For example
the fallen man is detected as a person, then a dog, then a backpack then a suitcase
and each time he gets a different ID number assigned. The docs say "By retaining the 
center points of the detected bounding boxes and connecting them, we can draw lines 
that represent the paths followed by the tracked objects." See yolo11track2.py
for a demo of drawing the path lines
'''

import cv2
from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("resources/model/yolo11n.pt")

# Open the video file
video_path = "resources/video/fall5.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO11 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLO11 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()