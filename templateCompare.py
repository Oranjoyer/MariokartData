import cv2
import numpy as np
from camManager import CoordPair
from fileService import BASE_PATH
import fileService
ASSETS_FOLDER = "assets"
PLACE_TEMPLATE_FOLDER = "placeTemplates"
RACE_PROGRESS_FOLDER = "raceProgress"
RESULT_FOLDER = "result"

TEMPLATE_FOLDERS = (PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RANKING_FOLDER)


# Simplifies Function to Retrieve Asset files from the filesystem
def getAsset(folder,name):
    fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder)+name,name)

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "CameraManager",message)

# Gather Template Files and Place in FileService
def obtainTemplates():
# Calls Every "ObtainTemplate" Function
    obtainPlaceTemplates()
    obtainRaceProgressTemplates()
    obtainResultsTemplates()

# Collect Every Race Progress Indicator Template from Folder
def obtainRaceProgressTemplates():
    getAsset(RACE_PROGRESS_FOLDER,"Go.jpg")
    getAsset(RACE_PROGRESS_FOLDER,"Finish.jpg")

# Collect Every Place Template Image from Folder
def obtainPlaceTemplates():
    for i in range(12):
        getAsset(PLACE_TEMPLATE_FOLDER,f"{i+1}Place.jpg")

# Collect Result Screen Templates
def obtainResultsTemplates():
    getAsset(RESULT_FOLDER,"TeamPoints.jpg")

# Class to Store Data about template image
class Template:
    def __init__(self,name,image,cropLocation,tolerance):
        self.name = name
        self.image = image
        self.cropLocation = cropLocation
        if(type(self.cropLocation) == tuple):
            sendMessage("Info", f"Converting Crop Location Coords in template \'{name}\' to CoordPair Object")
            self.cropLocation = CoordPair(cropLocation)
        if(CoordPair[1][0]-CoordPair[0][0] != image.shape()[1] | CoordPair[1][1]-CoordPair[0][1] != image.shape()[0]):
            sendMessage("Warning",f"Template \'{name}\' initialized with different shape than crop coordinate shape")
    def compareWithImage(self,img,tolerance):
        if(img.shape != (720,1280)):
            sendMessage("Info", "Resizing comparison image to 1280x720")
            img = cv2.resize(img,1280,720)

# Crops Images (Returns Image Object)
def cropImage(image,coords):
    sendMessage("NONE","Function \'cropImage\' not currently implemented")
    if(type(coords)==tuple):
        sendMessage("Info",f"Converting Coordinate Tuple \'{coords}\' to CoordPair Object")
        coords = CoordPair(coords)
    return None
    
# Compare an Image With a Template Image (Not Object) (Returns Boolean)
def compareImages(templateImg, image, templateCoords, imageCoords, tolerance):
    if(type(templateImg)==Template):
        sendMessage("Error",f"Template Object \'{templateImg.name}\' passed into function \'compareImages\' (Use Image Object). Returning False Value (Fix Ur Code)")
        return False

# Initializes all needed resources for this module
def init():
    obtainTemplates()