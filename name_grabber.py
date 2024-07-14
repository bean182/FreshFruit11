import os
import re
import gzip
import minecraft


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

            elif file.endswith(".txt") or file.endswith(".log"):
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
        UUID = minecraft.getUUID(username)

        # check if the dictionary already contains uuid
        if UUID in users.keys():
            # check if username is already used (duplicate)
            if not username in users[UUID]:
                # append username to value array in existing dictionary entry
                users[UUID].append(username)
        else:
            # create new dictionary entry
            users[UUID] = [username]
    
    # return dict so it can be used elsewhere
    return users

# directoryPath = "C:\\Users\\49151\\Desktop\\Old logs"
directoryPath = "./Data"

# catch the output of getNames() in a dictionary
userDictionary = extractFiles(directoryPath)

# print dictionary
# the items() method lists all key-value pairs
# the uuid was used as the key and the value is an array of usernames that user has had
validCount = 0
invalidCount = 0
for uuid, nameArray in userDictionary.items():
    if not uuid is None:
        output = str(uuid)
        for username in nameArray:
            output += " " + str(username)
        print(output)
        validCount += 1
    else:
        invalidCount = len(nameArray)

outputFile = "output.txt"
with open(outputFile, 'wt') as textFile:
    textFile.write(str(userDictionary.items())) 
    
print(f"Matched {validCount} usernames to UUID. Unable to match {invalidCount} usernames.")
print(f"Results written to {outputFile}")