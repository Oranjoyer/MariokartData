import sys
import cv2
from cv2_enumerate_cameras import enumerate_cameras
import logManager
import numpy as np

CAPTURE_METHOD = cv2.CAP_ANY
cameras = []

# Initialize Global Variables For this File
def init():
    global CAPTURE_METHOD
    CAPTURE_METHOD=getCaptureMethod()
    sendMessage("Info",f"Capture Method Set to \'{CAPTURE_METHOD}\' on \'{sys.platform}\' System")
    enumCams()

# Gets Capture Method Based on OS
def getCaptureMethod():
    if(sys.platform.lower()=="linux"):
        return cv2.CAP_V4L2
    elif(sys.platform.lower()=="windows"):
        return cv2.CAP_DSHOW
def cropPercent(image, coords):
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    spot1 = [int(frame_width*(coords.topLeft[0]*.01)), int(frame_height*(coords.topLeft[1]*0.01))]
    spot2 = [int(frame_width*bottomRight[0]*.01), int(frame_height*coords.bottomRight[1]*.01)]
    return image[spot1[1]:spot2[1], spot1[0]:spot2[0]]

def cropHD(image, coords):
    if(image.shape[0:2] != (720,1280)):
            sendMessage("Info", "Resizing cropped image to 1280x720")
            image = cv2.resize(img,1280,720)
    return cropDirect(image, coords)

def cropDirect(image, coords):
    return image[coords.topLeft[1]:coords.bottomRight[1], coords.topLeft[0]:coords.bottomRight[0]]
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
            if(self.sourcesUsing.len()==1):
                activateCamera()
            return
        if (source in self.sourcesUsing) & active == False:
            self.sourcesUsing.remove(source)
            if(sourcesUsing.len()==0):
                deactivateCamera()
            return

    # Initializes Camera if not active yet
    async def activateCamera(self):
        if(self.captureObject != None):
            sendMessage("Warning", "Camera \'{name}\' is Already Activated")
            return
        try:
            self.captureObject = cv2.VideoCapture(self.index,CAPTURE_METHOD)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[1])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[0])
            sendMessage(f"Info", "Camera \'{name}\' Successfully Activated")
            self.cameraActive = True
        except:
            sendMessage("Error", "Camera \'{name}\' Unavailable For Activation")
            return
    # Non-Blocking Function in Order to Retrieve Latest Image from The Linked Camera
    async def updateImage(self):
        if(self.cameraActive):
            self.captureObject.read()
            sendMessage("ExInfo","Image Updated at Camera Source \'{name}\'")
            return
        sendMessage("Error","Camera Source \'{name}\' Not Active Before Attempting Image Update")
    
    # Deactivates Camera if Initialized
    def deactivateCamera(self):
        if(self.captureObject==None):
            sendMessage(f"Warning", "Camera \'{name}\' is Already Deactivated")
            return
        self.captureObject.release()
        self.captureObject = None
        self.cameraActive = False

# Class Using Tuples for Coordinate Pairs (Top Left is 0,0)
class CoordPair:
    def __init__(self, topLeft, bottomRight):
        self.topLeft = topLeft
        self.bottomRight = bottomRight

# Class which grabs image from camera
class VideoSource:
    def __init__(self, name, camera):
        self.name = name
        self.camera = camera
        self.crop = CoordPair((0,0),(100,100))

    # Get Latest Image from CameraSource Object
    def getImage(self):
        if(camera.cameraActive == False):
            sendMessage("Warning", "Last Camera Image Retrieved from Camera \'{camera.name}\' While Camera is Not Active. Image Will be Blank or Stale")
        return camera.currentImage
    