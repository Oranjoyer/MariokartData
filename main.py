# import flask
# import flexx
import numpy as np
import cv2
import camManager
import logManager
import assetManager
import raceTracker
import activityManager
import templateManager
from templateManager import constructTemplates
from playerManager import Player
from frameAverage import edgeDetect
from threading import Thread
import trackRecog
INIT = False

# Executes Init Functions Of all Modules
def init():
    assetManager.init()
    camManager.init()
    raceTracker.init()
    activityManager.init()
    trackRecog.init()
    global INIT
    INIT = True
def constantCamUpdate():
    while True:
        camManager.updateCameraImages()
def main():
    init()
    thread = Thread(target=constantCamUpdate)
    thread.start()
    players = []
    for i in range(1):
        players.append(Player.createPlayer(f"Player{i+1}",camManager.cameras[0],((0,0),(100,100))))
    for p in players:    
            # print(p.name)
        Thread(target=functionForever, args=(p,)).start()
        # cv2.waitKey(1)
    while True:
        cv2.imshow("Raw",camManager.cameras[0].currentImage)
        # print(f"High: {camManager.cameras[0].currentImage[656][128]}")
        # print(f"Low: {camManager.cameras[0].currentImage[682][128]}")
        cv2.waitKey(1)
        
    # test = cv2.VideoCapture(0,cv2.CAP_ANY)
    # ret, img = test.read()
    # ret, img = test.read()

    # print(ret)
    # print(img)
    # cv2.imwrite("test.jpg",img)
    return

def functionForever(p):
    while True:
        p.scanActivity()
        # print(p.currentRace)
        # print(p.getImage())
# constructTemplates()
main()