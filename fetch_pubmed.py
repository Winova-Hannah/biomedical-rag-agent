import requests
import os
import time

SEARCH_TERM = "idiopathic pulmonary fibrosis TNIK"
MAX_RESULTS = 30
OUTPUT_FOLDER = "Data"

def search_pubmed(term, max_results):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_abstracts(id_list):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "rettype": "abstract",
        "retmode": "text"
    }
    response = requests.get(url, params=params)
    return response.text

def split_and_save(raw_text, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    articles = raw_text.split("\n\n\n")
    saved = 0

    for i, article in enumerate(articles):
        article = article.strip()
        if len(article) < 100:
            continue
        filename = os.path.join(folder, f"pubmed_{i+1}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(article)
        saved += 1

    return saved

if __name__ == "__main__":
    print(f"Searching PubMed for: {SEARCH_TERM}")
    ids = search_pubmed(SEARCH_TERM, MAX_RESULTS)
    print(f"Found {len(ids)} article IDs.")

    if not ids:
        print("No results found. Try a different search term.")
    else:
        print("Fetching abstracts...")
        raw_text = fetch_abstracts(ids)

        time.sleep(1)

        saved_count = split_and_save(raw_text, OUTPUT_FOLDER)
        print(f"Saved {saved_count} abstracts to '{OUTPUT_FOLDER}/'")
