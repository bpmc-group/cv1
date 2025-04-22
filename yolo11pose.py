''' From Ultralytics video about Object Detection
Based on yolo11.py but uses pose estimation pre-trained model. When this prog runs 
against vtest.avi (people walking around) it doesn't find many people. Are the people
too small? It recognizes people much better in fall5.mp4. It has trouble with fallen guy.
Note that the generated annotated copy is a video that runs much faster than when it was 
being annotated and can be stopped at any point to review the results at that instant.
'''
from ultralytics import YOLO

model = YOLO('resources/model/yolo11s-pose.pt')

results = model(source='resources/video/fall5.mp4', show=True, conf=0.4, save=True)