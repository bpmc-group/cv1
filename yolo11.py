''' From Ultralytics video about Object Detection
The speaker said using it was really simple, just a 3 line program so I had to try it
Each time that it is run, it adds a numbered "predict" to the runs/detect/ folder where 
each folder contains an annotated copy of the subject video, fall5.mp4 in this case. The
annotated copy is a dup of the original with every object that was detected outlined by a
boundary box that is labeled with the type of object that it is AND the confidence it has
that it is really that object. Funny to see the man lying on the floor being labeled a dog. 
'''
from ultralytics import YOLO

model = YOLO('/Users/nelsonchamberlain/Documents/GitHub/cv1/resources/model/yolo11x.pt')

results = model(source='resources/video/fall5.mp4', show=True, conf=0.4, save=True)