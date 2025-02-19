import cv2
import logManager

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "ImageManager",message)

# crops image using percentages as integers
def cropPercent(image, coords):
    frame_height = image.shape[0]
    frame_width = image.shape[1]
    spot1 = [int(frame_width*(coords[0][0]*.01)), int(frame_height*(coords[0][1]*0.01))]
    spot2 = [int(frame_width*coords[1][0]*.01), int(frame_height*coords[1][1]*.01)]
    return image[spot1[1]:spot2[1], spot1[0]:spot2[0]]

# Crop Image with Coordinates but make sure it is scaled to 1280x720 first
def cropHD(image, coords):
    if(image.shape[0:2] != (720,1280)):
            sendMessage("Info", "Resizing image to 1280x720 before cropping")
            image = cv2.resize(image,(1280,720))
    return cropDirect(image, coords)

# Crop Image from Pure Coordinates
def cropDirect(image, coords):
    sendMessage("Debug",f"Cropping Image of shape \'{image.shape}\'with Coordinates Bottom Left:\'{coords[0]}\' Bottom Right:\'{coords[1]}\'")
    return image[coords[0][1]:coords[1][1], coords[0][0]:coords[1][0]]