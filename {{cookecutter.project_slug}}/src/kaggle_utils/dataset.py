import json
import logging
import os
import shutil
import subprocess
import tempfile
from fnmatch import fnmatch
from functools import lru_cache
from pathlib import Path

from kaggle import KaggleApi

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
assert KAGGLE_USERNAME, "KAGGLE_USERNAME is not set."

kaggle_client = KaggleApi()
kaggle_client.authenticate()

IGNORE_PATTERNS = [
    ".*",
    "__pycache__",
    "sub",
    "deps",
    "data",
    "scripts",
    "pyproject.toml",
    "uv.lock",
]


@lru_cache
def existing_dataset() -> list:
    """Check existing dataset in kaggle."""
    return kaggle_client.dataset_list(user=os.getenv("KAGGLE_USERNAME"))


@lru_cache
def check_if_exist_dataset(handle: str) -> bool:
    """Check if dataset already exist in kaggle."""
    for ds in existing_dataset():
        if str(ds) == handle:
            return True
    return False


def make_dataset_metadata(handle: str) -> dict:
    """Create dataset metadata.

    Args:
        handle (str): "{USER_NAME}/{DATASET_NAME}"

    Returns:
        dict: dataset metadata
    """
    dataset_metadata = {}
    dataset_metadata["id"] = handle
    dataset_metadata["licenses"] = [{"name": "CC0-1.0"}]  # type: ignore
    dataset_metadata["title"] = handle.split("/")[-1]
    return dataset_metadata


def copytree(src: str, dst: str, ignore_patterns: list | None = None) -> None:
    """Copytree with ignore patterns."""
    ignore_patterns = ignore_patterns or []

    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        if any(fnmatch(item, pattern) for pattern in ignore_patterns):
            continue

        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, ignore_patterns)
        else:
            shutil.copy2(s, d)


def display_tree(directory: Path, file_prefix: str = "") -> None:
    """Display directory tree."""
    entries = list(directory.iterdir())
    file_count = len(entries)

    for i, entry in enumerate(sorted(entries, key=lambda x: x.name)):
        if i == file_count - 1:
            prefix = "└── "
            next_prefix = file_prefix + "    "
        else:
            prefix = "├── "
            next_prefix = file_prefix + "│   "

        line = file_prefix + prefix + entry.name
        print(line)

        if entry.is_dir():
            display_tree(entry, next_prefix)


def dataset_upload(
    handle: str,
    local_dataset_dir: str,
    ignore_patterns: list[str] = IGNORE_PATTERNS,
    update: bool = False,
) -> None:
    """Push output directory to kaggle dataset."""

    # model and predictions
    metadata = make_dataset_metadata(handle=handle)

    # if exist dataset, stop pushing
    if check_if_exist_dataset(handle=handle) and not update:
        logger.warning(f"{handle} already exist!! Stop pushing. 🛑")
        return

    dataset_name = handle.split("/")[-1]

    with tempfile.TemporaryDirectory() as tempdir:
        dst_dir = Path(tempdir) / dataset_name

        copytree(
            src=str(local_dataset_dir),
            dst=str(dst_dir),
            ignore_patterns=ignore_patterns,
        )

        print(f"dst_dir={dst_dir}\ntree")
        display_tree(dst_dir)

        with open(Path(dst_dir) / "dataset-metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        if check_if_exist_dataset(handle=handle) and update:
            logger.info(f"update {handle}")
            kaggle_client.dataset_create_version(
                folder=dst_dir,
                version_notes="latest",
                quiet=False,
                convert_to_csv=False,
                delete_old_versions=False,
                dir_mode="zip",
            )
            return

        logger.info(f"create {handle}")
        kaggle_client.dataset_create_new(
            folder=dst_dir,
            public=False,
            quiet=False,
            dir_mode="zip",
        )


def competition_download(
    handle: str,
    destination: str | Path = "./",
    force_download: bool = False,
) -> None:
    """Download competition dataset.

    Args:
        destination (str | Path): base destination directory ({destination}/{handle} is created)
        handle (str): competition name
        force_download (bool, optional): if True, overwrite existing dataset. Defaults to False.
    """
    out_dir = Path(destination) / handle
    zipfile_path = out_dir / f"{handle}.zip"
    zipfile_path.parent.mkdir(exist_ok=True, parents=True)

    if not zipfile_path.is_file() or force_download:
        kaggle_client.competition_download_files(
            competition=handle,
            path=out_dir,
            quiet=False,
            force=force_download,
        )
        subprocess.run(["unzip", "-o", "-q", zipfile_path, "-d", out_dir])
    else:
        logger.info(f"Dataset ({handle}) already exists.")


def datasets_download(
    handles: list[str],
    destination: str | Path = "./",
    force_download: bool = False,
) -> None:
    """Download kaggle datasets.

    Args:
        handles (list[str]): list of dataset names (e.g. ["username/dataset-name"])
        destination (str | Path, optional): destination directory. Defaults to "./".
        force_download (bool, optional): if True, overwrite existing dataset. Defaults to False.
    """
    for dataset in handles:
        dataset_name = dataset.split("/")[1]
        out_dir = Path(destination) / dataset_name
        zipfile_path = out_dir / f"{dataset_name}.zip"

        out_dir.mkdir(exist_ok=True, parents=True)

        if not zipfile_path.is_file() or force_download:
            logger.info(f"Downloading dataset: {dataset}")
            kaggle_client.dataset_download_files(
                dataset=dataset,
                quiet=False,
                unzip=False,
                path=out_dir,
                force=force_download,
            )

            subprocess.run(["unzip", "-o", "-q", zipfile_path, "-d", out_dir])
        else:
            logger.info(f"Dataset ({dataset}) already exists.")
