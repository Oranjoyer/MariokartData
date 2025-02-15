import time
import json
import fileService
from fileService import BASE_PATH

# Sends Log Message with 'RaceTracker' source
def sendMessage(type,message):
    logManager.sendMessage(type, "RaceTracker", message)
def init():
    asyncio.run(fileService.loadFile())


class Track:
    def __init__(name,trackType,strategy,bestStartSpot):
        self.name = name
        self.trackType = trackType
        self.strategy = strategy
        self.bestStartSpot = bestStartSpot
class eventDetails:
    def __init__(self,timeOccur, raceDict, description):
        self.timeOccur = time.ctime(raceDict["endTime"])
        self.timeElapsed = raceDict["endTime"]-raceDict["startTime"]
        self.conditions = raceDict
        self.description = description

class IndivRace:
    def __init__(self,player,track, start):
        self.player = player
        self.track = track
        self.startTime = start
        self.endTime = None
        self.raceDuration = end-start
        self.eventLog = []

        # Mid Race Info
        self.items = (None,None)
        self.lap = 0
        self.coins = 0
        self.track = None
        self.place = 0
    # Output Current Race Conditons As Json
    def outputCurrentAsDict(self):
        dictionary = __dict__()
        dictionary = dictionary.pop("eventLog")
        return dictionary

# Class Which calculates values related to a race that includes multiple players
class JointRace:
    def __init__(*raceInstances):
        races = [race for race in raceInstances]
        self.startTime = min([race.startTime for race in races])
        self.endTime = max([race.endTime for race in races])
        self.track = raceInstances[0].track

        # Input Validation
        for race in raceInstances:
            if(race.track != self.track):
                sendMessage("Error","\'JointRace\' creation with races that have different track. THIS SHOULD NEVER HAPPEN")


        self.averagePlace 


    def getPlayer(self, name):
        for race in races:
            if(name == race.player.name):
                sendMessage("Info",f"Player {name} found in race on track \'{self.track}\' that took place on {time.ctime(self.startTime)} and lasted {self.endTime-self.startTime} seconds")
                return race.player 
        sendMessage("Warning",f"Player {name} not found in race on track \'{self.track}\' that took place on {time.ctime(self.startTime)} and lasted {self.endTime-self.startTime} seconds")

