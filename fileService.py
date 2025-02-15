import asyncio
import os
import logManager
import cv2

IMAGE_EXTENSIONS={".jpg",".gif",".png",".tiff",".svg"}
BASE_PATH=""
fileList = []
# Class That Stores Data associated with a file. Formats as the proper filetype 
class FileContainer:
    def __init__(self,name,file,path,typeOf):
        self.name = name
        self.path = path
        if(type(file)==file):
            self.fileData = file.read()
            file.close()
        if(typeOf == "Text"):
            self.fileData = self.fileData.decode("utf-8")
        elif(typeOf == "Image"):
            self.fileData = cv2.imdecode(self.fileData)
        else:
            self.fileData = file


# Sends Log Message with 'FileService' source
def sendMessage(type,message):
    logManager.sendMessage(type, "FileService", message)

# Loads file into memory or retrieves file from list; returns file
async def loadFile(filePath,name):
    # sendMessage("Info", "Checking for preloaded files; disregard 2 potential error messages")
    nameFile = getFileByName(name)
    pathFile = getFileByPath(filePath)
    fileType = "Bytes"
    for imgExt in IMAGE_EXTENSIONS:
        if(imgExt in filePath[-len(imgExt)]):
            fileType = "Image"
    if(nameFile != None):
        sendMessage("Info",f"File by name \'{name}\' already loaded. Retrieving preloaded file instead")
        return getFileByName(name)
    elif(pathFile != None):
        sendMessage("Info",f"File at path \'{path}\' already loaded. Retrieving preloaded file instead")
        return getFileByPath(filePath)
    if(os.path.isfile(filePath)):
        sendMessage("Error",f"No file at path \'{filePath}\' returning null value instead of loading file")
        return None
    if(not(os.access(filePath, os.R_OK))):
        sendMessage("Error",f"Insufficient permissions to load file at path \'{filePath}\' returning null value instead of loading file")
        return None
    loadedFile = FileContainer(name,file.open(filePath, rb),filePath,fileType)
    fileList.append(loadedFile)
    return loadedFile

# Stores file from bytes or retrieves file with desired name
def loadFileFromMemory(fileData,name,fileType):
    # sendMessage("Info", "Checking for preloaded files; disregard 1 potential error messages")
    nameFile = getFileByName(name)
    if(nameFile != None):
        sendMessage("Info", f"File by name \'{name}\' already loaded. Retrieving preloaded file instead")
        return getFileByName(name)

    loadedFile = FileContainer(name,fileBytes,"From Memory",fileType)
    fileList.append(loadedFile)
    return loadedFile

# Retrieves stored file with specific name
def getFileByName(name):
    for file in fileList:
        if(file.name == name):
            return file
    sendMessage("Error", f"No preloaded file found with name \'{name}\' returning null value instead")
    return None

# Retrieves stored file with specific path
def getFileByPath(path):
    for file in fileList:
        if(file.path == path):
            return file
    sendMessage("Error", f"No preloaded file found with path \'{path}\' returning null value instead")
    return None

# Retrieves Index value in list of stored file with specific name
def getFileIndexByName(name):
    for i in range(fileList.len()):
        if(fileList[i].name==name):
            return i
    sendMessage("Error", f"No preloaded file found with name \'{name}\' returning null index instead")
    return -1

# Retrieves Index value in list of stored file with specific path
def getFileIndexByPath(path):
    for i in range(fileList.len()):
        if(fileList[i].path==path):
            return i
    sendMessage("Error",f"No preloaded file found with path \'{path}\' returning null index instead")
    return -1

# Unloads file with specific name from memory
def unloadFileByName(name):
    fileIndex = getFileIndexByName(name)
    if(fileIndex == -1):
        sendMessage("Error",f"No preloaded file found with name \'{name}\' removing no files from memory")
        return
    fileList[fileIndex].file.close()
    fileList.pop(fileIndex)
    sendMessage("Info",f"Successfully removed file with name \'{name}\' from memory")
    return

# Removes file with specific path from memory
def unloadFileByPath(path):
    fileIndex = getFileIndexByPath(path)
    if(fileIndex == -1):
        sendMessage("Error",f"No preloaded file found with path \'{path}\' removing no files from memory")
        return
    fileList[fileIndex].file.close()
    fileList.pop(fileIndex)
    sendMessage("Info",f"Successfully removed file with path \'{path}\' from memory")
    return

# Finds Files in Directory based on Query list. Including a '!' as the first character and then the query wrapped in quotes marks exclusion
def listFilesInDir(dir,*queries):
    allInDir = os.listdir(dir)
    files = [f for f in allInDir if(isFile(f))]

    for q in queries:
        removeString = False
        currentQuery = q
        if(f[0]=="!"):
            removeString = True
            currentQuery = stringInQuotes(f[1:])[0]
        for f in allInDir:
            if(not(checkStringForQuery(f,currentQuery,not(removeString)))):
                allInDir.remove(f)
                
                if(removeString):
                    sendMessage("ExInfo",f"File \'{f}\' filtered out of search list excluding for \'{currentQuery}\'")
                else:
                    sendMessage("ExInfo",f"File \'{f}\' filtered out of search list due to not including \'\'")
    return allInDir

# Loads Files from Directory into the FileService based on Query list. Including a '!' as the first character and then the query wrapped in quotes marks exclusion
def loadFilesFromList(dir, *fileList):
    if (dir[-1]!= "/") | (dir[-1] != "\\"):
        dir.append("/")
    for f in fileList:
        loadFile(dir+f,f)

# Loads All Files in a Directory based on Query List. Including a '!' as the first character and then the query wrapped in quotes marks exclusion 
def loadFilesFromQueries(dir,*queries):
    sendMessage("Info",f"Loading all files found in directory \'{dir}\' based on queries: {queries}")
    loadFilesFromList(dir,listFilesInDir(dir,queries))

# Formats Multiple Strings as proper Path
def formatStringsAsPath(*str):
    path = ""
    for s in str:
        path += s + "/"
    return path

# Checks whether string has or doesn't have a query based on whether it is desired
def checkStringForQuery(str,query,desired):
    if(str.contain(query)):
        return desired
    return not(desired)

# Returns all the characters contained in quotes within a string as a list of groups. If String does not contain quotes, the function will return the passed string
def stringInQuotes(str):
    strList = []
    currentString = ""
    startQuote = False
    quoteType = ''
    if(not(str.contain("\'") | str.contain("\""))):
        sendMessage("Warning",f"String \'{str}\' passed into \'stringInQuotes\' function without any quotes. Returning string as is")
        return str
    elif(totalQuotes(str)%2!=0):
        sendMessage("Warning",f"String \'{str}\' passed into \'stringInQuotes\' function with odd number of quotes. String may not format properly. Avoid adding extra quotes in String")
    for letter in str:
        if((letter == '\'' | letter == '\"') & startQuote == False):
            startQuote = True
            quoteType = letter
            sendMessage("ExInfo", f"QuoteType is set to \'{letter}\'")
        elif((letter == '\'' | letter == '\"') & letter != quoteType):
            sendMessage("Warning",f"Non-Matching Quotes Present in String \'{str}\'. Avoid Adding Extra Quotes in String")
        elif(letter == quoteType):
            startQuote = False
            strList.append(currentString)
        else:
            currentString += letter
    return strList

# Counts total number of quotes in string
def totalQuotes(str):
    return str.count("\'")+str.count("\"")