import pylablib as pll
from pylablib.devices import Thorlabs as tl
import cv2
import time
import matplotlib.pyplot as plt


cam = tl.ThorlabsTLCamera("18009")

serials = tl.list_cameras_tlcam()
print(serials)

#print(cam.get_full_info())

#time.sleep(15)
#print("slept")

cam.set_exposure(1)

image = cam.snap(timeout=15)
cam.close()



cv2.imwrite("pic.png", image)
print("Image taken")
#plt.imshow(image)
plt.plot(image.flatten())
#plt.colorbar()
plt.show()

#for i in range(10):
#    plt.imshow(images[i])
'''

cam = tl.ThorlabsTLCamera("18009")

try:
    print("Camera connected")

    # Set exposure to 100 ms
    cam.set_exposure(0.1)

    # Start acquisition
    cam.start_acquisition()
    time.sleep(1)

    # Capture a frame, with a longer timeout
    image = cam.snap(timeout=10)

    print("Image shape:", image.shape)

    plt.imshow(image, cmap="gray")
    plt.colorbar()
    plt.show()

finally:
    cam.close()
'''