import gzip
import os
import re
import requests 

# extract all previous logs from zip to regular file AND latest file and read file 
def extractFiles(directory):
    # a dictionary is a mapping of keys to values. Instead of numbers like an array: array[int] = value, a dictionary uses strings: dict[str] = value
    # https://www.w3schools.com/python/python_dictionaries.asp
    users = {}

    for dirpath, dirnames, filenames in os.walk(directory):
        # print(dirpath, dirnames, filenames)
        for file in filenames:
            filePath = os.path.join(dirpath,file)
            # print(filePath)
            if file.endswith(".gz"):
                with gzip.open(filePath, "rt", encoding="latin-1") as textFile:
                    text = textFile.read()
                    # print(text)

                    # combine current user dict with updated data
                    users.update(getNames(text))

            else:
                with open(filePath, "rt") as textFile:
                    text = textFile.read()
                    # print(text)

                    # combine current user dict with updated data
                    users.update(getNames(text))

    # return dict so it can be used elsewhere
    return users
                 
# search for unique pattern (FINAL KILL!)
def getNames(text):
    pattern = r"\[CHAT\] (.+?) was (.+?) FINAL KILL!"
    matches = re.findall(pattern,text)

    # create an empty dictionary to hold username-uuid pairs
    users = {}

    for match in matches:
        username = match[0]
        UUID = getUUID(username)

        # check if uuid was found
        if UUID is None:
            id = f"{hash(username) & ((1 << 64) - 1):016X}"
            key = "[" + id + "] No UID Found:"
            users[key] = [username]
        # check if the dictionary already contains uuid
        elif UUID in users.keys():
            # check if username is already used (duplicate)
            if not username in users[UUID]:
                # append username to value array in existing dictionary entry
                users[UUID].append(username)
        else:
            # create new dictionary entry
            users[UUID] = [username]
    
    # return dict so it can be used elsewhere
    return users

# query minecraft api for uuid
def getUUID(username):
    try:
        return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?").json()["id"]
    except Exception as e:
        return None
    
# directoryPath = "C:\\Users\\49151\\Desktop\\Old logs"
directoryPath = "./Data"

# catch the output of getNames() in a dictionary
userDictionary = extractFiles(directoryPath)

# print dictionary
# the items() method lists all key-value pairs
# the uuid was used as the key and the value is an array of usernames that user has had
for uuid, nameArray in userDictionary.items():
    output = str(uuid)
    for username in nameArray:
        output += " " + str(username)
    print(output)


# Hello


with open("output.txt", 'wt') as textFile:
    textFile.write(str(userDictionary.items())) 
    




#TODO:
#-username not found on mc api
# Cache for faster interaction 
