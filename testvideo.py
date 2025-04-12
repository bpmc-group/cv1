import numpy as np
import cv2 as cv
import cvzone
 
cap = cv.VideoCapture('resources/fall5.mp4')
 
while cap.isOpened():
    ret, frame = cap.read()
    frame = cvzone.cornerRect(
        frame,  # The image to draw on
        (200, 200, 600, 200),  # The position and dimensions of the rectangle (x, y, width, height)
        l=30,  # Length of the corner edges
        t=5,  # Thickness of the corner edges
        rt=1,  # Thickness of the rectangle
        colorR=(255, 0, 255),  # Color of the rectangle
        colorC=(0, 255, 0)  # Color of the corner edges
    )

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
 
 
cap.release()
cv.destroyAllWindows()

