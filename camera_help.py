
import numpy as np
import os
import time
import cv2
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE
 
# ---------------- Test settings (change these between runs) ----------------
SETTLE_SECONDS = 2       # Test 2: pause between arm() and the first trigger. Try 0, then 2.
POLL_TIMEOUT_MS = 200    # Short poll so we see WHEN the frame arrives
MAX_WAIT_S = 30          # Give up waiting for a frame after this long
EXTRA_TRIGGERS = 2       # Test 3: extra frames while still armed (is only the first one slow?)
# ---------------------------------------------------------------------------
 
dll_path = r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam"
# dll_path = r"C:\Users\mairi\LISA_project_code\dlls\64_lib"
os.add_dll_directory(dll_path)
os.environ["PATH"] = dll_path + os.pathsep + os.environ["PATH"]
 
 
def wait_for_frame(camera, label, t_start):
    """Poll for a frame, printing when it arrives. Returns the frame or None."""
    while time.time() - t_start < MAX_WAIT_S:
        frame = camera.get_pending_frame_or_null()
        if frame is not None:
            print(f"{label}: FRAME at {time.time() - t_start:.2f} s")
            return frame
    print(f"{label}: no frame within {MAX_WAIT_S} s")
    return None
 
 
def to_image(camera, frame):
    """Copy the frame out of the SDK buffer and scale to 8 bit for display."""
    img = np.copy(frame.image_buffer).reshape(
        camera.image_height_pixels, camera.image_width_pixels)
    return (img >> (camera.bit_depth - 8)).astype(np.uint8)
 
 
with TLCameraSDK() as sdk:
    available_cameras = sdk.discover_available_cameras()
    if len(available_cameras) < 1:
        print("no cameras detected")
        exit()
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
        camera.exposure_time_us = 10000                   # 10 ms
        camera.frames_per_trigger_zero_for_unlimited = 0  # one frame per trigger
        camera.image_poll_timeout_ms = POLL_TIMEOUT_MS
 
        t_arm = time.time()
        camera.arm(3)
        print(f"arm() took {time.time() - t_arm:.2f} s")
 
        if SETTLE_SECONDS > 0:
            print(f"settling for {SETTLE_SECONDS} s...")
            time.sleep(SETTLE_SECONDS)
 
        # First capture
        t0 = time.time()
        camera.issue_software_trigger()
        frame = wait_for_frame(camera, "first capture", t0)
 
        if frame is None:
            camera.disarm()
            print("Unable to acquire image, program exiting...")
            exit()
 
        print("frame #{} received!".format(frame.frame_count))
        image = to_image(camera, frame)   # copy now, before any further triggers
 
        # Extra captures while still armed: if these are fast, only the first is slow
        for i in range(EXTRA_TRIGGERS):
            t0 = time.time()
            camera.issue_software_trigger()
            wait_for_frame(camera, f"extra capture {i + 1}", t0)
 
        camera.disarm()
 
        cv2.imwrite("capture.png", image)
        cv2.imshow("Image From TSI Cam", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
 
print("program completed")