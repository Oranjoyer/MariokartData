# import flask
# import flexx
import numpy as np
import cv2
import camManager
import logManager

INIT = False

# Executes Init Functions Of all Modules
def init():
    camManager.init()
    templateCompare.init()
    global INIT
    INIT = True

def main():
    init()
    return

main()