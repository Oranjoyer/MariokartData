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
from threading import Thread
INIT = False

# Executes Init Functions Of all Modules
def init():
    camManager.init()
    assetManager.init()
    raceTracker.init()
    global INIT
    INIT = True
def constantCamUpdate():
    while True:
        camManager.updateCameraImages()
def main():
    thread = Thread(target=constantCamUpdate)
    thread.start
    init()
    player = Player.createPlayer("Grant",camManager.cameras[0],((0,0),(100,100)))
    while True:
        player.scanActivity()
    # cv2.imwrite("test.jpg",cv2.VideoCapture(0,cv2.CAP_V4L2).read()[1])
    return

# constructTemplates()
main()