import pytest
from ..main import ImageModifier

@pytest.mark.image_modifier
def test_image_modifier_open_image(example_empty_image_modifier):
    im = example_empty_image_modifier
    im.openImage()
    assert im.image != None