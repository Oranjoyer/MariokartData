import time
import json
import csv
import fileService
import logManager
from fileService import BASE_PATH
from templateManager import placeTemplateList, lapTemplateList,coinTemplateList
from templateManager import PLACES_FORMATTED
from templateManager import bulkCompare
from coinCount import countCoins
import statistics
import cv2
from io import StringIO
trackList = []


# Sends Log Message with 'RaceTracker' source
def sendMessage(type,message):
    logManager.sendMessage(type, "RaceTracker", message)
def init():
    generateTrackList()

def generateTrackList():
    trackStrats = fileService.getFileByName("trackStrats.csv").fileData
    for trackDict in trackStrats:
        trackList.append(Track(trackDict["course_num"],trackDict["course_name"],trackDict["course_type"],trackDict["best_start"],trackDict["description"]))





class Track:
    def __init__(self,trackNum,name,trackType,bestStartSpot,description):
        self.trackNum = trackNum
        self.name = name
        self.trackType = trackType
        self.bestStartSpot = bestStartSpot
        self.description = description

class EventDetails:
    def __init__(self, raceDict, description):
        self.timeOccur = time.ctime(raceDict["currentTime"])
        self.timeElapsed = raceDict["currentTime"]-raceDict["startTime"]
        self.conditions = raceDict
        self.description = description
    
    @staticmethod
    def reportEvent(race,description):
        sendMessage("Info",description)
        return EventDetails(race.outputCurrentAsDict(),description)

class IndivRace:
    def __init__(self,player,track):
        self.player = player
        self.track = track
        self.startTime = 0
        self.currentTime = 0
        self.endTime = 0
        self.raceDuration = 0
        self.eventLog = []
        self.finalPlace = 0
        self.playerCount = 12

        # Mid Race Info
        self.items = (None,None)
        self.lap = 1
        self.coins = 0
        self.hitsDetected = 0
        self.place = 0
        self.totalCoins = 0

        self.voteLim = 5
        self.coinVote = tuple(0 for _ in range(self.voteLim))

    def reportEvent(self,description):
        self.eventLog.append(EventDetails.reportEvent(self,description))
    # Output Current Race Conditons As Json
    def outputCurrentAsDict(self):
        dictionary = self.__dict__
        # dictionary = dictionary.pop("eventLog")
        return dictionary
    # Update Race Time
    def updateTime():
        self.currentTime = time.time()
        self.raceDuration = self.currentTime - self.startTime
    # Obtain Current Race Conditions
    def scanRace(self):
        self.scanPlace()
        self.scanLaps()
        self.scanCoins()

    def checkPlace(self):
        matchedPlaceTemplate = bulkCompare(placeTemplateList,self.player.getImage(),0)
        placeMatch = matchedPlaceTemplate[2]+1
        return matchedPlaceTemplate,placeMatch
        
    # Check Current Screen for Change in Placement
    def scanPlace(self):
        matchedPlaceTemplate,placeMatch = self.checkPlace()
        if((matchedPlaceTemplate[0] != None) and (placeMatch != self.place)):
            self.place = placeMatch
            eventString = f"Player \'{self.player.name}\' moved to {PLACES_FORMATTED[placeMatch-1]} place"
            self.eventLog.append(EventDetails.reportEvent(self,eventString))

    def scanLaps(self):
        playerImg = self.player.vSource.getImage()
        if(not((self.lap >= 3) and (self.track != None and self.track.name == "Baby Park")) and (self.lap >= len(lapTemplateList))):
            return
        nextLapTemplate = lapTemplateList[self.lap]
        nextCompare = nextLapTemplate.compareWithImage(self.player.getImage(),0)

        currentTemplate = lapTemplateList[self.lap-1]
        if(nextCompare[0] and (nextCompare[1] > currentTemplate.compareWithImage(self.player.getImage(),0)[1])):
            self.lap += 1
            self.eventLog.append(EventDetails.reportEvent(self,f"Player \'{self.player.name}\' moved to lap {self.lap}"))
    
    def scanCoins(self):
        playerImg = self.player.vSource.getImage()
        coinMatch = countCoins(playerImg)
        # lowCoin = max(self.coins-3, 0)
        
        if(coinMatch!=-1):
            self.coinVote = addToLine(coinMatch,self.coinVote,self.voteLim)

        if(self.coinVote[0] != self.coins and self.coinVote.count(self.coinVote[0]) > self.voteLim/2):
            if(self.coinVote[0]<self.coins):
                self.coins = self.coinVote[0]
                self.hitsDetected +=1
                self.reportEvent(f"Player \'{self.player.name}\' coins decreased to {self.coins}: {coinMatch}")
            elif(self.coinVote[0] > self.coins):
                self.coins = self.coinVote[0]
                self.reportEvent(f"Player \'{self.player.name}\' coins increased to {self.coins}: {coinMatch}")



def allSame(listItems):
    if(all(item == listItems[0] for item in listItems)):
        return listItems[0]
def addToLine(elem,items,lim):
    return (elem,) + (items[:lim]) 


# Class Which calculates values related to a race that includes multiple players
class JointRace:
    def __init__(*raceInstances):
        races = [race for race in raceInstances]
        self.startTime = min([race.startTime for race in races])
        self.endTime = max([race.endTime for race in races])
        self.totalDuration = self.endTime - self.startTime
        self.track = raceInstances[0].track
        self.players = [race.player for race in raceInstances]

        # Input Validation
        for race in raceInstances:
            if(race.track != self.track):
                sendMessage("Error","\'JointRace\' creation with races that have different track. THIS SHOULD NEVER HAPPEN")


        self.averagePlace = sum([race.place for race in raceInstances])/len(raceInstances)

        def __str__(self):
            return f"Track: {self.track.name}\nPlayers: {[player.name for player in self.players]}\nDuration: {self.totalDuration} seconds\nStart Time: {time.ctime(self.startTime)}\nEnd Time: {time.ctime(self.endTime)}"



    def getPlayer(self, name):
        for race in self.races:
            if(name == race.player.name):
                sendMessage("Info",f"Player {name} found in race on track \'{self.track}\' that took place on {time.ctime(self.startTime)} and lasted {self.endTime-self.startTime} seconds")
                return race.player 
        sendMessage("Warning",f"Player {name} not found in race on track \'{self.track}\' that took place on {time.ctime(self.startTime)} and lasted {self.endTime-self.startTime} seconds")

