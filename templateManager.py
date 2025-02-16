import fileService
import templateCompare
from frameAverage import grayscale, edgeDetect,getAverageFrame
import cv2
import camManager
import json
from assetManager import ASSETS_FOLDER
from fileService import BASE_PATH
import logManager

templatesList = []

PLACES_FORMATTED = ("1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th")
REFERENCE_DIR = "MKImageData"

OUTPUT_DIR = "templatesMade"
TEMPLATE_FILETYPE = ".jpg"

# Sends Log Message with 'TemplateManager' source
def sendMessage(type,message):
    logManager.sendMessage(type, "TemplateManager", message)

# Class to Store Data about template image
class Template:
    def __init__(self,name,image,cropLocation,tolerance,path):
        self.image = None
        if(type(image) == None):
            image = fileService.getFileByName(name).fileData
        self.name = name
        self.image = grayscale(image)
        self.cropLocation = cropLocation
        self.defTolerance = tolerance # default tolerance value
        self.path = path # path of file
        if(self.cropLocation[1][0]-self.cropLocation[0][0] != image.shape[1] | self.cropLocation[1][1]-self.cropLocation[0][1] != image.shape[0]):
            sendMessage("Warning",f"Template \'{name}\' initialized with different shape than crop coordinate shape")
    def compareWithImage(self,img,tolerance):
        img = edgeDetect(img)
        if(tolerance > 0):
            tolerance = self.defTolerance
        if(img.shape != (1280,720)):
            sendMessage("Info", "Resizing comparison image to 1280x720")
            img = cv2.resize(img,(1280,720))

        return compareImages(self,img,self.croplocation((0,0),self.image.shape),self.cropLocation)
    
    # Returns Template Details formatted as json String
    def asJson(self):
        diction = self.__dict__
        diction.pop("image")

        return json.dumps(diction)
    
    @staticmethod
    def reconstructTemplate(img, storedJson):
        if(type(storedJson)==str):
            storedJson = json.parse(storedJson)
        templateObj = Template(storedJson["name"],img,storedJson["cropLocation"],storedJson["tolerance"],storedJson["path"])

def createPlaces():
    for i in range(12):
        createTemplate(f"{i+1}Place",((1086,568),((1086+130),(568+121))),("Race","Drive","!PlaceChange",PLACES_FORMATTED[i]),0.15,"placeTemplates")

# Builds Templates from Queries and Saves a JSON with the other data about it. All Images Used to Make Templates Should be 1280x720 (resize function just in case)
def createTemplate(name,coords,queries,tolerance,path):
    sendMessage("ExInfo",f"Template by Name \'{name}\' being created with queries \'{queries}\'")
    fileList = fileService.loadFilesFromQueries(fileService.formatStringsAsPath(BASE_PATH,REFERENCE_DIR),queries)
    imageList = []
    for f in fileList:
        imageList.append(cv2.resize(f.fileData,(1280,720)))
        # print(f.fileData)
    
    # averageImage = getAverageFrame([cv2.resize(file.fileData,(1280,720)) for file in fileList])
    averageImage = getAverageFrame(imageList)
    # print(averageImage.shape)
    templateImg = averageImage
    templateImg = camManager.cropHD(averageImage,coords)
    templateObj = Template(name,templateImg,coords,tolerance,path)
    cv2.imwrite(fileService.formatStringsAsPath(BASE_PATH,OUTPUT_DIR,path)+name+TEMPLATE_FILETYPE,templateImg)
    templateJSON = open(fileService.formatStringsAsPath(BASE_PATH,OUTPUT_DIR,path)+name+".json","w")
    templateJSON.write(templateObj.asJson())
    templateJSON.close()
    # if(True not in storeQueried):
    # fileService.unloadFilesFromNameList([file.name for file in fileList])
    for f in fileList:
        fileService.fileList.remove(f)

# Function to load Template Images and JSONs as template objects. All templates should be saved as .jpg files or otherwise match TEMPLATE_FILETYPE and be in the same directory with same name as corresponding JSON contained in ASSETS_FOLDER as stated in assetManager.py
def loadTemplate(folder,name):
    tempImg = fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder+TEMPLATE_FILETYPE),name)
    tempJSON = fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder+".json"),name)
    templatesList.add(Template.asJson(tempImg,tempJSON))

def constructTemplates():
    createPlaces()
    





