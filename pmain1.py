import cv2  # OpenCV for image and video processing
from ultralytics import YOLO  # YOLO model for object detection
import pandas as pd  # Pandas for handling YOLO's output data
import cvzone  # CVZone for easier OpenCV operations

# Load the YOLOv10 model
model = YOLO("yolov10s.pt")  
 
# Function to capture mouse movement events (not used in detection logic)
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

# Creating a window for displaying the video
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Open video file for processing
cap = cv2.VideoCapture(0)

# Read COCO class labels (used for object detection classification)
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0  # Frame counter

while True:
    # Read frame from video
    ret, frame = cap.read()
    count += 1
    
    # Skip every third frame to improve processing speed
    if count % 3 != 0:
        continue
    
    # Break if the video has ended
    if not ret:
        break
    
    # Resize frame for better performance
    frame = cv2.resize(frame, (1020, 600))

    # Perform object detection using YOLO
    results = model(frame)
    a = results[0].boxes.data  # Extract detection results
    px = pd.DataFrame(a).astype("float")  # Convert to Pandas DataFrame
    
    for index, row in px.iterrows():
        x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])  # Bounding box coordinates
        d = int(row[5])  # Class ID
        c = class_list[d]  # Get class label (e.g., 'person')
        cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)  # Display class label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box (green for standing person)
        
        # Determine if the person is in a falling position
        h = y2 - y1  # Height of bounding box
        w = x2 - x1  # Width of bounding box
        thresh = h - w  # Threshold to determine if the person is lying down
        print(thresh)  # Debugging output
        
        if 'person' in c:
            if thresh < 0:  # If width > height, assume the person has fallen
                cvzone.putTextRect(frame, 'person_fall', (x1, y1), 1, 1)  # Display fall warning
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw bounding box in red for fall
            else:
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)  # Display class label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box in green

    # Show the processed frame with bounding boxes
    cv2.imshow("RGB", frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video resources and close display window
cap.release()
cv2.destroyAllWindows()
