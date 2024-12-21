import os

import polars as pl

KAGGLE_ENV = os.getenv("KAGGLE_DATA_PROXY_TOKEN") is not None
if not KAGGLE_ENV:
    import rootutils

    ROOT_DIR = rootutils.setup_root("./codes", indicator=".project-root", cwd=True, pythonpath=True)

from src.hello import hello

hello()
df = pl.read_csv("/kaggle/input/spaceship-titanic/sample_submission.csv")
df.write_csv("submission.csv")
