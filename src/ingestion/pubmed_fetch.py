import requests
import time
import json
import logging
from tqdm import tqdm
from pathlib import Path
from src.utils.helpers import ensure_dir
import xml.etree.ElementTree as ET


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query: str, reldate: int = 3650, retmax: int = 1000) -> list[str]:
    """
    Get PubMed IDs (PMIDs) for query.

    Uses the PubMed API to get article IDs matching the query and
    returns them as a list of IDs.

    Parameters
    ----------
    query : str, required
        Search query from user to be searched in the database.
    retmax : int, optional
        Max number of article ID numbers to return (defualt is 1000).
    reldate : int, optional
        Number of days in the past to include in the search (default is 3650 or 10 years)
    """

    url = BASE_URL + "esearch.fcgi"

    param = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "datetype": "pdat",
        "reldate": reldate
    }

    response = requests.get(url, params=param)
    response.raise_for_status()

    data_pull = response.json()
    id_list = data_pull["esearchresult"]["idlist"]

    return id_list


def fetch_details(id_list: list[str], batch_size: int = 200, sleep_time: float = 0.5) -> list[dict]:
    """
    Fetch and parse article details of ID list articles.

    Uses the PubMed API to get  details on article IDs. It
    then parses those details to isolate the title and abstract 
    and returns them as a list.

    Parameters
    ----------
    id_list : str, required
        List of article ID numbers to find details of.
    batch_size : int, optional
        size of batch to query the API with. Between 100-500 
        is customary (default is 200).
    sleep_time : int, optional
        Time between API querys. No more than 3 per 
        second (sleep_time=0.34) is allowed without 
        API key (default is 0.5, 2 per second).
    """
    
    url = BASE_URL + "efetch.fcgi"
    all_records = []

    for i in tqdm(range(0, len(id_list), batch_size), desc="Fetching Batches"):
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

def parse_pubmed_xml(xml_text: str) -> list[dict]:
    """
    Parse XML response into structured records.

    Takes in XML response from PubMed API efetch 
    and parses out PMID, Article Title, and Abstract.
    Then returns those items in a list.

    Parameters
    ----------
    xml_text : str, required
        XML response from PubMed API efetch.
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
        except Exception as e:
            logging.warning(f"Skipping article due to parse error: {e}")
            continue

    return records


def fetch_pubmed_data(query: str, output_path: str | Path, reldate: int = 3650, retmax: int = 1000) -> None:
    """
    Run full pipeline: search, fetch, save.

    Runs the full pipeline of searching the PubMed 
    database from searching the database based on 
    the query, to fetching the title and abstract,
    and finally saving to data/raw directory.

    Parameters
    ----------
    query : str, required
        Search query from user to be searched in the database.
    output_path : str, required
        size of batch to query the API with. Between 100-500 
        is customary (default is 200).
    retmax : int, optional
        Max number of article ID numbers to return (default is 1000).
    reldate : int, optional
        Number of days in the past to include in the search (default is 3650 or 10 years)
    """

    print(f"Searching PubMed for: {query}")
    id_list = search_pubmed(query, retmax=retmax, reldate=reldate)

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
        reldate=3650,
        retmax=1000
    )