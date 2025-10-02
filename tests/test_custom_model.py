import pytest
import pandas as pd
import os
from model import custom_model

@pytest.fixture
def sample_csv(tmp_path):
    # Create a sample CSV file
    csv_path = tmp_path / "BIQ2021.csv"
    df = pd.DataFrame({
        "filename": ["img (1).jpg", "img 2.jpg", "img3.jpg"],
        "label": [1, 0, 1]
    })
    df.to_csv(csv_path, index=False)
    # Create data directory and move file
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path.rename(data_dir / "BIQ2021.csv")
    return data_dir

def test_process_data_labels(monkeypatch, sample_csv, tmp_path):
    # Patch os.getcwd to tmp_path so relative paths work
    monkeypatch.chdir(tmp_path)
    # Patch print to suppress output
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    # Run function
    custom_model.process_data_labels()
    # Check output file exists
    cleaned_path = tmp_path / "data" / "BIQ2021_cleaned.csv"
    assert cleaned_path.exists()
    # Check contents
    df = pd.read_csv(cleaned_path)
    assert df["filename"].tolist() == ["img_1.jpg", "img_2.jpg", "img3.jpg"]
    assert df["label"].tolist() == [1, 0, 1]