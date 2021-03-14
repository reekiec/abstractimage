import numpy as np
from PIL import Image
from copy import deepcopy

class ImageModifier:
    def __init__(self):
        self.image = None
        self.mod_image = None
        self.difference_array = None

    def _largestIndex(self, l):
        return l.index(max(l))
    
    def _resizeImage(self, im):
        return im.resize((640, 480))

    def _initDifferenceArray(self):
        self.difference_array = np.ndarray((self.image.shape[0], self.image.shape[1], 4))

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
        self._initDifferenceArray()

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
    
    def _applyDifferences(self, row, col, count_greater):
        if count_greater < 2:
            self.mod_image[row,col] = [255, 255, 255]
        else:
            self.mod_image[row,col] = [0, 0, 0]

    def _findApplyRowDifference(self):
        if type(self.image) == type(None):
            return None
        
        for row in range(self.mod_image.shape[0] - 1):
            for col in range(self.mod_image.shape[1]):
                total1 = sum(self.mod_image[row, col])
                total2 = sum(self.mod_image[row + 1, col])
                diff = total2 - total1
                self.difference_array[row, col, 0] = abs(diff)
    
    def _findApplyColumnDifference(self):
        if type(self.image) == type(None):
            return None
        
        for row in range(self.mod_image.shape[0]):
            for col in range(self.mod_image.shape[1] - 1):
                total1 = sum(self.mod_image[row, col])
                total2 = sum(self.mod_image[row, col + 1])
                diff = total2 - total1
                self.difference_array[row, col, 1] = abs(diff)
        
    def _findApplyDRDifference(self):
        if type(self.image) == type(None):
            return None
        
        for row in range(self.mod_image.shape[0] - 1):
            for col in range(self.mod_image.shape[1] - 1):
                total1 = sum(self.mod_image[row, col])
                total2 = sum(self.mod_image[row + 1, col + 1])
                diff = total2 - total1
                self.difference_array[row, col, 2] = abs(diff)

    def _findApplyDLDifference(self):
        if type(self.image) == type(None):
            return None
        
        for row in range(self.mod_image.shape[0] - 1):
            for col in range(1, self.mod_image.shape[1]):
                total1 = sum(self.mod_image[row, col])
                total2 = sum(self.mod_image[row + 1, col - 1])
                diff = total2 - total1
                self.difference_array[row, col, 3] = abs(diff)

    def findDifferences(self, cutoff):
        diffs = [0]
        self.mod_image = deepcopy(self.image)
        self._findApplyRowDifference()
        self._findApplyColumnDifference()
        self._findApplyDRDifference()
        self._findApplyDLDifference()

        for row in range(self.difference_array.shape[0]):
            for col in range(self.difference_array.shape[1]):
                diffs = self.difference_array[row, col]
                count_greater = 0
                for diff in diffs:
                    if diff > cutoff:
                        count_greater += 1
                self._applyDifferences(row, col, count_greater)

        print(f"Rows: {self.image.shape[0]}, Columns: {self.image.shape[1]}, Total Pixels: {self.image.shape[1]*self.image.shape[0]}")
    
    def cleanModImage(self):
        if type(self.mod_image) == type(None):
            return None
        white = np.array([255, 255, 255])
        black = np.array([0, 0, 0])
        
        for row in range(1, self.mod_image.shape[0] - 1):
            for col in range(1, self.mod_image.shape[1] - 1):
                if np.array_equal(self.mod_image[row, col], white):
                    continue
                if np.array_equal(self.mod_image[row + 1, col], black):
                    continue
                if np.array_equal(self.mod_image[row - 1, col], black):
                    continue
                if np.array_equal(self.mod_image[row, col + 1], black):
                    continue
                if np.array_equal(self.mod_image[row, col - 1], black):
                    continue
                self.mod_image[row, col] = white


"""
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
"""