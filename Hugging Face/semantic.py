import requests

def get_semantic_scholar(query):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": query,
        "limit": 5,
        "fields": "title,authors,abstract,url,openAccessPdf"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    print("Status:", response.status_code)

    data = response.json()
    print("Total results:", data.get("total"))

    papers = []

    for paper in data.get("data", []):
        title = paper.get("title")
        summary = paper.get("abstract")

        authors = [author["name"] for author in paper.get("authors", [])]

        pdf_link = ""
        if paper.get("openAccessPdf"):
            pdf_link = paper["openAccessPdf"].get("url", "")

        abstract_link = paper.get("url")

        papers.append({
            "Title": title,
            "Authors": authors,
            "Summary": summary,
            "PDF": pdf_link,
            "Abstract": abstract_link
        })

    return papers


papers = get_semantic_scholar("machine learning")

print("Fetched:", len(papers))

for p in papers:
    print(p)
    print("-" * 50)