import fileService
from frameAverage import grayscale, edgeDetect,getAverageFrame
import cv2
from imageMgt import cropHD
import json
from fileService import BASE_PATH, ASSETS_FOLDER
import logManager

templatesList = []

PLACES_FORMATTED = ("1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th")
REFERENCE_DIR = "MKImageData"

ITEMS = ("Coin","Red","Green","Shroom","Banana","Boomerang","GoldShroom","Horn","Bullet","Star","Bomb","Inker","Shock","Plant","Boo","Fire","Blue","Crazy8","None")
ITEMS_WITH_MULTI = {"Red","Green","Shroom","Banana"}

OUTPUT_DIR = "templatesMade"
TEMPLATE_FILETYPE = ".jpg"

placeTemplateList = []
lapTemplateList = []
coinTemplateList = []

# Sends Log Message with 'TemplateManager' source
def sendMessage(type,message):
    logManager.sendMessage(type, "TemplateManager", message)
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
        if(comparison[0] and (comparison[1]>maxRecog[1])):
            maxRecog = temp, comparison[1]
        index += 1
    if(maxRecog[1]==0):
        sendMessage("ExInfo","No Matching template found in list")
    else:
        sendMessage("ExInfo",f"Matching template,\'{maxRecog[0].name}\'")
    return maxRecog + (index,)

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
        if(((self.cropLocation[1][0]-self.cropLocation[0][0]) != image.shape[1]) | ((self.cropLocation[1][1]-self.cropLocation[0][1]) != image.shape[0])):
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
    
    # Return Template Details As String
    def __str__(self):
        return f"Name: \'{self.name}\' | Crop Location: \'{self.cropLocation}\' | Default Tolerance: \'{self.defTolerance}\' | Folder Stored: \'{self.path}\' | Image Shape: \'{self.image.shape}\'"
    @staticmethod
    def reconstructTemplate(img, storedJson):
        if(type(storedJson)==str):
            storedJson = json.loads(storedJson)
        templateObj = Template(storedJson["name"],img,storedJson["cropLocation"],storedJson["defTolerance"],storedJson["path"])
        return templateObj

def createPlaces():
    for i in range(12):
        createTemplate(f"{i+1}Place",((1086,568),((1086+130),(568+121))),("Race","Drive","!PlaceChange",PLACES_FORMATTED[i]),0.15,"placeTemplates")
def createLaps():
    for i in range(3):
        createTemplate(f"Lap{i+1}",((153,644),(153+130,644+51)),[f"Lap{i+1}"],0.15,"raceProgress")
def createGo():
    createTemplate("Go",((468,236),(468+343,236+154)),["Go!"],0.1,"raceProgress")
def createFinish():
    createTemplate("Finish",((305,236),(305+669,236+154)),("Finish","Line"),0.15,"raceProgress")
def createCoins():
    for i in range(11):
        createTemplate(f"{i}Coin",((90,647),(90+55,647+50)),[f"{i}Coin"],0.15,"raceData")

# Builds Templates from Queries and Saves a JSON with the other data about it. All Images Used to Make Templates Should be 1280x720 (resize function just in case)
def createTemplate(name,coords,queries,tolerance,path):
    sendMessage("ExInfo",f"Template by Name \'{name}\' being created with queries \'{queries}\'")
    fileList = fileService.loadFilesFromQueries(fileService.formatStringsAsPath(BASE_PATH,REFERENCE_DIR),queries)
    imageList = []
    for f in fileList:
        imageList.append(cv2.resize(f.fileData,(1280,720)))
    
    # averageImage = getAverageFrame([cv2.resize(file.fileData,(1280,720)) for file in fileList])
    averageImage = getAverageFrame(imageList)
    templateImg = averageImage
    templateImg = cropHD(averageImage,coords)
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
    tempImg = fileService.loadFile(fileService.formatStringsAsPath(folder)+name+TEMPLATE_FILETYPE,name)
    tempJSON = fileService.loadFile(fileService.formatStringsAsPath(folder)+name+".json",name+".json")
    loadedTemplate = Template.reconstructTemplate(tempImg.fileData,tempJSON.fileData)
    templatesList.append(loadedTemplate)
    sendMessage("Info",f"Template successfully loaded with data: {loadedTemplate}")
    return loadedTemplate

def getLoadedTemplate(name):
    for template in templatesList:
        if(name == template.name):
            return template
    sendMessage("Error",f"Loaded Template by Name \'{name}\' not found. Returning null value instead")
    return None

def constructTemplates():
    createPlaces()
    createGo()
    createFinish()
    createLaps()
    createCoins()





