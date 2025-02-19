import sys
import cv2
import logManager
import numpy as np
from imageMgt import cropDirect, cropPercent,cropHD
import fileService

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "CameraManager",message)

FLIP = True
MAX_FAIL = 10
CAPTURE_METHOD = cv2.CAP_ANY
cameras = []

# Initialize Global Variables For this File
def init():
    global CAPTURE_METHOD
    CAPTURE_METHOD=getCaptureMethod()
    sendMessage("Info",f"Capture Method Set to \'{CAPTURE_METHOD}\' on \'{sys.platform}\' System")
    # videoTest = cv2.VideoCapture("mkVid.mkv")
    
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

# Finds All Attached Cameras
def enumerate_cameras(capMethod):
    index = 0
    borked = 0
    camList = []
    while borked < MAX_FAIL:
            sendMessage("Info",f"checking camera index \'{index}\'")
            cam = cv2.VideoCapture(index,capMethod)
            if(cam.isOpened()):
                if(cam.read()[0]):
                    sendMessage("Info",f"Able to Grab Images from camera \'{index}\'")
                camList.append((cam, index))
            else:
                borked += 1
            cam.release()
            index += 1
    
    return camList
# Finds All Connected Cameras
def enumCams():
    for camera in enumerate_cameras(CAPTURE_METHOD):
        camSource = CameraSource(camera[0],camera[1],f"Camera{camera[1]}")
        cameras.append(camSource)
        sendMessage(f"Info",f"Camera \'{camera[1]}\' Found and Added to List")


# Create And Return CameraSource Object
def createCameraSource(index, name):
    return CameraSource(index, name)

# Function to Get Current Image from Every Active CameraSource
def updateCameraImages():
    for camera in cameras:
        if(camera.cameraActive):
            camera.updateImage()

# Class That Manages VideoCapture objects and can remember camera indexes without blocking cameras when not in use
class CameraSource:
    def __init__(self, cam, index, name):
        self.name = name
        self.captureObject = cam
        self.index = index
        self.sourcesUsing = []        # if FLIP:
        #     flipComp = compareImages(self.image,cv2.f
        self.cameraActive = False
        self.resolution = (720,1280)
        self.currentImage = fileService.getFileByName("placeholder.png").fileData
    
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
        if(self.captureObject != None and self.captureObject.isOpened()):
            sendMessage("Warning", f"Camera \'{self.name}\' is Already Activated")
            return
        try:
            if(self.captureObject == None):
                if(type(self.index)== str):
                    CAPTURE_METHOD = cv2.CAP_ANY
                self.captureObject = cv2.VideoCapture(self.index,CAPTURE_METHOD)
            else:
                self.captureObject.open(self.index)
            ret, image = self.captureObject.read()
            if(not ret):
                sendMessage("Error", f"Camera \'{self.name}\' Unavailable For Activation. Likely In Use")
            else:
                self.captureObject.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[1])
                self.captureObject.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[0])
                sendMessage("Info", f"Camera \'{self.name}\' Successfully Activated")
                self.cameraActive = True
        except Exception as e:
            sendMessage("Error", f"Camera \'{self.name}\' Unavailable For Activation | Exception: {e}")
            return
    # Function in Order to Retrieve Latest Image from The Linked Camera
    def updateImage(self):
        if(self.cameraActive):
            ret, img = self.captureObject.read()
            if(ret):
                sendMessage("Debug",f"Image Updated at Camera Source \'{self.name}\'")
                if(FLIP):
                    self.currentImage = cv2.flip(img,0)
                else:
                    self.currentImage = img
            else:
                sendMessage("Error",f"Image failed to update at Camera Source \'{self.name}\'")
            return
        sendMessage("Error",f"Camera Source \'{self.name}\' Not Active Before Attempting Image Update")
    
    # Deactivates Camera if Initialized
    def deactivateCamera(self):
        if(not(self.captureObject.isOpened())):
            sendMessage(f"Warning", f"Camera \'{self.name}\' is Already Deactivated")
            return
        self.captureObject.release()
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
            sendMessage("Warning", f"Last Camera Image Retrieved from Camera \'{self.camera.name}\' While Camera is Not Active. Image Will be Blank or Stale")
        return cropPercent(self.camera.currentImage,self.cropPercent)
    