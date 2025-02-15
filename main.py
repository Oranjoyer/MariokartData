# import flask
# import flexx
import numpy as np
import cv2
import camManager
import logManager
import templateCompare
import assetManager

INIT = False

# Executes Init Functions Of all Modules
def init():
    camManager.init()
    assetManager.init()
    global INIT
    INIT = True

def main():
    init()
    return

main()