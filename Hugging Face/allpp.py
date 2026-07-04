from huggingface_hub import HfApi

api = HfApi()
papers = list(api.list_papers(query="diffusion models", limit=10))

print(papers)