import cv2
 
# Open the video file
cap = cv2.VideoCapture("resources/fall5.mp4")
 
# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()
 
# Get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
 
print(f"fps: {frame_rate}, width: {frame_width}, height: {frame_height}")
#exit()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, frame_rate, (frame_width, frame_height), isColor=False)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or error occurred.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Write the frame to the output video file
    out.write(gray_frame)
 
    # Display the frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()