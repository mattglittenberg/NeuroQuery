import requests
import time
import json
from pathlib import Path
from src.utils.helpers import ensure_dir
import xml.etree.ElementTree as ET


base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query, retmax=1000):
    """
    Get PubMed IDs (PMIDs) for query
    """

    url = base_url + "esearch.fcgi"

    param = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json"
    }

    response = requests.get(url, params=param)
    response.raise_for_status()

    data_pull = response.json()
    id_list = data_pull["esearchresult"]["idlist"]

    return id_list


def fetch_details(id_list, batch_size=200, sleep_time=0.5):
    """
    Fetch article detils 
    """
    
    url = base_url + "esearch.fcgi"
    all_records = []

    for i in range(0, len(id_list), batch_size):
        batch_ids = id_list[i:i + batch_size]

        param = {
            "db": "pubmed",
            "id": ",".join(batch_ids),
            "retmode": "xml"
        }

        response = requests.get(url, params=param)
        response.raise_for_status()

        records = parse_pubmed_xml(response.text)
        all_records.extend(records)

        time.sleep(sleep_time)

    return all_records


def parse_pubmed_xml(xml_text):
    """
    Parse XML response into structured records
    """

    root = ET.fromstring(xml_text)
    records = []

    for article in root.findall(".//PubmedArticle"):
        try:
            pmid = article.findtext(".//PMID")
            title = article.findtext(".//ArticleTitle")

            abstract_nodes = article.findall(".//AbstractText")
            abstract = " ".join([node.text for node in abstract_nodes if node.text])

            records.append({
                "id": pmid,
                "title": title,
                "abstract": abstract
            })
        except Exception:
            continue

    return records


def fetch_pubmed_data(query, output_path, retmax=1000):
    """
    Run full pipeline: search, fetch, save
    """

    print(f"Searching PubMed for: {query}")
    id_list = search_pubmed(query, retmax=retmax)

    print(f"Found {len(id_list)} articles")

    print("Getting article details...")
    records = fetch_details(id_list)

    print(f"Found {len(records)} records")

    ensure_dir(Path(output_path).parent)

    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    fetch_pubmed_data(
        query="Alzheimers disease AND biomarkers",
        output_path = "data/raw/pubmed_raw.json",
        retmax=1000
    )