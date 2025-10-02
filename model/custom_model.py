



# '''Format the BIQ2021 image label file'''
# def process_filenames_in_labelled_data(path: str):
#     '''Remove certain characters from filenames
#     '''
#     print('Processing filenames')
#     replacements = {" ":"_", "(":"", ")":""}
#     files = sorted(os.listdir(path))
#     counter = 0

#     for file_name in files:
#         new_name = file_name
#         # counter += 1
#         for old,new in replacements.items():
#             new_name = new_name.replace(old, new)

#         if new_name != file_name: # Rename if changed
#             old_path = os.path.join(path, file_name)
#             new_path = os.path.join(path, new_name)
#             os.rename(old_path, new_path)
#             counter += 1

#     print(f'Filenames processed: {counter} filenames changed')




'''Convert to pandas df
iterate over rows
in col 0 replace certain chars with others'''

import pandas as pd
data = pd.read_csv('data\BIQ2021.csv')


for i, row in data.head(2).iterrows():
    new_col_name = data.iloc[i,0]
    print(new_col_name)