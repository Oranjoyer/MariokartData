import fileService
import templateCompare
from frameAverage import grayscale, edgeDetect,getAverageFrame
import cv2
import camManager
import json
from assetManager import ASSETS_FOLDER
from fileService import BASE_PATH

templatesList = []

PLACES_FORMATTED = ("1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th")
REFERENCE_DIR = "MKImageData"

OUTPUT_DIR = "templatesMade"
TEMPLATE_FILETYPE = ".jpg"


# Class to Store Data about template image
class Template:
    def __init__(self,name,image,cropLocation,tolerance,path):
        self.image = None
        if(type(image) == None):
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

# # Need to Rework these create Functions
# def createPlaces():
#     for i in range(12):
#         frame=getAverageFrame.getAverageFrameColor(scaleImagesToAndBack(getAverageFrame.filesToImage(getAverageFrame.filterPlace(FILES,i+1)),scale))
#         # cv2.imshow('Debug' + str(i+1),frame)
#         cv2.imwrite("PlaceTemplates/" + str(i+1)+f"Place{iscale}.jpg",getAverageFrame.highPass(cropFrame(frame,85, 79, 94.5, 95)))
# def createFinish(scale):
#     frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Finish","Line"]),scale))
#     if(scale==1):
#         scale=""
#     frame = cropFrame(frame,24.1,33,76.1,53)
#     cv2.imwrite(f"Go&Finish/Finish{scale}.jpg",frame)
# def createGo(scale):
#     frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Go!"]),scale))
#     if(scale==1):
#         scale=""
#     frame = cropFrame(frame,36.875,32.625,63.195,54.195)
#     cv2.imwrite(f"Go&Finish/Go!{scale}.jpg",frame)
# def createRankings(scale):
#     frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Rankings"]),scale))
#     if(scale==1):
#         scale=""
#     frame = cropFrame(frame,42.89,6.5,42.89+53.47,14)
#     cv2.imwrite(f"RankTemplates/Rankings{scale}.jpg",frame)
def createPlaces():
    for i in range(12):
        createTemplate(f"{i+1}Place",((1450,758),((1450+164),(758+157))),("race","drive","!placeChange",PLACES_FORMATTED[i]),0.15,"placeTemplates")

# Builds Templates from Queries and Saves a JSON with the other data about it. All Images Used to Make Templates Should be 1280x720 (resize function just in case)
def createTemplate(name,coords,queries,tolerance,path):
    queries
    print(queries)
    fileList = fileService.loadFilesFromQueries(fileService.formatStringsAsPath(BASE_PATH,REFERENCE_DIR),queries)
    for file in fileList:
        print(type(file))
    averageImage = getAverageFrame([cv2.resize(file.fileData,(720,1280)) for file in fileList])
    templateImg = camManager.cropHD(averageImage,coords)
    templateObj = Template(name,templateImg,coords,tolerance,path)
    cv2.imwrite(fileService.formatStringsAsPath(BASE_PATH,OUTPUT_DIR,path,name+TEMPLATE_FILETYPE),templateImg)
    templateJSON = open(fileService.formatStringsAsPath(BASE_PATH,OUTPUT_DIR,path,name+".json"),w)
    templateJSON.write(templateObj.asJson())
    templateJSON.close()
    # if(True not in storeQueried):
    #     fileService.unloadFilesFromNameList([file.name for file in fileList])

# Function to load Template Images and JSONs as template objects. All templates should be saved as .jpg files or otherwise match TEMPLATE_FILETYPE and be in the same directory with same name as corresponding JSON contained in ASSETS_FOLDER as stated in assetManager.py
def loadTemplate(folder,name):
    tempImg = fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder+TEMPLATE_FILETYPE),name)
    tempJSON = fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder+".json"),name)

    templatesList.add(Template.asJson(tempImg,tempJSON))

def constructTemplates():
    createPlaces()
    





