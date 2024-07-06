import gzip
import os
import re
import requests 

# extract all previous logs from zip to regular file AND latest file and read file 
def extractFiles(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        # print(dirpath, dirnames, filenames)
        for file in filenames:
            filePath = os.path.join(dirpath,file)
            # print(filePath)
            if file.endswith(".gz"):
                with gzip.open(filePath, "rt", encoding="latin-1") as textFile:
                    text = textFile.read()
                    #print(text)
                    getNames(text)
            elif file.endswith(".txt"):
                text = textFile.read().decode("utf-8")
                #print(text)
                getNames(text)
                 
# search for unique pattern (FINAL KILL!)
def getNames(text):
    pattern = r"\[CHAT\] (.+?) was (.+?) FINAL KILL!"
    matches = re.findall(pattern,text)
    for match in matches:
        username = match[0]
        UUID = getUUID(username)
        print(UUID,username)

# query minecraft api for uuid
def getUUID(username):
    try:
        return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?").json()["id"]
    except Exception as e:
        return None
    


# remove duplicates
# fix uuid not found
 
directoryPath = "C:\\Users\\49151\\Desktop\\Old logs"
extractFiles(directoryPath)