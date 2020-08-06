import os
import glob
import logger
import datetime


def getImages():
    path = os.path.join("images", "*.jpg")

    files = [f for f in glob.glob(path, recursive=True)]

    for f in files:
        logger.Log(f)
    return files


def GetNextResultName():
    return "results" + os.path.sep + "result-" + str(datetime.datetime.now().timestamp()) + ".jpg"
