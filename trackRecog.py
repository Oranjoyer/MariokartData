# Credit to Glitcher01

# import pyautogui
import cv2
import os
import fileService
import assetManager
from templateManager import compareFullImg
from raceTracker import trackList as track_key
import numpy as np
# directory = os.fsencode('LoadingScreens')
trackSpriteSheet = None
trackBG = None
board_size = (288, 162)
# track_key = ['Mario Kart Stadium', 'Water Park', 'Sweet Sweet Canyon', 'Thwomp Ruins', 'Mario Circuit', 'Toad Harbor', 'Twisted Mansion', 'Shy Guy Falls', 'Sunshine Airport', 'Dolphin Shoals', 'Electrodrome', 'Mount Wario', 'Cloudtop Cruise', 'Bone-Dry Dunes', "Bowser's Castle", 'Rainbow Road', 'Wii Moo Moo Meadows', 'GBA Mario Circuit', 'DS Cheep Cheep Beach', "N64 Toad's Turnpike", 'GCN Dry Dry Desert', 'SNES Donut Plains 3', 'N64 Royal Raceway', '3DS DK Jungle', 'DS Wario Stadium', 'GCN Sherbet Land', '3DS Music Park', 'N64 Yoshi Valley', 'DS Tick-Tock Clock', '3DS Piranha Plant Slide', 'Wii Grumble Volcano', 'N64 Rainbow Road', 'GCN Yoshi Circuit', 'Excitebike Arena', 'Dragon Driftway', 'Mute City', "Wii Wario's Gold Mine", 'SNES Rainbow Road', 'Ice Ice Outpost', 'Hyrule Circuit', 'GCN Baby Park', 'GBA Cheese Land', 'Wild Woods', 'Animal Crossing', '3DS Neo Bowser City', 'GBA Ribbon Road', 'Super Bell Subway', 'Big Blue', 'Tour Paris Promenade', '3DS Toad Circuit', 'N64 Choco Mountain', 'Wii Coconut Mall', 'Tour Tokyo Blur', 'DS Shroom Ridge', 'GBA Sky Garden', 'Ninja Hideaway', 'Tour New York Minute', 'SNES Mario Circuit 3', 'N64 Kalimari Desert', 'DS Waluigi Pinball', 'Tour Sydney Sprint', 'GBA Snow Land', 'Wii Mushroom Gorge', 'Sky-High Sundae', 'Tour London Loop', 'GBA Boo Lake', '3DS Rock Rock Mountain', 'Wii Maple Treeway', 'Tour Berlin Byways', 'DS Peach Gardens', 'Merry Mountain', '3DS Rainbow Road', 'Tour Amsterdam Drift', 'GBA Riverside Park', 'Wii DK Summit', "Yoshi's Island", 'Tour Bangkok Rush', 'DS Mario Circuit', 'GCN Waluigi Stadium', 'Tour Singapore Speedway', 'Tour Athens Dash', 'GCN Daisy Cruiser', 'Wii Moonview Highway', 'Squeaky Clean Sprint', 'Tour Los Angeles Laps', 'GBA Sunset Wilds', 'Wii Koopa Cape', 'Tour Vancouver Velocity', 'Tour Rome Avanti', 'GCN DK Mountain', 'Wii Daisy Circuit', 'Piranha Plant Cove', 'Tour Madrid Drive', "3DS Rosalina's Ice World", 'SNES Bowser Castle 3', 'Wii Rainbow Road']
# track_key = trackList
def init():
    global trackSpriteSheet
    global trackBG

    trackSpriteSheet = assetManager.getAsset("trackRecog","track-ss.png").fileData
    trackBG = assetManager.getAsset("trackRecog","track-ss.png").fileData

def new_recog(img):
    track_bg = trackBG
    height, width, channels = track_bg.shape
    subdivision_x = [(0, 90), (1382, width)]
    subdivisions = []
    for i in range(0, len(subdivision_x)): # Create subdivisions
        subdivisions.append(track_bg[0:height,subdivision_x[i][0]:subdivision_x[i][1]])
    height, width, channels = img.shape
    if height != 1080 or width != 1920:
        img = cv2.resize(img, (0, 0), fx=1920/width, fy=1080/height)
    img = img[923:1057,224:1696]
    # cv2.imwrite('test-work.png', subdivisions[1])
    for s in subdivisions:
        # print(s)
        try: compareFullImg(s,img,.15)
        except Exception as e:
            print(e)
            return False
    track_ss = trackSpriteSheet
    track_img = img[15:118,1189:1362]
    for row in range(0, 12):
        for col in range(0, 8):
            current_track=track_ss[row * board_size[1]:(row+1) * board_size[1],col * board_size[0]:(col + 1) * board_size[0]]
            height, width, channels = current_track.shape
            current_track = cv2.resize(current_track, (0, 0), fx=223/width, fy=126/height)
            current_track = current_track[15:118,24:197]
            try: 
                if compareFullImg(current_track,track_img,0.15)[0]:
                    return track_key[row * 8 + col]
                    break
            except pyautogui.ImageNotFoundException: # If image doesn't match, move on to next one
                continue

# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     if filename.endswith(".png") or filename.endswith(".jpg"):
#         print(filename + ': ' + new_recog(r'LoadingScreens/' + filename))
#         continue
#     else:
#         continue