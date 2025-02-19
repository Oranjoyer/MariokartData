# Credit to Glitcher01

import cv2
# import os

# directory = os.fsencode('LoadingScreens')
player_size = (865, 128)

def count_players(img):
    height, width, channels = img.shape
    if width != 1920 or height != 1080:
        img = cv2.resize(img, (0, 0), fx=1920/width, fy=1080/height)
    player_count = 0
    img = img[86:874,94:1829]
    while player_count < 12:
        current_box = img[4 * (player_count % 6) + player_size[1] * (player_count % 6):4 * (player_count % 6) + player_size[1] * ((player_count % 6) + 1), (player_count >= 6) * 871:(player_count >= 6) * 871 + player_size[0]]
        if (all(v == 0 for v in current_box[player_size[1] // 2, player_size[0] // 2])):
            break
        player_count += 1
    return player_count

# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     if filename.endswith(".png") or filename.endswith(".jpg"):
#         print(filename + ': ', end='')
#         print(count_players('LoadingScreens/' + filename))
#         continue
#     else:
#         continue