from templateCompare import template

TEMPLATE_DIR = "MKImageData"

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
def scaleImagesToAndBack(images,scale):
     imageList = []
     for image in images:
          imageList.append(scaleSingleToAndBack(image,scale))
     return imageList