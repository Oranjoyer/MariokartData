import cv2
import numpy as np
import fileService
from fileService import BASE_PATH
from camManager import cropDirect
from templateManager import Template, edgeDetect, grayscale
import logManager
    
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