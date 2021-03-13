import numpy as np
from PIL import Image

class ImageModifier:
    def __init__(self):
        self.image = None

    def openImage(imagePath):
        """
        Load image rgb array

        :param imagePath: string path to image to be loaded
        """

        img = Image.open(imagePath)
        img = np.array(img)
        self.image = img

    def getRedList(self):
        """
        Return a list of "red" values from image array if it exists. Otherwise
        return None

        :return: list of red values from image array
        """

        if self.image != None:
            return self.image[:,:,0].tolist()