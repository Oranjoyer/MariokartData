import sys
import cv2
from cv2_enumerate_cameras import enumerate_cameras
import logManager
import numpy as np
from imageMgt import cropDirect, cropPercent,cropHD

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "CameraManager",message)

CAPTURE_METHOD = cv2.CAP_ANY
cameras = []

# Initialize Global Variables For this File
def init():
    global CAPTURE_METHOD
    CAPTURE_METHOD=getCaptureMethod()
    sendMessage("Info",f"Capture Method Set to \'{CAPTURE_METHOD}\' on \'{sys.platform}\' System")
    # videoTest = cv2.VideoCapture("mkVid.mkv")
    videoTest = cv2.VideoCapture(0)
    videoTest.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    videoTest.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    enumCams()

# Gets Capture Method Based on OS
def getCaptureMethod():
    if(sys.platform.lower()=="linux"):
        return cv2.CAP_ANY
    elif(sys.platform.lower()=="windows"):
        return cv2.CAP_DSHOW
# Send Messages to Logs
def sendMessage(type, message):
    logManager.sendMessage(type, "CameraManager", message)

# Finds All Connected Cameras
def enumCams():
    for camera_info in enumerate_cameras(CAPTURE_METHOD):
        camSource = createCameraSource(camera_info.index,camera_info.name)
        cameras.append(camSource)
        sendMessage(f"Info",f"Camera with index \'{camSource.index}\' and name \'{camSource.name}\' Found and Added to List")

# Create And Return CameraSource Object
def createCameraSource(index, name):
    return CameraSource(index, name)

# Function to Get Current Image from Every Active CameraSource
def updateCameraImages():
    for camera in cameras:
        if(camera.cameraActive):
            asyncio.run(camera.updateImage())

# Class That Manages VideoCapture objects and can remember camera indexes without blocking cameras when not in use
class CameraSource:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.captureObject = None
        self.sourcesUsing = []
        self.cameraActive = False
        resolution = (720,1280)
        self.currentImage = np.empty(resolution)
    
    # Sets Whether The Camera Is Active
    def setActivity(self, source, active):
        if (source not in self.sourcesUsing) & active:
            self.sourcesUsing.append(source)
            if(len(self.sourcesUsing)==1):
                self.activateCamera()
            return
        if (source in self.sourcesUsing) & active == False:
            self.sourcesUsing.remove(source)
            if(sourcesUsing.len()==0):
                deactivateCamera()
            return

    # Initializes Camera if not active yet
    def activateCamera(self):
        if(self.captureObject != None):
            sendMessage("Warning", f"Camera \'{name}\' is Already Activated")
            return
        try:
            self.captureObject = cv2.VideoCapture(self.index,CAPTURE_METHOD)
            self.captureObject.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[1])
            self.captureObject.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[0])
            sendMessage("Info", f"Camera \'{name}\' Successfully Activated")
            self.cameraActive = True
        except Exception as e:
            print(e)
            sendMessage("Error", f"Camera \'{self.name}\' Unavailable For Activation")
            return
    # Function in Order to Retrieve Latest Image from The Linked Camera
    def updateImage(self):
        if(self.cameraActive):
            self.captureObject.read()
            sendMessage("ExInfo",f"Image Updated at Camera Source \'{name}\'")
            return
        sendMessage("Error",f"Camera Source \'{self.name}\' Not Active Before Attempting Image Update")
    
    # Deactivates Camera if Initialized
    def deactivateCamera(self):
        if(self.captureObject==None):
            sendMessage(f"Warning", f"Camera \'{self.name}\' is Already Deactivated")
            return
        self.captureObject.release()
        self.captureObject = None
        self.cameraActive = False

# Class which grabs image from camera. Optionally pass 2d tuple of (x1 y1) and (x2 y2) pairs
class VideoSource:
    def __init__(self, name, camera,cropPercent):
        self.name = name
        self.camera = camera
        self.cropPercent = cropPercent
    def setActivity(self,active):
        self.camera.setActivity(self,active)
    # Get Latest Image from CameraSource Object
    def getImage(self):
        if(self.camera.cameraActive == False):
            sendMessage("Warning", f"Last Camera Image Retrieved from Camera \'{camera.name}\' While Camera is Not Active. Image Will be Blank or Stale")
        return cropPercent(camera.currentImage,self.cropPercent(cropPercent))
    