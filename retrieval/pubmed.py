from Bio import Entrez

Entrez.email = "azlaanmohammad66@gmail.com"

def fetch_pubmed(query: str, max_results: int = 5) -> list[dict]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]
    if not ids:
        return []

    handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="text")
    raw = handle.read()

    abstracts = [a.strip() for a in raw.strip().split("\n\n\n") if a.strip()]
    return [{"pmid": pmid, "abstract": ab} for pmid, ab in zip(ids, abstracts)]

if __name__ == "__main__":
    results = fetch_pubmed("epilepsy seizure detection machine learning")
    for r in results:
        print(f"PMID: {r['pmid']}\n{r['abstract']}\n{'-'*60}")
