#!/bin/bash
set -e
cd ./deps || { echo "Failed to enter ./deps directory"; exit 1; }
kaggle k push || { echo "Kaggle push failed"; exit 1; }
cd - > /dev/null  # 直前のディレクトリに戻る
