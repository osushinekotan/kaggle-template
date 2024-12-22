import logging
import os

import fire
import rootutils

from kaggle_utils.dataset import competition_download, datasets_download

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# change the root directory to the project root
ROOT_DIR = rootutils.setup_root(".", indicator="pyproject.toml", cwd=True, dotenv=True)
logger.info(f"ROOT_DIR: {ROOT_DIR}")

KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_COMPETITION_NAME = os.getenv("KAGGLE_COMPETITION_NAME", "{{ cookiecutter.competition_name }}")

assert KAGGLE_USERNAME, "KAGGLE_USERNAME is not set."

INPUT_DIR = ROOT_DIR / "data" / "input"
INPUT_DIR.mkdir(exist_ok=True, parents=True)


if __name__ == "__main__":
    fire.Fire(
        {
            "competition_download": lambda handle=KAGGLE_COMPETITION_NAME,
            destination=INPUT_DIR,
            force_download=False: competition_download(
                handle=handle, destination=destination, force_download=force_download
            ),
            "datasets_download": lambda handles, destination=INPUT_DIR, force_download=False: datasets_download(
                handles=handles, destination=destination, force_download=force_download
            ),
        }
    )
