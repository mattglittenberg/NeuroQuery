import pandas as pd
import json
import re

def clean_text(text):
    """
    Clean text from JSON for processing.

    Takes text and changes it to all lower case,
    removes all special characters, and strips all
    extra whitespace. Then returns clean text.

    Parameters
    ----------
    text : str, required
        Text to be cleaned.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()

def preprocess(input_path, output_path):
    """
    Preprocesses raw text data.

    Takes raw data from JSON, converts to 
    a Pandas DataFrame, removes missing abstract 
    entries and duplicates, cleans text, and outputs 
    a parquet data file.

    Parameters
    ----------
    input_path : str, required
        Filepath to raw JSON data file
    output_path: str, required
        Filepath to output cleaned data
    """

    with open(input_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df = df.dropna(subset=["abstract"])
    df = df.drop_duplicates(subset=["abstract"])

    df["cleaned_text"] = df["abstract"].apply(clean_text)
    df = df[~df["title"].isin(["Association of ", "Associations of "])]

    df.to_parquet(output_path, index=False)

if __name__ == "__main__":
    preprocess("data/raw/pubmed_raw.json", "data/processed/cleaned.parquet")