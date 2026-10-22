import numpy as np
import os
import cv2
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE
import time
'''
try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path("C:\\Program Files\\Thorlabs\\ThorImageCAM")
except ImportError:
    configure_path = None
'''
#dll_path = r"C:\Users\mairi\LISA_project_code\dlls\64_lib"
dll_path = r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam"
os.add_dll_directory(dll_path)
os.environ["PATH"] = dll_path +os.pathsep + os.environ["PATH"]

with TLCameraSDK() as sdk:
    available_cameras = sdk.discover_available_cameras()
    if len(available_cameras) < 1:
        print("no cameras detected")
    else:
        print("Available Cameras: ", available_cameras)

    with sdk.open_camera(available_cameras[0]) as camera:

        def show(name):
            try:
                print(name, "=", getattr(camera, name))
            except Exception as e:
                print(name, "-> not available:", e)

        for name in [
            "operation_mode",
            "frames_per_trigger_zero_for_unlimited",
            "is_frame_rate_control_enabled",
            "frame_rate_control_value",
            "frame_time_us",
            "usb_port_type",
            "firmware_version",
        ]:
            show(name)

        print("Model:", camera.model, "| bit depth:", camera.bit_depth)
        print("Exposure limits (us):", camera.exposure_time_range_us)
        camera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED

        camera.exposure_time_us = 10000  # set exposure to 11 ms
        camera.frames_per_trigger_zero_for_unlimited = 1  # start camera in continuous mode
        camera.image_poll_timeout_ms = 5000  # 1 second polling timeout

        camera.arm(2)
        t0 = time.time()
        camera.issue_software_trigger()

        frame = None
        for attempt in range(5):
            frame = camera.get_pending_frame_or_null()
            if frame is not None:
                break
            print(f"attempt {attempt + 1} at {time.time() - t0:.2f} s:",
          "got frame" if frame is not None else "no frame")

        
        if frame is not None:
            print("frame #{} received!".format(frame.frame_count))
            frame.image_buffer
            image_buffer_copy = np.copy(frame.image_buffer)
            numpy_shaped_image = image_buffer_copy.reshape(camera.image_height_pixels, camera.image_width_pixels)
            nd_image_array = np.full((camera.image_height_pixels, camera.image_width_pixels, 3), 0, dtype=np.uint8)
            nd_image_array[:,:,0] = numpy_shaped_image
            nd_image_array[:,:,1] = numpy_shaped_image
            nd_image_array[:,:,2] = numpy_shaped_image
            
            cv2.imshow("Image From TSI Cam", nd_image_array)
        else:
            print("Unable to acquire image, program exiting...")
            exit()
            
        cv2.waitKey(0)
        camera.disarm()

#  Because we are using the 'with' statement context-manager, disposal has been taken care of.

print("program completed")
