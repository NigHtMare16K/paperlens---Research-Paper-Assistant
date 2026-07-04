import urllib.request
import urllib.parse

topic = input("Enter topic: ")

query = urllib.parse.quote(topic)
url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1'

data = urllib.request.urlopen(url)

dec = data.read().decode('utf-8')

print(dec[summary])