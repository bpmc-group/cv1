import cv2
import numpy as np
import matplotlib   #needed to get_backend()
import matplotlib.pyplot as plt

print(matplotlib.get_backend())
plt.plot((1, 4, 6, 2, 10))
plt.show()

# This plot won't show until prev plot closed
plt.plot((2, 4, 6, 8, 10))
plt.show()

# Read image as gray scale.
cb_img = cv2.imread("resources/img/blox.jpg", 0)

# Set color map to gray scale for proper rendering.
plt.imshow(cb_img, cmap="gray")
plt.show() # required in regular progs to show the plot
# but is NOT usually required in Jupyter

img_bgr = cv2.imread("resources/img/pic5.png", cv2.IMREAD_COLOR)
img_rgb_a = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

img_bgr = cv2.imread("resources/img/baboon.jpg", cv2.IMREAD_COLOR)
img_rgb_b = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

img_bgr = cv2.imread("resources/img/butterfly.jpg", cv2.IMREAD_COLOR)
img_rgb_c = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


plt.figure(figsize=[15, 5])
plt.subplot(131); plt.imshow(img_rgb_a); plt.title("pic5"); 
plt.subplot(132); plt.imshow(img_rgb_b); plt.title("baboon");
plt.subplot(133); plt.imshow(img_rgb_c); plt.title("butterfly");
plt.show() # needs the trailing plt.show()
