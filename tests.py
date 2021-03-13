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

if __name__ == "__main__":
    # test_open_image()
    # test_get_red_list()
    # test_get_red_percentile()
    # test_get_percentile_list()
    test_isolate_colors()