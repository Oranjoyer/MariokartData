import asyncio
import fileService
from fileService import BASE_PATH
import logManager

ASSETS_FOLDER = "assets"
PLACE_TEMPLATE_FOLDER = "placeTemplates"
RACE_PROGRESS_FOLDER = "raceProgress"
RESULT_FOLDER = "result"
DATA_FOLDER = "dataSets"

TEMPLATE_FOLDERS = (PLACE_TEMPLATE_FOLDER,RACE_PROGRESS_FOLDER,RESULT_FOLDER)

# Simplifies Function to Retrieve Asset files from the filesystem
async def getAsset(folder,name):
    if(await fileService.loadFile(fileService.formatStringsAsPath(BASE_PATH,ASSETS_FOLDER,folder)+name,name)==None):
        sendMessage("Error",f"Asset \'{name}\' failed to load")
    else:
        sendMessage("Info",f"Asset \'{name}\' successfully loaded")

# Send Message to Logs
def sendMessage(type,message):
    logManager.sendMessage(type, "AssetManager",message)

# Gather Template Files and Place in FileService
def obtainTemplateAssets():
# Calls Every "ObtainTemplate" Function
    asyncio.run(obtainPlaceTemplates())
    asyncio.run(obtainRaceProgressTemplates())
    asyncio.run(obtainResultsTemplates())

# Collect Every Race Progress Indicator Template from Folder
async def obtainRaceProgressTemplates():
    await getAsset(RACE_PROGRESS_FOLDER,"Go.jpg")
    await getAsset(RACE_PROGRESS_FOLDER,"Finish.jpg")

# Collect Every Place Template Image from Folder
async def obtainPlaceTemplates():
    for i in range(12):
        await getAsset(PLACE_TEMPLATE_FOLDER,f"{i+1}Place.jpg")

# Collect Result Screen Templates
async def obtainResultsTemplates():
    await getAsset(RESULT_FOLDER,"TeamPoints.jpg")
async def getTrackCSV():
    await getAsset(DATA_FOLDER,"trackStrats.csv")



# Initializes all needed resources for this module
def init():
    obtainTemplateAssets()
    asyncio.run(getTrackCSV())