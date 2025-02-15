import time
import json

class Track:
    def __init__(name,trackType,strategy):
        self.name = name
        self.trackType = trackType
        self.strategy = strategy
class eventDetails:
    def __init__(self,timeOccur, raceJSON, description):
        self.timeOccur = timeOccur
        self.conditions = raceJSON
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


    def getPlayer(self, name):
        for race in races:
            if(name == race.player.name):
                sendMessage()
