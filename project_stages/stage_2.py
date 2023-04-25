import requests
from bs4 import BeautifulSoup


# Project stage 2/5:The Beautiful Soup Ingredients
#
url = input("Input the URL:\n")

if not url.startswith("https://www.nature.com/") or "articles" not in url:
    print("Invalid page!")
else:
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('title').text
    description = soup.find("meta", {"name": "description"}).get('content')

    result = {"title": title, "description": description}

    print(result)
