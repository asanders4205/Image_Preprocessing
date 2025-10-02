import pandas as pd
import os

def process_data_labels():
    """
    Reads image filenames and labels from 'data/BIQ2021.csv', cleans the filenames by replacing spaces with underscores and removing parentheses,
    updates the DataFrame, prints the number of filenames changed, displays sample rows, and exports the cleaned data to 'data/BIQ2021_cleaned.csv'.
    Returns:
        None
    """
    data = pd.read_csv("data/BIQ2021.csv")


    print("Processing filenames")
    replacements = {" ": "_", "(": "", ")": ""}

    counter = 0

# Apply replacements directly to the first column (filenames)
    new_filenames = []
    for file_name in data.iloc[:, 0]:
        new_name = file_name
        for old, new in replacements.items():
            new_name = new_name.replace(old, new)
        if new_name != file_name:
            counter += 1
        new_filenames.append(new_name)

# Update dataframe with cleaned filenames
    data.iloc[:, 0] = new_filenames

    print(f"Filenames processed: {counter} filenames changed")

# Show sample rows
    for i, row in data.head(2).iterrows():
        print(i, row)
        print()

# Export cleaned DataFrame to a new CSV
    data.to_csv("data/BIQ2021_cleaned.csv", index=False)
    print("Exported cleaned file list to data/BIQ2021_cleaned.csv")




def assign_quality_label():
    data = pd.read_csv("data/BIQ2021_cleaned.csv")    
    
    quality_bins = [0, 0.5, 0.75, 1]
    names = ['low', 'medium', 'high']

    data['QualityRating'] = pd.cut(data['MOS'], quality_bins, labels=names)

# Labelled data preprocessed
'''
The file contains 3 attributes, MOS is the target variable whereas the image only or image as well as standard deviation can be used as independent variable:

Images: provide the name of the image with correct file extension.

MOS: provides corresponding mean opinion score (MOS) for each image and will be used as target label.

StandardDeviation: provides the standard deviation of ratings obtained from several subjects which can be used as attribute during training.
'''


process_data_labels()
assign_quality_label()