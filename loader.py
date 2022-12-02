def initalizeList():
  essayFile = open("essayFile.json")
  return json.initialize(essayFile)

def initalizeLog():
  logFile = open("logFile.json")
  return json.initalize(logFile)