import cv2

MAX_FAIL = 10

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "CameraEnumerator",message)

class CamInfo:
    def __init__(self,index,name):
        self.name = name
        self.index = index
def enumerate_cameras(capMethod):
    index = 0
    borked = 0
    camList = []
    while borked < MAX_FAIL:
            sendMessage(f"checking camera index \'{index}\'")
            cam = cv2.VideoCapture(index,capMethod)
            if(cam.isOpened()):
                print(cam.read()[0])
                camList.append(CamInfo(index,f"Camera{index}"))
                cam.release()
            else:
                borked += 1
            index += 1
    return camList
