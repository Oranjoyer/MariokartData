from templateCompare import template
import fileService
import templateCompare
import averageFrame
import cv2
import camManager
import json
from fileService import BASE_PATH
from templateCompare import CoordPair
from templateCompare import Template
TEMPLATE_DIR = "MKImageData"
OUTPUT_DIR = "templatesMade"

# Need to Rework these create Functions
def createPlaces():
    for i in range(12):
        frame=getAverageFrame.getAverageFrameColor(scaleImagesToAndBack(getAverageFrame.filesToImage(getAverageFrame.filterPlace(FILES,i+1)),scale))
        # cv2.imshow('Debug' + str(i+1),frame)
        cv2.imwrite("PlaceTemplates/" + str(i+1)+f"Place{iscale}.jpg",getAverageFrame.highPass(cropFrame(frame,85, 79, 94.5, 95)))
def createFinish(scale):
    frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Finish","Line"]),scale))
    if(scale==1):
        scale=""
    frame = cropFrame(frame,24.1,33,76.1,53)
    cv2.imwrite(f"Go&Finish/Finish{scale}.jpg",frame)
def createGo(scale):
    frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Go!"]),scale))
    if(scale==1):
        scale=""
    frame = cropFrame(frame,36.875,32.625,63.195,54.195)
    cv2.imwrite(f"Go&Finish/Go!{scale}.jpg",frame)
def createRankings(scale):
    frame = getAverageFrame.getAverageFrame(scaleImagesToAndBack(getAverageFrame.imagesFromFilter(FILES,["Rankings"]),scale))
    if(scale==1):
        scale=""
    frame = cropFrame(frame,42.89,6.5,42.89+53.47,14)
    cv2.imwrite(f"RankTemplates/Rankings{scale}.jpg",frame)

# Builds Templates from Queries and Saves a JSON with the other data about it. All Images Used to Make Templates Should be 1280x720 (resize function just in case)
def createTemplate(name,coords,queries,tolerance,path,*storeQueried):
    queries += fileService.IMAGE_EXTENSIONS
    fileList = fileService.loadFilesFromQueries(queries)
    averageImage = averageFrame.getAverageFrame([cv2.resize(file.fileData,1280,720) for file in fileList])
    templateImg = camManager.cropHD(averageFrame,coords)
    templateObj = Template(name,templateImg,coords,tolerance,path)
    cv2.imwrite(fileService.formatStringsAsPath(BASE_PATH,OUTPUT_DIR,path,name+".jpg"),templateImg)
    templateJSON = open(fileService.formatStringsAsPath(BASE_PATH,OUTPUT_DIR,path,name+".json"),w)
    templateJSON.write(templateObj.asJson())
    templateJSON.close()
    if(True not in storeQueried):
        fileService.unloadFilesFromNameList([file.name for file in fileList])


