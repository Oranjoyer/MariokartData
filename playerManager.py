import json
from activityManager import activityList
from raceTracker import IndivRace, trackList
from raceTracker import EventDetails
from templateManager import PLACES_FORMATTED
from camManager import VideoSource
from frameAverage import getAverageFrameColor as averageFrame
from trackRecog import new_recog as detectTrack
from playerCount import count_players
import logManager
import time
import cv2

# Sends Log Message with 'PlayerManager' source
def sendMessage(type,message):
    logManager.sendMessage(type, "PlayerManager", message)

# Class that manages each player and their data
playerList = []
class Player:
    def __init__(self,name,vSource):
        self.name = name
        self.vSource = vSource
        vSource.setActivity(True)
        self.imageSamples = []
        self.sampleLen = 3

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
        self.currentRace = None

        self.raceList = []
    def disablePlayer(self):
        self.vSource.setActivity(False)
    def enablePlayer(self):
        self.vSource.setActivity(False)
    def getImage(self):
        if(self.sampleLen <= 1):
            return self.vSource.getImage()
        else:
            self.imageSamples.append(self.vSource.getImage())
            if(len(self.imageSamples)>self.sampleLen):
                self.imageSamples.pop(0)
            average = averageFrame(self.imageSamples)
            return average
    def scanActivity(self):
        # print(activityList)
        for act in activityList:
            # print(act)
            # print(act.checkActivity(self.vSource.getImage(),self.currentActivity))
            if(act.checkActivity(self.vSource.getImage(),self.currentActivity)):
                if(act.name == "CommError"):
                    self.currentActivity = None
                else:
                    if(self.currentActivity != act):
                        sendMessage("Info",f"Player \'{self.name}\' switched activities to \'{act.name}\'")
                    self.currentActivity = act
        if(self.currentActivity != None):
            if(self.currentActivity.name=="TrackLoad"):
                if(self.currentRace == None):
                    track = detectTrack(self.getImage())
                    while(track == None):
                        track = detectTrack(self.getImage())
                        playerCount = count_players(self.getImage())

                    race = IndivRace(self,track)
                    race.playerCount = playerCount
                    self.currentRace = race
            elif(self.currentActivity.name=="Race"):
                if(self.currentRace==None):
                    self.currentRace = IndivRace(self,None)
                if(self.currentRace.startTime == 0):
                    self.currentRace.startTime = time.time()
                # Update Race Conditions
                self.currentRace.scanRace()
            elif((self.currentActivity.name =="RaceEnd") and (self.currentRace != None)):
                # Get The Time the Race Ends
                if(self.currentRace.endTime == 0):
                    self.currentRace.endTime = time.time()
                    self.currentRace.currentTime = self.currentRace.endTime
                    self.currentRace.raceDuration = self.currentRace.endTime-self.currentRace.startTime
                # Get Final Placement Reported 
                if(self.currentRace.finalPlace == 0):
                    finalizedPlacement=self.currentRace.checkPlace()[1]
                    if(finalizedPlacement != 0):
                        self.currentRace.finalPlace = finalizedPlacement
                        trackName = None
                        if(self.currentRace.track != None):
                            trackName = self.currentRace.track.name
                        self.currentRace.eventLog.append(EventDetails.reportEvent(self.currentRace,f"Player \'{self.name}\' finished race on track \'{trackName}\' with {PLACES_FORMATTED[finalizedPlacement]} place"))
    @staticmethod
    def createPlayer(name,camera,crop):
        source = VideoSource(name,camera,crop)
        return Player(name,source)

# def detectTrack(image):
#     # Just Waiting for track detection modules
#     return trackList[0]
def createPlayerFromDict(diction):
    if(type(diction)!=dict & type(diction) == str):
        sendMessage("Info","String passed into \'createPlayer\' function. Attempting to parse as JSON")
        dict = json.parse(dict)
    elif(type(diction)!=str):
        sendMessage("Error","Unsupported Object Passed Into \'createPlayer\' function. Please use dictionary or properly formatted JSON string")
        return None


        