import config
import polars as pl

df = pl.read_csv(config.COMP_DATASET_DIR / "sample_submission.csv")
df.write_csv(config.OUTPUT_DIR / "submission.csv")
