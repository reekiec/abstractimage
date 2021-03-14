import numpy as np
from PIL import Image
from copy import deepcopy

class ImageModifier:
    def __init__(self):
        self.image = None
        self.mod_image = None

    def _largestIndex(self, l):
        return l.index(max(l))
    
    def _resizeImage(self, im):
        return im.resize((640, 480))

    def openImage(self, imagePath):
        """
        Load image rgb array

        :param imagePath: string path to image to be loaded
        """

        img = Image.open(imagePath)
        img = self._resizeImage(img)
        img = np.array(img)
        self.image = img
        self.mod_image = deepcopy(self.image)

    def getRedList(self):
        """
        Return a list of "red" values from image array if it exists. Otherwise
        return None

        :return: list of red values from image array
        """

        if type(self.image) != type(None):
            return self.image[:,:,0].tolist()
        return None

    def getGreenList(self):
        """
        Return a list of "green" values from image array if it exists. Otherwise
        return None

        :return: list of green values from image array
        """

        if type(self.image) != type(None):
            return self.image[:,:,1].tolist()
        return None

    def getBlueList(self):
        """
        Return a list of "blue" values from image array if it exists. Otherwise
        return None

        :return: list of blue values from image array
        """

        if type(self.image) != type(None):
            return self.image[:,:,2].tolist()
        return None

    def getRedPercentile(self, p):
        """
        Return a decimal percentile (p) of red values

        :return: float percentile (p)
        """

        redList = self.getRedList()
        if type(redList) != type(None):
            return np.percentile(np.array(redList), p)
        return None

    def getGreenPercentile(self, p):
        """
        Return a decimal percentile (p) of green values

        :return: float percentile (p)
        """

        greenList = self.getGreenList()
        if type(greenList) != type(None):
            return np.percentile(np.array(greenList), p)
        return None

    def getBluePercentile(self, p):
        """
        Return a decimal percentile (p) of blue values

        :return: float percentile (p)
        """

        blueList = self.getBlueList()
        if type(blueList) != type(None):
            return np.percentile(np.array(blueList), p)
        return None

    def getPercentileList(self, p):
        redPercentile = self.getRedPercentile(p)
        if type(redPercentile) == type(None):
            return None
        greenPercentile = self.getGreenPercentile(p)
        bluePercentile = self.getBluePercentile(p)

        return [
            redPercentile,
            bluePercentile,
            greenPercentile
        ]

    def isolateColors(self, percentileList):
        self.mod_image = deepcopy(self.image)
        for row in range(self.mod_image.shape[0]):
            for column in range(self.mod_image.shape[1]): 
                replacement = [255,255,255]
                max_index = self._largestIndex(list(self.mod_image[row,column]))
                
                if self.mod_image[row,column,0] > 200 and self.mod_image[row,column,1] > 200 and self.mod_image[row,column,2] > 200: # if white
                    self.mod_image[row,column] = replacement
                    continue
                elif self.mod_image[row,column,max_index] >= percentileList[max_index]:
                    replacement = [0,0,0]
                    replacement[max_index] = self.mod_image[row, column, max_index]
                
                self.mod_image[row, column] = replacement

    def saveModImage(self, imgPath):
        if type(self.mod_image) != type(None):
            img = Image.fromarray(self.mod_image, 'RGB')
            img.save(imgPath)
    
    def _applyDifferences(self, row, col, diff, cutoff):
        if abs(diff) < cutoff:
            self.mod_image[row,col] = [255, 255, 255]
        else:
            self.mod_image[row,col] = [0, 0, 0]

    def findDifferences(self, cutoff):
        diffs = [0]
        self.mod_image = deepcopy(self.image)

        # Search differences between rows
        for row in range(self.mod_image.shape[0]-1):
            for col in range(self.mod_image.shape[1]):
                total1 = sum(self.mod_image[row,col])
                total2 = sum(self.mod_image[row+1,col])
                diff = total2 - total1
                diffs.append(diff)
                self._applyDifferences(row, col, diff, cutoff)

        print("Max: ", max(diffs))
        print("Min: ", min(diffs))
        print(f"Count above {cutoff}: ", sum(i>=cutoff for i in diffs))
        print(f"Count below -{cutoff}: ", sum(i<=-1*cutoff for i in diffs))

        print(f"Rows: {self.image.shape[0]}, Columns: {self.image.shape[1]}, Total Pixels: {self.image.shape[1]*self.image.shape[0]}")