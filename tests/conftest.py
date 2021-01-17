import pathlib

import pytest


CURR_PATH = pathlib.Path(__file__).parent.absolute()
DATA_DIR = CURR_PATH / "data"


@pytest.fixture
def sample_root_path():
    return DATA_DIR / "sample_root"


@pytest.fixture
def sample_db_path():
    return DATA_DIR / "sample.db"
