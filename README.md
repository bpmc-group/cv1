# cv1

Explore computer vision with Pyton3, OpenCV and other libraries.

## Required libs

This is a listing of libraries that **MIGHT** be used in any code file but not necessarily every lib will be used in every code file. These will probably end up in a requirements.txt file

* opencv
* ultralytics (yolo v10)
* pandas
* cvzone

## Virtual Environments

Setting up a virtual envirnoment that has the Required libs installed makes it easier to develop and test the application programs. A potential use case would be developing CV apps using different base libraries, such as opencv vs kerras. Instead of  having a single environment that is polluted with all libs, separate environments should be created for each use case, ensuring that the required libs are included with distributions and no unused libs are included.

**NOTE:** Exiting a virtual environment is usually done by typing `deactivate` at the terminal prompt. If you are switching between virtual environments, it is probably prudent to deactive the current environment before activating the next env.

### Nelson's Env for opencv

* **Air laptop:** /opt/anaconda3/bin/activate && conda activate /opt/anaconda3/envs/cv-proj1
* **Mac mini:** /opt/anaconda3/bin/activate && conda activate /opt/anaconda3/envs/cv1
* **Win desktop:**

### Anaconda Virtual Environments

Anaconda is a wrapper around conda (package management tool) that includes the ability to launch many software tools such as Jupyter Lab/Notebook, PyCharm, Oracle Data Science Service, etc. It includes a "base" virtual environment that can be 'sticky' and show up where you don't expect it, for example, when you open a terminal in VS Code. If that happens, you can exit Anaconda's (base) environment by typing `conda deactivate`.

## Performance Measurements - Mac Mini M4

* 34.3 secs: yolov10s.pt, fall5.mp4, frame skip = 3
* 17.7 secs: same except frame skip = 6
* 48.2 secs: yolov10m.pt, fall5.mp4, frame skip = 3
* 25.2 secs: same except frame skip = 6
* 60.1 secs: yolov10b.pt, fall5.mp4, frame skip = 3
* 31.5 secs: same except frame skip = 6
* 70.5 secs: yolov10l.pt, fall5.mp4, frame skip = 3
* 36.1 secs: same except frame skip = 6
* 92.7 secs: yolov10x.pt, fall5.mp4, frame skip = 3
* 47.5 secs: same except frame skip = 6

**NOTE:** using "results = model(frame, verbose=False)" doesn't seem to improve performance. The cost of reporting which objects were detected and speed, etc, apparently is small.

Haven't found a precise way to measure how many objects were detected and which ones, but it appears that yolov10l is the most consistent detector of objects. 10x seems to detect more tv's but has trouble consistently detecting people, frisbees, etc. which is surprising since the 10x is supposed to be more accurate.

## Goals (in no particular order)

This is NOT a checklist of things to accomplish but just a listing of items that may (or may not) be explored in this project.

* provide selector program that allows user to pick the features to explore, for example, pose estimation, boundary boxes, and video camera
* add limb tracing/skeleton view
* add live video capabilities
* add multiple videos for testing, experimentaion (what about video of football, rugby, soccer, b-ball? - might not *   apply but should be easy to get)
* add interfacing with SMS messaging
* add interfacing with email
* add interfacing with other devices (alert/alarm systems unknown at this time)
* add audio notification
* checkbox list of notification choices
* web interface
* single room video feed- detect objects in room
* single room video feed - motion detection or image changing detection
* single room video feed- identify people in room - introduce visitors to CV system?
