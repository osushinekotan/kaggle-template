# {{ cookiecutter.project_name }}


## setup

```bash
export KAGGLE_USERNAME={YOUR_KAGGLE_USERNAME}
export KAGGLE_KEY={YOUR_KAGGLE_KEY}
```

```bash
uv sync
```

## download competition dataset

```bash
sh scripts/download_competition.sh
```

## submission flow

1. `experiments` に実験フォルダを作成する

2. 実験を行う

3. 以下のいずれかの方法を使って、サブミッション時に使用するコードやモデルを upload する

   - コードの実行

     ```python
     if not config.IS_KAGGLE_ENV:
         from src.kaggle_utils.dataset import dataset_upload

         dataset_upload(
             handle=config.ARTIFACTS_HANDLE,
             local_dataset_dir=config.OUTPUT_DIR,
             update=True,
         )
         dataset_upload(
             handle=config.CODES_HANDLE,
             local_dataset_dir=config.ROOT_DIR,
             update=True,
         )
     ```

   - スクリプトの実行

     ```bash
     sh scripts/push_experiment.sh 001
     ```

4. 必要な dependencies を push する

   ```sh
   sh scripts/push_deps.sh
   ```

5. submission

   ```sh
   sh scripts/push_sub.sh
   ```

## lint & format

```bash
uv run pre-commit run -a
```

## Reference

- [効率的なコードコンペティションの作業フロー](https://ho.lc/blog/kaggle_code_submission/)
- [Kaggleコンペ用のVScode拡張を開発した](https://ho.lc/blog/vscode_kaggle_extension/)
