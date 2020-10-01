import pytest
from AceBank import AceBank


@pytest.fixture
def ace_bank():
    return AceBank()
