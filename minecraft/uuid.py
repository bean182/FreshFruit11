import csv
import requests
from typing import Optional

class UserCache:
    def __init__(self, cachePath: str):
        """
        :param cachePath: Path to cache file. If cache does not exist, it will be created
        """ 
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
        """
        Get a UUID from the cache

        :param username: Minecraft username
        :return: UUID if cached, None if uncached
        """ 
        return self.cache.get(username)

    def AddUUID(self, username: str, uuid: str) -> None:
        """
        Add a UUID from the cache

        :param username: Minecraft username
        :param uuid: UUID
        """ 
        self.cache[username] = uuid

        with open(self.cachePath, mode='w', newline='') as f:
            writer = csv.writer(f)
            for name, uuid in self.cache.items():
                writer.writerow([name, uuid])

cache: UserCache = UserCache("uuidCache.csv")

def getUUID(username: str) -> str:
    """
    Gets a UUID. If the username is not found, None is returned.

    :param username: Minecraft username
    :return: UUID
    """ 
    global cache

    uuid = cache.GetUUID(username)

    if uuid is not None:
        return uuid

    try:
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?").json()["id"]
        cache.AddUUID(username, uuid)

        return uuid
    except Exception as e:
        # Username not found, return None
        uuid = None
        cache.AddUUID(username, uuid)

        return uuid