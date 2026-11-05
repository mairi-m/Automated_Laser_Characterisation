# Author: Mairi MacIain
# Date October 2026
# 
# This is a combination of camera_help.py and grab_single_frame.py. It has issues with 


import numpy as np
import os
import time
import cv2
import matplotlib.pyplot as plt
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE

dll_path = r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam"
os.add_dll_directory(dll_path)
os.environ["PATH"] = dll_path + os.pathsep + os.environ["PATH"]


with TLCameraSDK() as sdk:
    available_cameras = sdk.discover_available_cameras()

    if len(available_cameras) < 1:
        print("No cameras detected")
        exit()
    elif len(available_cameras) >1:
        print("Multiple cameras detected")
        exit()
    else:
        print("Available Camera: ", available_cameras)


    with sdk.open_camera(available_cameras[0]) as camera:
        camera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
        camera.exposure_time_us = 10000  # set exposure to 11 ms
        camera.frames_per_trigger_zero_for_unlimited = 0  # start camera in continuous mode
        camera.image_poll_timeout_ms = 1000  # 1 second polling timeout

        t_arm = time.time()
        camera.arm(3)
        print(f"arm() took {time.time() - t_arm:.2f} s")

        camera.issue_software_trigger()
        frame = camera.get_pending_frame_or_null()



        if frame is None:
            camera.disarm()
            print("Unable to acquire image, program exiting...")
            exit()

        #plt.hist(frame.image_buffer)
        #plt.show

        print("frame #{} received!".format(frame.frame_count))
        image = np.copy(frame.image_buffer).reshape(camera.image_height_pixels, camera.image_width_pixels) 

        print(image[350:400, 100:150])
        #image_array = np.full((camera.image_height_pixels, camera.image_width_pixels, 3), 0, dtype=np.uint8)
        #image_array[:,:,0] = image
        #image_array[:,:,1] = image
        #image_array[:,:,2] = image

        print(camera.bit_depth)
        #image = (image >> (camera.bit_depth - 8)).astype(np.uint8)
        #image = image.astype(np.uint8)

        camera.disarm()

        #cv2.calcHist(image.flatten())
        #cv2.imwrite("camera_aquisition.png", image)
        #cv2.imshow("Image From TSI Cam", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        plt.figure(figsize=(8,6))
        plt.imshow(image, cmap="gray")
        cbar = plt.colorbar(shrink=0.6)
        cbar.set_label("Pixel Value")
        plt.xlabel("Width (Pixels)")
        plt.ylabel("Height (Pixels)")
        plt.title("Yoda as taken by camera_aquisition.py (Exposure 11ms)")
        plt.savefig("yoda_aquisition.png")

        plt.figure(figsize=(8,6))
        plt.xlabel("Pixel Value")
        plt.ylabel("Counts")
        plt.title("Yoda image histogram")
        plt.hist(image.ravel(), bins=2**10)
        plt.savefig("yoda_histogram.png")
        plt.show()


    print("Done")