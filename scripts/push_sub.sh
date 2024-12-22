#!/bin/bash
set -e
cd ./sub || { echo "Failed to enter ./sub directory"; exit 1; }
kaggle k push || { echo "Kaggle push failed"; exit 1; }
cd - > /dev/null  # 直前のディレクトリに戻る
