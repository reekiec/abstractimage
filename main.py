import numpy as np
from PIL import Image

class ImageModifier:
    def __init__(self):
        self.image = None

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
        for row in range(self.image.shape[0]):
            for column in range(self.image.shape[1]): 
                replacement = [255,255,255]
                max_index = self._largestIndex(list(self.image[row,column]))
                
                if self.image[row,column,0] > 200 and self.image[row,column,1] > 200 and self.image[row,column,2] > 200: # if white
                    self.image[row,column] = replacement
                    continue
                elif self.image[row,column,max_index] >= percentileList[max_index]:
                    replacement = [0,0,0]
                    replacement[max_index] = self.image[row, column, max_index]
                
                self.image[row, column] = replacement

    def saveImage(self, imgPath):
        if type(self.image) != type(None):
            img = Image.fromarray(self.image, 'RGB')
            img.save(imgPath)
    
    def findDifferences(self, cutoff,direction):
        diffs = [0]

        # Search differences between rows
        if (direction == 0):
            for row in range(self.image.shape[0]-1):
                for col in range(self.image.shape[1]):
                    total1 = sum(self.image[row,col])
                    total2 = sum(self.image[row+1,col])
                    diff = total2 - total1
                    diffs.append(diff)
                    if abs(diff) < cutoff:
                        self.image[row,col] = [255, 255, 255]
                    else:
                        self.image[row,col] = [0, 0, 0]
        
        # Search differences between columns
        elif (direction == 1):
            for row in range(self.image.shape[0]):
                for col in range(self.image.shape[1]-1):
                    total1 = sum(self.image[row,col])
                    total2 = sum(self.image[row,col+1])
                    diff = total2 - total1
                    diffs.append(diff)
                    if abs(diff) >= cutoff:
                        self.image[row,col] = [0, 0, 0]
                    else:
                        self.image[row,col] = [255,255,255]

        # Search diagonally down & right
        elif (direction == 2):
            for row in range(self.image.shape[0]-1):
                for col in range(self.image.shape[1]-1):
                    total1 = sum(self.image[row,col])
                    total2 = sum(self.image[row+1,col+1])
                    diff = total2 - total1
                    diffs.append(diff)
                    if abs(diff) < cutoff:
                        self.image[row,col] = [255, 255, 255]
                    else:
                        self.image[row,col] = [0, 0, 0]

        # Search diagonally down & left
        elif (direction == 3):
            for row in range(self.image.shape[0]-1):
                for col in range(1,self.image.shape[1]):
                    total1 = sum(self.image[row,col])
                    total2 = sum(self.image[row+1,col-1])
                    diff = total2 - total1
                    diffs.append(diff)
                    if abs(diff) < cutoff:
                        self.image[row,col] = [255, 255, 255]
                    else:
                        self.image[row,col] = [0, 0, 0]

        print("Max: ", max(diffs))
        print("Min: ", min(diffs))
        print(f"Count above {cutoff}: ", sum(i>=cutoff for i in diffs))
        print(f"Count below -{cutoff}: ", sum(i<=-1*cutoff for i in diffs))

        print(f"Rows: {self.image.shape[0]}, Columns: {self.image.shape[1]}, Total Pixels: {self.image.shape[1]*self.image.shape[0]}")