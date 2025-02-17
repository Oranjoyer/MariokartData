from templateManager import getLoadedTemplate

activityList = []

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
        print(f"Checking for Activity \'{self.name}\'")
        if((current != None) and not(isAvailable(current))):
            return False
        for template in self.coreTemplates:
            if(template.compareWithImage(img),0):
                return True
        return False

def collectActivities():
    activityList.append(Activity("TrackLoad",None,[getLoadedTemplate("TrackLoad")]))
    activityList.append(Activity("Race",["TrackLoad"],[getLoadedTemplate("Go")]))
    activityList.append(Activity("RaceEnd",["Race"],[getLoadedTemplate("Finish")]))