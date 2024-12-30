import os
from pathlib import Path

EXP_NAME = "001"


# ---------- # DIRECTORIES # ---------- #
IS_KAGGLE_ENV = os.getenv("KAGGLE_DATA_PROXY_TOKEN") is not None
KAGGLE_COMPETITION_NAME = os.getenv(
    "KAGGLE_COMPETITION_NAME", "{{ cookiecutter.competition_name }}"
)

if not IS_KAGGLE_ENV:
    import rootutils

    ROOT_DIR = rootutils.setup_root(
        ".",
        indicator="pyproject.toml",
        cwd=True,
        pythonpath=True,
    )
    INPUT_DIR = ROOT_DIR / "data" / "input"
    # RTIFACT_DIR / EXP_NAME / 1 でのアクセスを想定
    ARTIFACT_DIR = ROOT_DIR / "data" / "output"
    # 当該 code の生成物の出力先. kaggle code とパスを合わせるために 1 を付与
    OUTPUT_DIR = ARTIFACT_DIR / EXP_NAME / "1"

    KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME", "{{ cookiecutter.kaggle_username }}")
    ARTIFACTS_HANDLE = (
        f"{KAGGLE_USERNAME}/{KAGGLE_COMPETITION_NAME}-artifacts/other/{EXP_NAME}"
    )
    CODES_HANDLE = f"{KAGGLE_USERNAME}/{KAGGLE_COMPETITION_NAME}-codes"
else:
    ROOT_DIR = Path("/kaggle/working")
    INPUT_DIR = Path("/kaggle/input")
    # 当該 code 以外の生成物が格納されている場所 (Model として使用できる)  ARTIFACT_DIR / EXP_NAME / 1 でアクセス可能
    ARTIFACT_DIR = INPUT_DIR  / f"{KAGGLE_COMPETITION_NAME}-artifacts"/ "other"
    OUTPUT_DIR = ROOT_DIR  # 当該 code の生成物の出力先

COMP_DATASET_DIR = INPUT_DIR / KAGGLE_COMPETITION_NAME

for d in [INPUT_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True, parents=True)

ARTIFACT_EXP_DIR = lambda exp_name=EXP_NAME: ARTIFACT_DIR / exp_name / "1"  # noqa  # 対象の exp の artifact が格納されている場所を返す
