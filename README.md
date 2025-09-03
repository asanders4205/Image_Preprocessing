'''
# Image Quality Classifier #

## The goal of this process is to classify images as good quality or bad quality! ##
We will be using the BIQ2021 dataset found on Kaggle here:\
https://www.kaggle.com/datasets/nisarahmedrana/biq2021

The processing will be done step-by-step\
    and will reference the Knowledge Discovery in Databases (KDD) process outlined below

Selection:  identify and collect relevant data\
    > Load in the dataset\
Preprocessing:  clean and handle missing/noisy data.\
    > Resizing\
    > Grayscaling\
    > Noise reduction\
    > Normalization\
    > Binarization\
    > Contrast enhancement\
Transformation:  normalize, reduce, or engineer features \
Data Mining:  apply algorithms (classification, clustering, etc.) \
Evaluation:  assess results, interpret patterns \
Knowledge/Deployment:  use insights in decision-making


## To get started ##
Create a 'data' folder in your project directory \
In your terminal run 'pip install -r requirements.txt' to install requirements \
Execute the code to download the dataset via this line\
    path = kagglehub.dataset_download("nisarahmedrana/biq2021") \

README will be updated as the project moves along