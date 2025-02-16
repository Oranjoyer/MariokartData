# import asyncio
import fileService
from fileService import BASE_PATH, ASSETS_FOLDER, PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RESULT_FOLDER,DATA_FOLDER
import logManager
import templateManager

TEMPLATE_FOLDERS = (PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RESULT_FOLDER)

# Simplifies Function to Retrieve Asset files from the filesystem
def getAsset(folder,name):
    if(fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder)+name,name)==None):
        sendMessage("Error",f"Asset \'{name}\' failed to load")
    else:
        sendMessage("Info",f"Asset \'{name}\' successfully loaded")

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "AssetManager",message)

# Gather Template Files and Place in FileService
def obtainTemplateAssets():
# Calls Every "ObtainTemplate" Function
    obtainPlaceTemplates()
    obtainRaceProgressTemplates()
    obtainResultsTemplates()

# Collect Every Race Progress Indicator Template from Folder
def obtainRaceProgressTemplates():
    getAsset(RACE_PROGRESS_FOLDER,"Go.jpg")
    getAsset(RACE_PROGRESS_FOLDER,"Finish.jpg")

# Collect Every Place Template Image from Folder
def obtainPlaceTemplates():
    for i in range(12):
        templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,PLACE_TEMPLATE_FOLDER),f"{i+1}Place")

# Collect Result Screen Templates
def obtainResultsTemplates():
    getAsset(RESULT_FOLDER,"TeamPoints.jpg")
def getTrackCSV():
    getAsset(DATA_FOLDER,"trackStrats.csv")



# Initializes all needed resources for this module
def init():
    obtainTemplateAssets()
    getTrackCSV()