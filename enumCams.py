import cv2

MAX_FAIL = 10
class CamInfo:
    def __init__(self,index,name):
        self.name = name
        self.index = index
def enumerate_cameras(capMethod):
    index = 0
    borked = 0
    camList = []
    while borked < MAX_FAIL:
            print(f"checking index {index}")
            cam = cv2.VideoCapture(index,capMethod)
            if(cam.isOpened()):
                camList.append(CamInfo(index,f"Camera{index}"))
            else:
                borked += 1
            index += 1
    return camList
