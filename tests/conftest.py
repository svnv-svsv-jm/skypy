import json
import os
import sys
import typing as ty
from pathlib import Path

import pendulum
import pyrootutils
import pytest
from loguru import logger

from skypy.types import LogLevel


def get_root() -> str:
    """Get root directory of this project.
    Using `pyrootutils`, we find the root directory of this project and make sure it is our working directory.
    """
    return str(
        pyrootutils.setup_root(
            search_from=".",
            indicator=[".git", "pyproject.toml"],
            pythonpath=False,
            dotenv=True,
            cwd=True,
        )
    )


root = get_root()


@pytest.fixture(autouse=True)
def root_dir() -> str:
    """Root folder.
    Using pyrootutils, we find the root directory of this project and make sure it is our working directory.
    """
    return get_root()


@pytest.fixture
def invoked_path() -> str:
    """First argument for `python` command.
    This may be equal to the script being called.
    """
    p = os.path.abspath(sys.argv[0])
    logger.debug(f"invoked_path: {p}")
    return p


@pytest.fixture
def running_locally(invoked_path: str) -> bool:
    """Whether the test is running locally or not.
    This is inferred by checking if the first arg to the `python` executable ends with `.py`.
    """
    return invoked_path.endswith(".py")


@pytest.fixture(autouse=True)
def logging_level() -> LogLevel:
    """Logging level."""
    return "TRACE"


@pytest.fixture(autouse=True)
def logger_for_tests(logging_level: LogLevel) -> ty.Iterator[int]:
    """Set up logger for all tests."""
    logger.remove()
    lll = logger.add(sys.stderr, level=logging_level)
    yield lll


@pytest.fixture
def log_filename(request: pytest.FixtureRequest) -> str:
    """Basename for the file where to store logs.
    By default, it gets the name of the current test.
    """
    name: str = str(request.node.name)  # type: ignore
    logger.debug(f"Running test: {name}")
    return f"{name}"


@pytest.fixture
def log_file(artifacts_path: str, log_filename: str) -> str:
    """File where to store logs."""
    return os.path.join(
        artifacts_path, f"{log_filename}--{pendulum.now().to_date_string()}.log"
    )


@pytest.fixture
def log_to_file(logging_level: str, log_file: str) -> ty.Iterator[int]:
    """Add sink for logging to a file."""
    logger_id = logger.add(log_file, level=logging_level)
    yield logger_id
    with logger.catch(Exception):
        logger.remove(logger_id)


@pytest.fixture
def catch_logs(
    logging_level: LogLevel,
    logger_for_tests: int,
) -> ty.Iterator[list[dict[str, ty.Any]]]:
    """Capture logs.

    Import this fixture and you will get a list of logged items.

    For example:

    ```python
    def test_something(catch_logs: list[dict]) -> None:
    logger.info('hello')
    # Check there is one 'hello' message in `catch_logs`
    ```
    """
    logger.debug(f"logger_for_tests (id): {logger_for_tests}")
    logs: list[dict[str, ty.Any]] = []

    def sink_function(record: str) -> None:
        """Receives serialized records."""
        r: dict[str, ty.Any] = json.loads(record)
        logs.append(r)

    logger.debug(f"Adding sink function: {sink_function}")
    logger_id = logger.add(sink_function, level=logging_level, serialize=True)

    yield logs

    with logger.catch(Exception):
        logger.remove(logger_id)


@pytest.fixture
def assets_dir() -> str:
    """Assets directory."""
    return os.path.join(root, "assets")


@pytest.fixture
def za_assets_dir(assets_dir: str) -> str:
    """Zelda Assets directory."""
    return os.path.join(assets_dir, "za")


@pytest.fixture
def za_trainer_data_path(za_assets_dir: str) -> str:
    """Zelda Trainer data path."""
    return os.path.join(za_assets_dir, "Input/trdata_array.json")


@pytest.fixture
def za_trainer_data_raw(za_trainer_data_path: str) -> dict:
    """Load raw data from the trainer data file."""
    # Load the trpfs file which contains the actual trainer data
    trpfs_file = Path(za_trainer_data_path)

    with trpfs_file.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return raw_data


@pytest.fixture
def za_trainer_data_dummy(za_trainer_data_raw: dict) -> list[dict]:
    """Trainer data for the first (dummy) trainer.

    Example:
    ```json
    {
        "trid": "00_test_data",
        "trtype": 1048451227980125490,
        "trtype2": 1048451227980125490,
        "zaRank": "NONE",
        "moneyRate": 12,
        "megEvolution": False,
        "lastHand": False,
        "poke1": {
            "devId": "DEV_MEGANIUMU",
            "formId": 0,
            "sex": "DEFAULT",
            "item": "ITEMID_NONE",
            "level": 10,
            "ballId": "MONSUTAABOORU",
            "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "seikaku": "GANBARIYA",
            "tokusei": "RANDOM_12",
            "talentValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "effortValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "rareType": "NO_RARE",
            "scaleValue": 128,
        },
        "poke2": {
            "devId": "DEV_NULL",
            "formId": 0,
            "sex": "DEFAULT",
            "item": "ITEMID_NONE",
            "level": 0,
            "ballId": "MONSUTAABOORU",
            "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "seikaku": "GANBARIYA",
            "tokusei": "RANDOM_12",
            "talentValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "effortValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "rareType": "NO_RARE",
            "scaleValue": 128,
        },
        "poke3": {
            "devId": "DEV_NULL",
            "formId": 0,
            "sex": "DEFAULT",
            "item": "ITEMID_NONE",
            "level": 0,
            "ballId": "MONSUTAABOORU",
            "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "seikaku": "GANBARIYA",
            "tokusei": "RANDOM_12",
            "talentValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "effortValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "rareType": "NO_RARE",
            "scaleValue": 128,
        },
        "poke4": {
            "devId": "DEV_NULL",
            "formId": 0,
            "sex": "DEFAULT",
            "item": "ITEMID_NONE",
            "level": 0,
            "ballId": "MONSUTAABOORU",
            "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "seikaku": "GANBARIYA",
            "tokusei": "RANDOM_12",
            "talentValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "effortValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "rareType": "NO_RARE",
            "scaleValue": 128,
        },
        "poke5": {
            "devId": "DEV_NULL",
            "formId": 0,
            "sex": "DEFAULT",
            "item": "ITEMID_NONE",
            "level": 0,
            "ballId": "MONSUTAABOORU",
            "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "seikaku": "GANBARIYA",
            "tokusei": "RANDOM_12",
            "talentValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "effortValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "rareType": "NO_RARE",
            "scaleValue": 128,
        },
        "poke6": {
            "devId": "DEV_NULL",
            "formId": 0,
            "sex": "DEFAULT",
            "item": "ITEMID_NONE",
            "level": 0,
            "ballId": "MONSUTAABOORU",
            "waza1": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza2": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza3": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "waza4": {"wazaId": "WAZA_NULL", "isPlusWaza": False},
            "seikaku": "GANBARIYA",
            "tokusei": "RANDOM_12",
            "talentValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "effortValue": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spAtk": 0,
                "spDef": 0,
                "agi": 0,
            },
            "rareType": "NO_RARE",
            "scaleValue": 128,
        },
        "aiBasic": True,
        "aiHigh": False,
        "aiExpert": False,
        "aiDouble": False,
        "aiRaid": False,
        "aiWeak": False,
        "aiItem": False,
        "aiChange": False,
        "viewHorizontalAngle": 30.0,
        "viewVerticalAngle": 50.0,
        "viewRange": 17.0,
        "hearingRange": 17.0,
    }
    ```
    """
    values = za_trainer_data_raw["values"]
    # Return first Trainer, which is the dummy one
    return values[0]
