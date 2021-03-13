import numpy as np
from main import ImageModifier

def test_open_image():
    im = ImageModifier()
    print(isinstance(im.image, type(None)))
    im.openImage("mountain.jpeg")
    print(type(im.image))

def test_get_red_list():
    im = ImageModifier()
    im.openImage("mountain.jpeg")
    print(im.getRedList())

def test_get_red_percentile():
    im = ImageModifier()
    im.openImage("mountain.jpeg")
    print(im.getRedPercentile(75))

def test_get_percentile_list():
    im = ImageModifier()
    im.openImage("mountain.jpeg")
    print(im.getPercentileList(75))

def test_isolate_colors():
    im = ImageModifier()
    im.openImage("mountain.jpeg")
    percentileList = im.getPercentileList(75)
    im.isolateColors(percentileList)
    im.saveImage("mtn.png")

def differences():
    """
    Creates four different pictures based on the difference between
    sums of pixel values in certain directions.
    1st value is the cutoff for difference to trigger output pixel
    2nd value is direction:
    0 = down
    1 = right
    2 = down+right
    3 = down+left
    Down seems to produce clearest output, but it depends on the picture
    """
    im = ImageModifier()
    im.openImage("ferrari.jpeg")
    im.findDifferences(50,0)
    im.saveImage("car.png")
    im.findDifferences(50,1)
    im.saveImage("car1.png")
    im.findDifferences(50,2)
    im.saveImage("car2.png")
    im.findDifferences(50,3)
    im.saveImage("car3.png")

if __name__ == "__main__":
    # test_open_image()
    # test_get_red_list()
    # test_get_red_percentile()
    # test_get_percentile_list()
    # test_isolate_colors()
    differences()