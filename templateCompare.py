import cv2
import numpy as np
from camManager import CoordPair
import fileService
from fileService import BASE_PATH
from camManager import cropDirect
ASSETS_FOLDER = "assets"
PLACE_TEMPLATE_FOLDER = "placeTemplates"
RACE_PROGRESS_FOLDER = "raceProgress"
RESULT_FOLDER = "result"

TEMPLATE_FOLDERS = (PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RANKING_FOLDER)

def grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
def edgeDetect(frame):
    passF = frame - cv2.GaussianBlur(frame,(21,21),3)+127
    if(len(passF.shape)>2):
        passF = grayscale(passF)
    passF = cv2.Laplacian(passF, -1)
    return passF


# Not really gonna be used
def colorPass(frame):
    passF = frame
    passF = passF - cv2.GaussianBlur(passF,(21,21),3)+127
    passF = cv2.Laplacian(passF, -1)

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
        self.image = grayscale(image)
        self.cropLocation = cropLocation
        self.defTolerance = tolerance
        if(type(self.cropLocation) == tuple):
            sendMessage("Info", f"Converting Crop Location Coords in template \'{name}\' to CoordPair Object")
            self.cropLocation = CoordPair(cropLocation)
        if(CoordPair[1][0]-CoordPair[0][0] != image.shape()[1] | CoordPair[1][1]-CoordPair[0][1] != image.shape()[0]):
            sendMessage("Warning",f"Template \'{name}\' initialized with different shape than crop coordinate shape")
    def compareWithImage(self,img,tolerance):
        img = edgeDetect(img)
        if(tolerance > 0):
            tolerance = self.defTolerance
        if(img.shape != (720,1280)):
            sendMessage("Info", "Resizing comparison image to 1280x720")
            img = cv2.resize(img,1280,720)

        return compareImages(self,img,CoordPair((0,0),self.image.shape),self.cropLocation)
    
# Compare an Image With a Template Image (Not Object) (Based on 720p) (Returns Boolean)
def compareImages(templateImg, image, templateCoords, imageCoords, tolerance):
    if(type(templateImg)==Template):
        sendMessage("Error",f"Template Object \'{templateImg.name}\' passed into function \'compareImages\' (Use Image Object or template's built in compare function). Returning False Value (Fix Ur Code)")
        return False
    image = highPass(image)

    templateImg = cropDirect(templateImg,templateCoords)
    image = cropDirect(image,imageCoords)

    res = cv2.matchTemplate(frame,place,cv2.TM_CCOEFF_NORMED)
    loc = np.max(res)
    if(loc>tolerance):
        return true, loc
    
def bulkCompare(templateList,img,tolerance):
    maxRecog = None, 0
    index = 0
    for temp in templateList:
        comparison = temp.compareWithImage(img,tolerance)
        if(comparison[0]):
            maxRecog = temp, comparison[1]
        index += 1
    if(maxRecog[1]==0):
        sendMessage("ExInfo","No Matching template found in list")
    else:
        sendMessage("ExInfo",f"Matching template,\'{maxRecog[0].name}\'")
    return maxRecog, index

# Initializes all needed resources for this module
def init():
    obtainTemplates()