# import flask
# import flexx
import numpy as np
import cv2
import camManager
import logManager
import assetManager
from templateManager import constructTemplates

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

# constructTemplates()
main()