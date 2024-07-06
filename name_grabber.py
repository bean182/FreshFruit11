import gzip
import os
import re
import requests 
from typing import Optional


def extractFiles(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        # print(dirpath, dirnames, filenames)
        for file in filenames:
            filePath = os.path.join(dirpath,file)
            # print(filePath)
            if file.endswith(".gz"):
                with gzip.open(filePath, "rt",encoding="latin-1") as textFile:
                    text = textFile.read()
                    #print(text)
                    getNames(text)
            elif file.endswith(".txt"):
                text = textFile.read().decode("utf-8")
                #print(text)
                getNames(text)
                 

def getNames(text):
    pattern = r"\[CHAT\] (.+?) was (.+?) FINAL KILL!"
    matches = re.findall(pattern,text)
    for match in matches:
        username = match[0]
        UUID = getUUID(username)
        print(UUID,username)


def getUUID(username: str) -> Optional[str]:
    try:
        return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?").json()["id"]
    except Exception as e:
        return None
    
# remove duplicates
# fix uuid not found
# extract all previous logs from zip to regular file AND latest file and read file  
directoryPath = "C:\\Users\\49151\\Desktop\\Old logs"
extractFiles(directoryPath)
  # search for unique pattern (FINAL KILL!)