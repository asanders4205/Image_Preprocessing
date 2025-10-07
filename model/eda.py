'''
Take a look at the dataset, find high and low quality image, etc
'''
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd


def eda():
    # input_data_filename = "data/BIQ2021_cleaned.csv"
    # df = pd.read_csv(input_data_filename)

    # print(df.head(5))


    labelled_dataset_path = "data\BIQ2021_cleaned.csv"
    
    data_labels = pd.read_csv(labelled_dataset_path)
    



    # Save back from dataframe to csv
    # dataframe_name = pd.to_csv('out_filepath.csv')
    # data_labels.to_csv(labelled_dataset_path, sep = '\t')

   

    print(data_labels.head(10))



eda()