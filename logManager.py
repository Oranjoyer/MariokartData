import time

logList = []
CONSOLE_LOG_LEVEL = "Info"
LOG_HIERARCHY = ("NONE","Error","Warning","Info","ExInfo","Debug","ALL")

# Determines if the set Log Level includes passed String 'type'
def logLevelIncludesType(type):
    # Getting Console Log Level
    logHierarchyLevel = LOG_HIERARCHY.index("ALL")
    if(CONSOLE_LOG_LEVEL in LOG_HIERARCHY):
        logHierarchyLevel = LOG_HIERARCHY.index(CONSOLE_LOG_LEVEL)
    # Getting Message Level
    typeIndex = LOG_HIERARCHY.index("ALL")
    if(type in LOG_HIERARCHY):
        typeIndex = LOG_HIERARCHY.index(type)
    # Prints Message if Console Log Level Includes the Message's Type
    if(typeIndex<=logHierarchyLevel):
        return True
    return False

# Sends message to log and outputs to console if 'logLevelIncludesType' function returns true for passed 'type' string
def sendMessage(type, source, message):
    logMessage = f"{time.ctime(time.time())} :: {type} ({source}): {message}"
    logList.append(logMessage)
    if(logLevelIncludesType(type)):
        print(logMessage)
sendMessage("NONE","LogManager",f"Console Log Level Set to \'{CONSOLE_LOG_LEVEL}\'")