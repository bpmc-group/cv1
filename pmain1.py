import cv2  # OpenCV for image and video processing
from ultralytics import YOLO  # YOLO model for object detection
import pandas as pd  # Pandas for handling YOLO's output data
import cvzone  # CVZone for easier OpenCV operations

# Load the YOLOv10 model
model = YOLO("resources/yolov10s.pt")  
 
# Function to capture mouse movement events (not used in detection logic)
# This capability is not part of the mainline functionality of this program
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point) #displays, for example  '[1054, 837]'

# Creating a window for displaying the video
cv2.namedWindow('resources/vtest.avi')
cv2.setMouseCallback('RGB', RGB)


# Open video camera for processing - comment out when using video file option
#cap = cv2.VideoCapture(0)

frame_title = 'resources/fall5.mp4'
# Open video file for processing - comment out when using video camera option
cap = cv2.VideoCapture(frame_title)

#if cap.isOpened():
#    print("Error opening video file")
#    exit()

# Read COCO class labels (used for object detection classification)
my_file = open("resources/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

ret, frame = cap.read()
multiplier = .75
h, w, ch = frame.shape
h = round(h * multiplier) 
w = round(w * multiplier)
print(f"H: {h} x W:{w}")

count = 0  # Frame counter

while True:
    # Read frame from video
    ret, frame = cap.read()
    count += 1
    
    # Skip every third frame to improve processing speed
    # Every frame is still being read but only a few are processed
    if count % 3 != 0:
        continue
    '''Reducing count to 2 makes movements slower but smoother 
        but doesn't seem to improve detection of objects.
        Increasing count to 8, 15, even 30 makes the movements
        jerkier but faster (like fast forward. At 30, it still
        seems to detect all the same objects but it is only detecting
        once per second. At 60, very jerky and things pop in and
        then just disappear). If this were a production env, the 
        number of frames to skip should be a config value or a
        param value so could optimize for each viewing device '''
    
    # Break if the video has ended
    if not ret:
        print(f"Frames Processed In Video: {count}")
        break
    
    # Resize frame for better performance (WxH) # Seems to run OK without resizing
    #frame = cv2.resize(frame, (1020, 600))
    #frame = cv2.resize(frame, (210, 150)) 
    #frame = cv2.resize(frame, (1440,810))

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
       # print(thresh)  # Debugging output
        
        if 'person' in c:
            if thresh < 0:  # If width > height, assume the person has fallen
                cvzone.putTextRect(frame, 'person_fall', (x1, y1), 1, 1)  # Display fall warning
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw bounding box in red for fall
            else:
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)  # Display class label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box in green

    # Show the processed frame with bounding boxes
    cv2.imshow(frame_title, frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"Frames Processed Before Break: {count}")
        break

# Release video resources and close display window
cap.release()
cv2.destroyAllWindows()
