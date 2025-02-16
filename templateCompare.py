import cv2
import numpy as np
import fileService
from fileService import BASE_PATH
from camManager import cropDirect
import logManager

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

# Class to Store Data about template image
class Template:
    def __init__(self,name,image,cropLocation,tolerance,path):
        self.image = None
        if(image == None):
            self.image = fileService.getFileByName(name).fileData
        self.name = name
        self.image = grayscale(image)
        self.cropLocation = cropLocation
        self.defTolerance = tolerance # default tolerance value
        self.path = path # path of file
        if(self.croplocation[1][0]-self.croplocation[0][0] != image.shape[1] | self.croplocation[1][1]-self.croplocation[0][1] != image.shape[0]):
            sendMessage("Warning",f"Template \'{name}\' initialized with different shape than crop coordinate shape")
    def compareWithImage(self,img,tolerance):
        img = edgeDetect(img)
        if(tolerance > 0):
            tolerance = self.defTolerance
        if(img.shape != (720,1280)):
            sendMessage("Info", "Resizing comparison image to 1280x720")
            img = cv2.resize(img,1280,720)

        return compareImages(self,img,self.croplocation((0,0),self.image.shape),self.cropLocation)
    
    # Returns Template Details formatted as json String
    def asJson():
        diction = __dict__()
        diction.pop("image")

        return json.dumps(diction)
    
    @staticmethod
    def reconstructTemplate(img, storedJson):
        if(type(storedJson)==str):
            storedJson = json.parse(storedJson)
        templateObj = Template(storedJson["name"],img,storedJson["cropLocation"],storedJson["tolerance"],storedJson["path"])
    
# Compare an Image With a Template Image (Not Object) (Based on 720p) (Returns Boolean)
def compareImages(templateImg, image, templateCoords, imageCoords, tolerance):
    if(type(templateImg)==Template):
        sendMessage("Error",f"Template Object \'{templateImg.name}\' passed into function \'compareImages\' (Use Image Object or template's built in compare function). Returning False Value (Fix Ur Code)")
        return False
    image = edgeDetect(image)

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