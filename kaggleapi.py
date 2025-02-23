from dotenv import load_dotenv
import os
load_dotenv()

#the kaggle credentials
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

#dataset details
DATASET_ID = "suruchiarora/yahoo-finance-dataset-2018-2023"
EXCEL_FILE = "yahoo_data.xlsx"
