# kaggle-template

```bash
uv run pre-commit run -a
```

## Code

initial creation

```bash
cd ./codes
kaggle d create -p .
```

update dataset

```bash
cd ./codes
kaggle d version -m 'update' -r zip
```

## Sub

```bash
cd ./sub
kaggle k push
```

## Model

```python
import kagglehub

handle = "<KAGGLE_USERNAME>/<DATASET>"
local_dataset_dir = "path/to/local/dataset/dir"
kagglehub.model_upload(handle, local_dataset_dir, ignore_patterns=["ckpt*.pth"])
```

## Reference

- [効率的なコードコンペティションの作業フロー](https://ho.lc/blog/kaggle_code_submission/)
- [Kaggleコンペ用のVScode拡張を開発した](https://ho.lc/blog/vscode_kaggle_extension/)
