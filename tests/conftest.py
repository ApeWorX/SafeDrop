from pathlib import Path
from tempfile import mkdtemp

import pytest

from ..scripts._lib import DB


@pytest.fixture(scope="session")
def db_path():
    return Path(mkdtemp()) / "db.json"


@pytest.fixture(autouse=True, scope="session")
def db(db_path):
    return DB(path=db_path)


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def hacker(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def hack_details():
    return (
        "XBridgeHack Claim 2024-06-26",  # Name
        "XBridgeHack_20240626",  # Symbol
        "The X-Bridge hack resulting in the loss off ...",  # Description
    )
