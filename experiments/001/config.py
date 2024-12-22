import os
from pathlib import Path

EXP_NAME = "001"

IS_KAGGLE_ENV = os.getenv("KAGGLE_DATA_PROXY_TOKEN") is not None
KAGGLE_COMPETITION_NAME = os.getenv("KAGGLE_COMPETITION_NAME", "spaceship-titanic")

if not IS_KAGGLE_ENV:
    import rootutils

    ROOT_DIR = rootutils.setup_root(
        ".",
        indicator="pyproject.toml",
        cwd=True,
        pythonpath=True,
    )
    INPUT_DIR = ROOT_DIR / "data" / "input"
    OUTPUT_DIR = ROOT_DIR / "data" / "output" / EXP_NAME

    KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME", "{{ cookiecutter.kaggle_username }}")

    ARTIFACTS_HANDLE = f"{KAGGLE_USERNAME}/{KAGGLE_COMPETITION_NAME}-artifacts"
    CODES_HANDLE = f"{KAGGLE_USERNAME}/{KAGGLE_COMPETITION_NAME}-codes"
else:
    ROOT_DIR = Path("/kaggle/working")
    INPUT_DIR = Path("/kaggle/input")
    OUTPUT_DIR = ROOT_DIR

COMP_DATASET_DIR = INPUT_DIR / KAGGLE_COMPETITION_NAME

for d in [INPUT_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True, parents=True)
