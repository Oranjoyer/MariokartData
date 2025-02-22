# import asyncio
import fileService
from fileService import BASE_PATH, ASSETS_FOLDER, PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RESULT_FOLDER,DATA_FOLDER,RACE_DATA_FOLDER
import logManager
import templateManager
from templateManager import placeTemplateList, lapTemplateList, coinTemplateList

TEMPLATE_FOLDERS = (PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RESULT_FOLDER)



# Simplifies Function to Retrieve Asset files from the filesystem
def getAsset(folder,name):
    asset = fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder)+name,name)
    if(asset==None):
        sendMessage("Error",f"Asset \'{name}\' failed to load")
    else:
        sendMessage("Info",f"Asset \'{name}\' successfully loaded")
        return asset

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "AssetManager",message)

# Gather Template Files and Place in FileService
def obtainTemplateAssets():
# Calls Every "ObtainTemplate" Function
    obtainPlaceTemplates()
    obtainRaceProgressTemplates()
    obtainResultsTemplates()
    obtainCoinTemplates()

# Collect Every Race Progress Indicator Template from Folder
def obtainRaceProgressTemplates():
    templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,RACE_PROGRESS_FOLDER),"Go")
    templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,RACE_PROGRESS_FOLDER),"Finish")
    for i in range(3):
        lapTemplateList.append(templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,RACE_PROGRESS_FOLDER),f"Lap{i+1}"))
    templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,RACE_PROGRESS_FOLDER),"TrackLoad")

# Collect Every Place Template Image from Folder
def obtainPlaceTemplates():
    for i in range(12):
        placeTemplateList.append(templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,PLACE_TEMPLATE_FOLDER),f"{i+1}Place"))
    sendMessage("Info",f"Loaded Place Templates Into Memory {[t.name for t in placeTemplateList]}")

# Collect Every Coin Template Image from Folder
def obtainCoinTemplates():
    for i in range(11):
        coinTemplateList.append(templateManager.loadTemplate(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,RACE_DATA_FOLDER),f"{i}Coin"))
    sendMessage("Info",f"Loaded Coin Templates Into Memory {[t.name for t in placeTemplateList]}")

# Collect Result Screen Templates
def obtainResultsTemplates():
    getAsset(RESULT_FOLDER,"TeamPoints.jpg")
def getTrackCSV():
    getAsset(DATA_FOLDER,"trackStrats.csv")



# Initializes all needed resources for this module
def init():
    obtainTemplateAssets()
    getAsset(".","placeholder.png")
    getTrackCSV()