import filesService
import imagesFactory
import threading
import userInterface

for image in filesService.getImages():
    imagesFactory.NewImage(image)

threading.Thread(target=imagesFactory.DisplayResultImage).start()
userInterface.OpenUserInterface()
