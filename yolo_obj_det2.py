import cv2  # OpenCV for image and video processing
from ultralytics import YOLO  # YOLO model for object detection
#from ultralytics import settings #didn't show what NEC wanted
import pandas as pd  # Pandas for handling YOLO's output data
import cvzone  # CVZone for easier OpenCV operations
import time
# also uses resources/coco.txt - list of 80 most common objects to detect

# Load the YOLOv11 model
#model = YOLO("resources/model/yolo11n.pt") #nano version - speed 
#model = YOLO("resources/model/yolo11s.pt") #small version - balanced speed & accuracy
model = YOLO("resources/model/yolo11m.pt") #medium version - general purpose
#model = YOLO("resources/model/yolo11l.pt") #large version - higher accuracy but increased CPU req
#model = YOLO("resources/model/yolo11x.pt") #Extra-large version - maximum accuracy

# Open video camera for processing - comment out when using video file option
#cap = cv2.VideoCapture(0)
#frame_title = "Camera"

#frame_title = 'resources/video/vtest.avi'
#frame_title = 'resources/video/Megamind.avi'
frame_title = 'resources/video/fall5.mp4'
#frame_title = 'resources/video/fall5gray.mp4'
# Open video file for processing - comment out when using video camera option
cap = cv2.VideoCapture(frame_title)

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS)) 

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
    
    # Skip every n frames to improve processing speed
    # Every frame is still being read but only a few are processed
    if count % 3 != 0:
        continue
    ''' Remove count to process every screen but slowest.
        Set count between 2 and 60 depending on hardware and video
        being viewed. Make this a runtime param for production
    '''
    
    # Break if the video has ended
    if not ret:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Frames Processed In Video: {count}\nElapsed time: {elapsed_time:.1f} seconds")
        break
    
    # Run without resizing & see how it performs. Reduce frame size IF required
    #frame = cv2.resize(frame, (960, 540)) # may slow down processing
    # IN PRODUCTION ENV, make frame size a run time parameter, pick multiple of actual screen size

    # Perform object detection using YOLO
    results = model(frame)  # verbose=False doesn't improve performance by very much

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
        else: # make this a run time parameter - if NOT a person, skip #NOTE doesn't save much time but easier to view people
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

print(f"fps: {frame_rate}, width: {frame_width}, height: {frame_height}") 

# Release video resources and close display window
cap.release()
cv2.destroyAllWindows()
