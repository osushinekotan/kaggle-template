# Kaggle Template

cookiecutter を使った kaggle code competition 用のテンプレート

## Quickstart

**install cookiecutter**

```bash
pip install cookiecutter
```

**project の作成**

1. project root directory ごと作成する場合

    ```bash
    cookiecutter https://github.com/osushinekotan/kaggle-template.git
    ```

2. 作成済みの project root directory を使いたい場合 (clone した repository など)

    ```bash
    cd {project_dir}
    cookiecutter https://github.com/osushinekotan/kaggle-template.git -f -o ../
    ```

    - `project_slug` と `{projet_dir}` が同じ名前であり、それを上書きする形で template を作成する
    - cookicutter の [CL options](https://cookiecutter.readthedocs.io/en/1.7.0/advanced/cli_options.html) を使う

**cookiecutter parameters**

- `competition_name`: Kaggle competition の名前。コンペ URL に含まれる名前、もしくは `kaggle competitions download -c {competition_name}` で指定する名前をここで使用する
- `project_name`: プロジェクトの名前
- `project_slug`: 作成されるディレクトリ名
- `project_description`: プロジェクトの説明
- `kaggle_username`: kaggle に登録してあるユーザー名
- `python_version`: 使用する python version。`3.11` や `3.12` のように指定する
