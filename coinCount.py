import cv2
from templateManager import getLoadedTemplate
from statistics import mean
threeHoriCoords = ((128,656), (128,670), (128,682))
LeftVertCoords = ((120,663),(120,674))
RightVertCoords= ((136,663),(136,674))
TOLERANCE = 100
MIN_BRIGHT = 200


CoordList = (threeHoriCoords[0],LeftVertCoords[0],threeHoriCoords[1],RightVertCoords[0],LeftVertCoords[1],threeHoriCoords[2],RightVertCoords[1])
# Order of Segments: TopMiddle,TopLeft,Center,TopRight,BottomLeft,BottomMiddle,BottomRight
NUM_LIST = (
(True,True,False,True,True,True,True), #0
(False,True,False,True,True,False,True), #1
(True,False,True,True,True,True,False), #2
(True,False,True,True,False,True,True), #3
(False,True,True,True,False,False,True), #4
(True,True,True,False,False,True,True), #5
(True,True,True,False,True,True,True), #6
(True,False,False,True,False,False,True), #7
(True,True,True,True,True,True,True), #8
(True,True,True,True,False,True,True), #9
) # I'm Lazy so 10 is just template matching



def countCoins(img):
    maxCoinTemplate = getLoadedTemplate("10Coin")
    if(maxCoinTemplate.compareWithImage(img,0)[0]):
        return 10
    return sevSegDecode(img)




def sevSegDecode(img):
    segList = []
    for coord in CoordList:
        segList.append(isSegment(img,coord,TOLERANCE))
    segList4One = []
    for coord in [(c[0] - 8,c[1]) for c in CoordList]:
        segList4One.append(isSegment(img,coord,TOLERANCE))
    
    
    index = 0
    for num in NUM_LIST:
        if(index == 1 and tuple(segList4One) == num):
            return index
        if(tuple(segList)==num):
            return index
        index += 1
    return -1

def isSegment(img,coords,tolerance):
    firstColorVal = img[coords[1]][coords[0]][0]
    if(firstColorVal<MIN_BRIGHT):
        return False
    aveBright = mean(img[coords[1]][coords[0]])
    distFirstVal = abs(aveBright-firstColorVal)
    # print(distFirstVal)
    if(distFirstVal <= tolerance):
        return True
        