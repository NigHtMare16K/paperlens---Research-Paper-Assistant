#Arxiv 
import feedparser

def get_arxiv(query):
    papers = []
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10'

    feed = feedparser.parse(url)
    papers = []
    for entry in feed.entries:
        title = entry.title
        summary = entry.summary

        authors = [author.name for author in entry.authors]

        pdf_link = ""
        for link in entry.links:
            if link.type == "application/pdf":
                pdf_link = link.href

        abstract_link = entry.id

        papers.append({
        "Title": title,
        "Authors": authors,
        "Summary": summary,
        "PDF": pdf_link,
        "Abstract": abstract_link
        })

    return papers

# p = get_arxiv("MachineLearning")
# for pr in p:
#     print(pr)
#     print("-" * 50)

#HF Papers
from huggingface_hub import HfApi

api = HfApi()

from huggingface_hub import HfApi

api = HfApi()
def get_hf():
    hf_papers = []
    for paper in api.list_daily_papers(sort="trending", limit=5):
        title = paper.title
        arxiv_id = paper.id
        authors = [a.name for a in paper.authors]

        abstract_url = f"https://arxiv.org/abs/{arxiv_id}"
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        summary = paper.summary
        upvotes = paper.upvotes

        hf_papers.append({
            "Title": title,
            "id": arxiv_id,
            "Authors": [authors],
            "Abstract_Url": abstract_url,
            "Pdf": pdf_url,
            "Summary": summary,
            "Upvotes": upvotes
        })

    return hf_papers

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