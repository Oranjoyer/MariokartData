from camManager import VideoSource

templateScreens = []

# Scans Image to determine what the current screen is. If the program does not have an idea of the current screen, cross-references with all available screen templates
def getScreenType(Source):
    if(Source.currentScreen == None):
        compareAllScreens(Source)
    
def compareAllScreens(Source):
    for template in templateScreens:
        sendMessage("NONE","Function Not Implemented")
        return

def CollectTemplateScreens():
    sendMessage("NONE","Function Not Implemented")
    return