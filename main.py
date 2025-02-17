# import flask
# import flexx
import numpy as np
import cv2
import camManager
import logManager
import assetManager
import raceTracker
from templateManager import constructTemplates
from playerManager import Player
INIT = False

# Executes Init Functions Of all Modules
def init():
    camManager.init()
    assetManager.init()
    raceTracker.init()
    global INIT
    INIT = True

def main():
    init()
    Player.createPlayer("Grant",camManager.cameras[0],((0,0),(100,100)))
    return

# constructTemplates()
main()