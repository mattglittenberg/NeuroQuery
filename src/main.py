from utils.helpers import load_config
from src.ingestion.pubmed_fetch import fetch_pubmed_data

def run_pipeline():
    config = load_config()

    print("Step 1: Getting PubMed data...")

    fetch_pubmed_data(
        query=config["ingestion"]["query"],
        output_path=config["data"]["raw_path"],
        retmax=config["ingestion"]["retmax"]
    )
