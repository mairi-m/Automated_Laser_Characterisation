This repository contains code for the automated characterisation of a laser beam. It involves code for controlling 2 Thorlabs components, a stage and a camera.

To use this code type in a terminal: git clone LINK
where LINK is the HTTPS URL you get when you press the green code button.

You will also need to download some Thorlabs software:
- Kinesis software found at: https://www.thorlabs.com/software-pages/motion_control/?tabName=Kinesis%20Software

- ThorCam software https://www.thorlabs.com/software-pages/thorcam/?tabName=ThorCam%20Software (not ThorImageCam)

Unzip the C:\Program Files\Thorlabs\Scientific Imaging\Scientific Camera Support\Scientific_Camera_Interfaces.zip folder to C:\Program Files\Thorlabs\Scientific Imaging.

Then in a terminal write:
python -m pip install "C:\Program Files\Thorlabs\Scientific Imaging\Scientific Camera Interfaces\SDK\Python Toolkit\thorlabs_tsi_camera_python_sdk_package.zip"