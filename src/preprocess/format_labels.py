import pandas as pd
import os
'''Format labels in CSV containing quality rating
   - Rename files
   - Assign each decimal quality rating to a category
   
   Input - CSV file contianing image names, their Mean opinion scores, and stdev of that score in the dataset.
    Distribution is heavilty right-skewed and roughly normal (most values are to the left of the mean).
   
   '''
def process_data_labels():
    """
    Reads image filenames and labels from 'data/BIQ2021.csv', cleans the filenames by replacing spaces with underscores and removing parentheses,
    updates the DataFrame, prints the number of filenames changed, displays sample rows, and exports the cleaned data to 'data/BIQ2021_cleaned.csv'.
    Returns:
        None
    """
    input_data_filename = "data/BIQ2021.csv"
    data = pd.read_csv(input_data_filename)


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

    labelled_dataset_path = "data/BIQ2021_cleaned.csv"
    data_labels = pd.read_csv(labelled_dataset_path)
    

    min = data_labels['MOS'].min()
    q1 = data_labels['MOS'].quantile(q=0.25, interpolation='nearest')
    q2 = data_labels['MOS'].quantile(q=0.5, interpolation='nearest')
    q3 = data_labels['MOS'].quantile(q=0.75, interpolation='nearest')
    max = data_labels['MOS'].max()


    print('Summary stats of mean opinion score (MOS):\n',
           f'min: {min}',
           f'q1: {q1}',
           f'q2: {q2}',
           f'q3: {q3}',
           f'max: {max}')


    quality_bins = [min, q1, q2, q3, max]

    # quality_


    names = ['unusable', 'low', 'medium', 'high']

    data_labels['QualityRating'] = pd.cut(data_labels['MOS'], quality_bins, labels=names)

    # Save back from dataframe to csv
    # dataframe_name = pd.to_csv('out_filepath.csv')
    data_labels.to_csv(labelled_dataset_path, sep = '\t')

    # Labelled data preprocessed
    '''
    The file contains 3 attributes, MOS is the target variable whereas the image only or image as well as standard deviation can be used as independent variable:

    Images: provide the name of the image with correct file extension.

    MOS: provides corresponding mean opinion score (MOS) for each image and will be used as target label.

    StandardDeviation: provides the standard deviation of ratings obtained from several subjects which can be used as attribute during training.
    '''


    print(data_labels.head(10))


process_data_labels()
assign_quality_label()