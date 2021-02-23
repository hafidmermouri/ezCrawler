
import os, json
import time
from config import *



class Cache :
    @staticmethod
    def get(key, dir=CACHE_DIR, endless=False):
        filename = os.path.join(dir, key)
        if not os.path.exists(filename):
            return False

        mtime = os.stat(filename).st_mtime #to work on creation time => st.ctime
        age_hours = (time.time() - mtime) / 60 # get minutes
        if endless or age_hours < CACHE_DELAY_MINUTES :
            return open(filename).read()
        return False

    @staticmethod
    def set(key, data, dir=CACHE_DIR):
        filename = os.path.join(dir, key)
        if not isinstance(data, str) :
            data = json.dumps(data, sort_keys=True, indent=4)

        open(filename, "w").write(data)

