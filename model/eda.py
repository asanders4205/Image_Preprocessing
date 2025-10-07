'''
Take a look at the dataset, find high and low quality image, etc
'''
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd


def eda():

    labelled_dataset_path = "data\BIQ2021_cleaned.csv"
    
    data_labels = pd.read_csv(labelled_dataset_path)

    print(data_labels.head(10))


eda()