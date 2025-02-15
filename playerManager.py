import json
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

def createPlayerFromDict(diction):
    if(type(diction)!=dict & type(diction) == str):
        sendMessage("Info","String passed into \'createPlayer\' function. Attempting to parse as JSON")
        dict = json.parse(dict)
    elif(type(diction)!=str):
        sendMessage("Error","Unsupported Object Passed Into \'createPlayer\' function. Please use dictionary or properly formatted JSON string")
        return None

        