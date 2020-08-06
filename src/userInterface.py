import imagesFactory
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


class UIRow:
    frame: Frame = None
    fileNameLabel: Label = None
    alphaSlider: Scale = None
    zeroOutButton: Button = None
    tkinterImage: ImageTk = None
    imageLabel: Label = None
    image = None

    def ZeroOutImage(self):
        self.image.ZeroOut()
        ResetUI()


UIRows = []


def ResetUI():
    index = 0
    for image in imagesFactory.GetImages():
        UIRows[index].alphaSlider.set(image.alpha)
        index = index+1


def ResetValues():
    imagesFactory.ResetResult()
    ResetUI()


def SaveImage():
    imagesFactory.SaveResultImage()
    messagebox.showinfo(title="Message", message="File Saved Successfully")


def OpenUserInterface():
    mainWindow = Tk()
    mainWindow.minsize(700, 0)

    images = imagesFactory.GetImages()

    mainFrame = Frame(mainWindow)
    mainFrame.pack(fill="both", expand=True)

    for image in images:
        row = UIRow()
        row.image = image
        row.frame = Frame(mainFrame)

        row.fileNameLabel = Label(row.frame, text=image.GetFileName())
        row.fileNameLabel.grid(row=0, column=0, sticky="nsew")

        row.alphaSlider = Scale(row.frame, from_=0, to=1,
                                resolution=0.01, orient=HORIZONTAL, command=image.SetAlpha)
        row.alphaSlider.set(image.alpha)
        row.alphaSlider.grid(row=0, column=1, sticky="nsew")

        image = image.GetImage()
        width, height = image.size
        ratio = height/50
        row.tkinterImage = ImageTk.PhotoImage(
            image=image.resize((int(width/ratio), 50)))
        row.imageLabel = Label(row.frame, image=row.tkinterImage)
        row.imageLabel.grid(row=0, column=2, sticky="nsew", padx=10)

        row.zeroOutButton = Button(
            row.frame, text="Zero Out", command=row.ZeroOutImage)
        row.zeroOutButton.grid(row=0, column=3, sticky="ew", padx=10)

        row.frame.grid_columnconfigure(0, weight=1)
        row.frame.grid_columnconfigure(1, weight=4)
        row.frame.grid_columnconfigure(2, weight=1)
        row.frame.grid_columnconfigure(3, weight=1)

        row.frame.pack(fill="x")
        UIRows.append(row)

    # Buttons Frame
    buttonsFrame = Frame(mainFrame, pady=10)

    saveButton = Button(buttonsFrame, text="Save",
                        command=SaveImage)
    saveButton.grid(row=0, column=0)

    resetButton = Button(buttonsFrame, text="Reset Values",
                         command=ResetValues)
    resetButton.grid(row=0, column=1)
    buttonsFrame.pack(fill="x")
    buttonsFrame.grid_columnconfigure(0, weight=1)
    buttonsFrame.grid_columnconfigure(1, weight=1)
    buttonsFrame.pack(fill="x")

    mainWindow.mainloop()
