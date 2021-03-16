import pytest
from src.AceBank import AceBank


@pytest.fixture
def ace_bank():
    return AceBank()
