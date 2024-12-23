import logging
import os

import fire
import rootutils

from kaggle_utils.customhub import dataset_upload, model_upload

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ROOT_DIR = rootutils.setup_root(".", indicator="pyproject.toml", cwd=True, dotenv=True)
DATA_DIR = ROOT_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
INPUT_DIR.mkdir(exist_ok=True, parents=True)

KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_COMPETITION_NAME = os.getenv(
    "KAGGLE_COMPETITION_NAME", "{{ cookiecutter.competition_name }}"
)

assert KAGGLE_USERNAME, "KAGGLE_USERNAME is not set."


BASE_ARTIFACTS_HANDLE = f"{KAGGLE_USERNAME}/{KAGGLE_COMPETITION_NAME}-artifacts/other"
CODES_HANDLE = f"{KAGGLE_USERNAME}/{KAGGLE_COMPETITION_NAME}-codes"

if __name__ == "__main__":
    fire.Fire(
        {
            "codes": lambda: dataset_upload(
                handle=CODES_HANDLE,
                local_dataset_dir=ROOT_DIR,
                update=True,
            ),
            "artifacts": lambda exp_name: model_upload(
                handle=f"{BASE_ARTIFACTS_HANDLE}/{exp_name}",
                local_model_dir=OUTPUT_DIR
                / exp_name
                / "1",  # output dir に存在する artifact をアップロード
                update=False,
            ),
        }
    )
