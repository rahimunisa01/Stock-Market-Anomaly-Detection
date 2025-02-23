import os
import subprocess
import pandas as pd
from kaggleapi import KAGGLE_USERNAME, KAGGLE_KEY, DATASET_ID, EXCEL_FILE

def connection_kaggle():
    os.environ['KAGGLE_USERNAME'] = KAGGLE_USERNAME
    os.environ['KAGGLE_KEY'] = KAGGLE_KEY
    os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    with open(kaggle_json_path, "w") as f:
        f.write('{"username": "%s", "key": "%s"}' % (KAGGLE_USERNAME, KAGGLE_KEY))
    os.chmod(kaggle_json_path, 0o600)

def reading_dataset():
    zipfile = f"{DATASET_ID.split('/')[-1]}.zip"
    subprocess.run(["kaggle", "datasets", "download", "-d", DATASET_ID], check=True)
    subprocess.run(["unzip", "-o", zipfile], check=True)

def load_data():
    data = pd.read_excel(EXCEL_FILE, parse_dates=["Date"])
    return data

if __name__ == "__main__":
    connection_kaggle()
    reading_dataset()
    data = load_data()