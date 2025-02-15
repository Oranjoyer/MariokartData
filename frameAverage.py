

# Get Average Frame but Edge Detection
def getAverageFrame(frameList):
    # averageFrame = np.zeros((720,1280), np.uint8)
    # global DEBUG
    if len(frameLine) < 1:
        return np.zeros((720,1280), np.uint8)
    averageFrame = highPass(frameLine[0])
    for i in range(len(frameLine)-1):
        averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), highPass(frameLine[i+1]), getWeight(i),0.0)
    return cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Function to get the weight of a new element added to an average
def getWeight(iterations):
    base = 1/(iterations+2)
    return base


# Average Frames but Keep full color
def getAverageFrameColor(frameLine):
    if len(frameLine) < 1:
        return np.zeros((720,1280), np.uint8)
    averageFrame = frameLine[0]
    for i in range(len(frameLine)-1):
        averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), frameLine[i+1], getWeight(i),0.0)
            # cv2.destroyWindow("Debug")
    # return cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return averageFrame


def highPass(frame):
    passF = frame - cv2.GaussianBlur(frame,(21,21),3)+127
    if(len(passF.shape)>2):
        passF = cv2.cvtColor(passF, cv2.COLOR_BGR2GRAY)
    passF = cv2.Laplacian(passF, -1)
    return passF
def grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
def colorPass(frame):
    passF = frame
    passF = passF - cv2.GaussianBlur(passF,(21,21),3)+127
    passF = cv2.Laplacian(passF, -1)

    return passF