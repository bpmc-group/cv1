import cv2  # OpenCV for image and video processing
from ultralytics import YOLO  # YOLO model for object detection
#from ultralytics import settings #didn't show what NEC wanted
import pandas as pd  # Pandas for handling YOLO's output data
import cvzone  # CVZone for easier OpenCV operations
import time
# also uses resources/coco.txt - list of 80 most common objects to detect

# Load the YOLOv10 model
model = YOLO("resources/yolov10s.pt") #small version - balanced speed & accuracy
#model = YOLO("trial/yolov10m.pt") #medium version - general purpose
#model = YOLO("trial/yolov10b.pt") #balanced version - increased width for accur
#model = YOLO("trial/yolov10l.pt") #large version - higher accuracy but increased CPU req
#model = YOLO("trial/yolov10x.pt") #Extra-large version - maximum accuracy
# YOLO 11
#model = YOLO("trial/yolo11s-pose.pt") #only shows people - no pose so far
#model = YOLO("trial/yolo11m-pose.pt") #only shows people - no pose so far
 
# Function to capture mouse movement events (not used in detection logic)
# This capability is not part of the mainline functionality of this program
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point) #displays, for example  '[1054, 837]'

# Creating a window for displaying the video
cv2.namedWindow('mouseWindow')
cv2.setMouseCallback('mouseWindow', RGB)

# Open video camera for processing - comment out when using video file option
#cap = cv2.VideoCapture(0)
#frame_title = "Camera"

#frame_title = 'resources/vtest.avi'
#frame_title = 'resources/Megamind.avi'
frame_title = 'resources/fall5.mp4'
#frame_title = 'resources/fall5gray.mp4'
# Open video file for processing - comment out when using video camera option
cap = cv2.VideoCapture(frame_title)

# Read COCO class labels (used for object detection classification)
my_file = open("resources/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

ret, frame = cap.read()

count = 0  # Frame counter
start_time = time.time() #measure elapsed time for performance estimation

while True:
    # Read frame from video
    ret, frame = cap.read()
    count += 1
    
    # Skip every third frame to improve processing speed
    # Every frame is still being read but only a few are processed
    if count % 6 != 0:
        continue
    '''Reducing count to 2 makes movements slower but smoother 
        but doesn't seem to improve detection of objects.
        Increasing count to 8, 15, even 30 makes the movements
        jerkier but faster (like fast forward. At 30, it still
        seems to detect all the same objects but it is only detecting
        once per second. At 60, very jerky and things pop in and
        then just disappear). If this were a production env, the 
        number of frames to skip should be a config value or a
        param value so could optimize for each device '''
    
    # Break if the video has ended
    if not ret:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Frames Processed In Video: {count}\nElapsed time: {elapsed_time:.1f} seconds")
        break
    
    # Run without resizing & see how it looks. Change sizes IF required as it may slow down processing
    #frame = cv2.resize(frame, (640, 384)) # actually ran slower
    #frame = cv2.resize(frame, (1280, 960)) # double-size makes vtest.avi easier to view
    #frame = cv2.resize(frame, (1440,810))
    # IN PRODUCTION ENV: Frame size should be run time param

    # Perform object detection using YOLO
    results = model(frame)  # include ", verbose=False" in params to turn off diagnostic info BUT turning off 
        # verbose doesn't improve performance by very much
        # YOLO model ALWAYS detects every type of object so not much performance improvement detecting just people
    a = results[0].boxes.data  # Extract detection results
    px = pd.DataFrame(a).astype("float")  # Convert to Pandas DataFrame
    
    for index, row in px.iterrows():
        x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])  # Bounding box coordinates
        d = int(row[5])  # Class ID
        c = class_list[d]  # Get class label (e.g., 'person')
        if 'person' in c:
            # Determine if the person is in a falling position
            h_fall = y2 - y1  # Height of bounding box
            w_fall = x2 - x1  # Width of bounding box
            thresh = h_fall - w_fall  # Threshold to determine if the person is lying down
            #This only works if person lying down in y-dimension (left to right). If person
            # is lying down in x-dimension (perpendicular to bottom of screen). ALSO, if 
            # person is NOT moving around, the object detector stops detecting the person
            if thresh < 0:  # If width > height, assume the person has fallen
                cvzone.putTextRect(frame, 'person_fall', (x1, y1), 1, 1)  # Display fall warning
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw bounding box in red for fall
                print(thresh)  # Debugging output 
            else:
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)  # Display class label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box (green for standing person)
        else: # make this a run time parameter - if NOT a person, skip #NOTE doesn't save much time but easier to watch
            cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)  # Display class label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box in green       

    # Show the processed frame with bounding boxes
    cv2.imshow(frame_title, frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Frames Processed Before Break: {count}\nElapsed time: {elapsed_time:.1f} seconds")
        break

# Release video resources and close display window
cap.release()
cv2.destroyAllWindows()
