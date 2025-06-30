import zipfile
import os

def extract_files_from_zip(zip_path : str, extract_path: str) -> None:
    # Create the dir 
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    
    print(f"Extracted all zip files to {extract_path}")


if __name__ == "__main__":
    extract_files_from_zip(zip_path="dataset.zip", extract_path="dataset")