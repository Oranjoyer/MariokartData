from templateManager import getLoadedTemplate
import logManager
import cv2

activityList = []

def sendMessage(type, message):
    logManager.sendMessage(type,"ActivityManager",message)
class Activity:
    def __init__(self,name,preReq,coreTemplates):
        self.name = name
        self.preReq = preReq
        self.templates = coreTemplates # templates that are telltale signs of this activity

    # Check If Activity Can Occur
    def isAvailable(self,current):
        if(self.preReq == None):
            return True
        if(type(current)==Activity):
            current = current.name
        return current in self.preReq
    
    # Check Whether Activity Is Occurring 
    def checkActivity(self,img,current):
        if((current != None) and not(self.isAvailable(current))):
            return False
        sendMessage("Debug",f"Checking for Activity \'{self.name}\'")
        for template in self.templates:
        #     cv2.imshow("CurrentIMG",img)
            if(template.compareWithImage(img,0)[0]):
                return True
        return False

def collectActivities():
    activityList.append(Activity("TrackLoad",None,[getLoadedTemplate("TrackLoad")]))
    activityList.append(Activity("Race",["TrackLoad"],[getLoadedTemplate("Go")]))
    activityList.append(Activity("RaceEnd",["Race"],[getLoadedTemplate("Finish")]))

def init():
    collectActivities()