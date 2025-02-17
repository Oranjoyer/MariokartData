import json
from activityManager import activityList
from raceTracker import IndivRace
import time
# Class that manages each player and their data
playerList = []
class Player:
    def __init__(name,vSource):
        self.name = name
        self.vSource = vSource

        # Default Initialization of Player's Combo, will be changed post Init with gui
        self.character = "Mario"
        self.kart = "Standard Kart"
        self.wheels = "Standard"
        self.glider = "Super Glider"
        
        # Other Player Info
        self.currentActivity = None
        self.points = -1
        self.vr = -1
        self.placesRec = []
        self.teamColor = None
        self.inRace = False
        self.currentRace = None

        self.raceList = []
    def getImage(self):
        return self.vSource.getImage()
    def scanActivity(self):
        for act in activityList:
            if(act.checkActivity(self.vSource.getImage(),self.currentActivity)):
                if(act.name == "CommError"):
                    self.currentActivity = None
                else:
                    self.currentActivity = act
        if(self.currentActivity.name=="TrackLoad"):
            if(self.currentRace == None):
                track = detectTrack(self.getImage())

                self.currentRace = IndivRace(self,track)
        elif(self.currentActivity.name=="Race"):
            if(self.currentRace.startTime == 0):
                self.currentRace.startTime = time.time()
            # Update Race Conditions
            self.currentRace.scanRace()
        elif(self.currentActivity.name =="RaceEnd"):
            # Get The Time the Race Ends
            if(self.currentRace.endTime == 0):
                self.currentRace.endTime = time.time()
                self.currentRace.currentTime = self.currentRace.endTime
                self.currentRace.raceDuration = self.currentRace.endTime-self.currentRace.startTime
            # Get Final Placement Reported 
            if(self.currentRace.finalPlace == 0):
                self.currentRace.finalPlace = self.currentRace.checkPlace()

def createPlayerFromDict(diction):
    if(type(diction)!=dict & type(diction) == str):
        sendMessage("Info","String passed into \'createPlayer\' function. Attempting to parse as JSON")
        dict = json.parse(dict)
    elif(type(diction)!=str):
        sendMessage("Error","Unsupported Object Passed Into \'createPlayer\' function. Please use dictionary or properly formatted JSON string")
        return None


        