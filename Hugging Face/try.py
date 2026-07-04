from huggingface_hub import HfApi

api = HfApi()

# List daily papers sorted by trending
# for paper in api.list_daily_papers(sort="trending",limit=1):
#     # print(paper.title, paper.published_at)
#     print(paper)

# Or fetch papers for a specific date
# papers = list(api.list_daily_papers(date="2026-05-01", sort="trending", limit=10))

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

p = get_hf()
for pr in p:
    print(p)
    print("-" * 50)