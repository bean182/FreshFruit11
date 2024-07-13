import csv
import requests
from typing import Optional

class UserCache:
    def __init__(self, cachePath: str):
        # Load in cache
        self.cachePath: str  = cachePath
        self.cache:     dict = {}

        try:
            with open(cachePath, mode='r') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if len(row) == 2:
                        username, uuid = row
                        self.cache[username] = uuid
        except FileNotFoundError:
            print(f"No cache found - creating new at \"{cachePath}\"")
            self.cache = {}
        except:
            print(f"Corrupt cache at \"{cachePath}\"")
            self.cache = {}

    def GetUUID(self, username: str) -> Optional[str]:
        return self.cache.get(username)

    def AddUUID(self, username: str, uuid: str) -> None:
        self.cache[username] = uuid

        with open(self.cachePath, mode='w', newline='') as f:
            writer = csv.writer(f)
            for name, uuid in self.cache.items():
                writer.writerow([name, uuid])

cache: UserCache = UserCache("uuidCache.csv")

def getUUID(username: str) -> str:
    global cache

    uuid = cache.GetUUID(username)

    if uuid is not None:
        return uuid

    try:
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?").json()["id"]
        cache.AddUUID(username, uuid)

        return uuid
    except Exception as e:
        # Username not found, create fake uuid
        uuid = f"{hash(username) & ((1 << 64) - 1):016X}"
        cache.AddUUID(username, uuid)

        return uuid