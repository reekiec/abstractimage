import pytest
from abstractimage.main import ImageModifier

@pytest.fixture
def example_empty_image_modifier():
    return ImageModifier()