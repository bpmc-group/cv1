import numpy as np
import cv2 as cv
import cvzone
 
cap = cv.VideoCapture('resources/video/fall5gray.mp4')

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get frame width and height
frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv.CAP_PROP_FPS)) 

box_width = 300
box_height = 300
h_origin = 200
v_origin = 20

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("End of video or read() fail")
        break

    frame = cvzone.cornerRect(
        frame,  # The image to draw on
        (h_origin, v_origin, box_width, box_height),  # The position and dimensions of the rectangle (x, y, width, height)
        l=30,  # Length of the corner edges
        t=5,  # Thickness of the corner edges
        rt=1,  # Thickness of the rectangle
        colorR=(255, 0, 255),  # Color of the rectangle
        colorC=(0, 255, 0)  # Color of the corner edges
    )
    if box_width + h_origin <= 1800:
        box_width += 2

    if box_height+v_origin <= 1000:
        box_height += 2

    # Show the modified image
    cv.imshow("Image", frame)  # Display the image in a window named "Image"
    if cv.waitKey(1) == ord('q'):
        break

'''
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('frame', gray)
'''
print(f"fps: {frame_rate}, width: {frame_width}, height: {frame_height}") 
 
cap.release()
cv.destroyAllWindows()

