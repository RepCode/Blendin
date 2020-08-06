import os
import logger
import cv2 as cv
import copy
import filesService
from PIL import Image as PilImage

ImagesList = []
CurrentResult = None


class Image:
    filePath: str
    alpha: float = .0
    openCVImage = None

    def GetFileName(self):
        return self.filePath.split(os.path.sep)[-1]

    def SetAlpha(self, value: float):
        self.alpha = float(value)
        UpdateResultImage()

    def ZeroOut(self):
        self.alpha = 0
        UpdateResultImage()

    def GetImage(self):
        b,g,r = cv.split(self.openCVImage)
        img = cv.merge((r,g,b))
        return PilImage.fromarray(img)



def NewImage(filePath: str):
    image = Image()
    image.filePath = filePath
    ImagesList.append(image)
    alpha = 1.0/len(ImagesList)
    image.openCVImage = cv.imread(image.filePath)

    for image in ImagesList:
        image.alpha = alpha


def GetImages():
    return ImagesList


def DisplayResultImage():
    UpdateResultImage()

    cv.startWindowThread()

    cv.waitKey(0)
    cv.destroyAllWindows()


def UpdateResultImage():
    global CurrentResult
    if len(ImagesList) == 0:
        return

    prevImage = None
    count = 0
    beta = 0
    for image in ImagesList:
        if prevImage is None:
            # I have to make a deep copy or else it modifies de first image
            prevImage = copy.deepcopy(image)
            beta = prevImage.alpha
            continue
        prevImage.openCVImage = cv.addWeighted(
            prevImage.openCVImage, beta, image.openCVImage, image.alpha, 0.0)
        beta = 1
    CurrentResult = prevImage.openCVImage
    cv.namedWindow("Result", cv.WINDOW_NORMAL)
    cv.imshow("Result", prevImage.openCVImage)


def SaveResultImage():
    global CurrentResult
    cv.imwrite(filesService.GetNextResultName(), CurrentResult)


def ResetResult():
    global ImagesList
    alpha = 1.0/len(ImagesList)
    for image in ImagesList:
        image.alpha = alpha
    UpdateResultImage()
