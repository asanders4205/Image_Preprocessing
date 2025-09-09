'''
# Image Quality Classifier #

## The goal of this process is to classify images as good quality or bad quality! ##

Programmed using the BIQ2021 dataset found on Kaggle here:\
https://www.kaggle.com/datasets/nisarahmedrana/biq2021


Uses python 3.9+ \
Programmed on Windows, may not be portable. Modifications to follow 

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
Activate a virtual environment if you so choose \
Ensure you are using python 3.9+ \
Create a 'data' folder in your project directory \
In your terminal run 'pip install -r requirements.txt' to install requirements \
Execute the code to download the dataset via this line\
    path = kagglehub.dataset_download("nisarahmedrana/biq2021") \

README will be updated as the project moves along


## Future expansions ##
- Compatibility with image datasets outside of Kaggle