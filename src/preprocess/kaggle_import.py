import kagglehub


def import_dataset_from_kaggle(url: str) -> str:
    '''
        Get images from kaggle dataset 
        Input: URL
        Output: Local filepath in .cache/kagglehub
    '''
    # Download latest version
    output_path = kagglehub.dataset_download(url)

    print('Downloaded dataset from {url}\n to folder: {output_path}')

    return output_path