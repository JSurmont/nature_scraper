import string
import requests
from bs4 import BeautifulSoup


# Project stage 4/5: The Soup is Real
#
url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
domain = "https://www.nature.com"

main_response = requests.get(url)

if not main_response.status_code == 200:
    print(f"Couldn't get source code from url, status code: {main_response.status_code}.\n")
    exit()

main_soup = BeautifulSoup(main_response.content, "html.parser")

articles_list = main_soup.find_all("article")

file_found_count = 0
teaser_count = 0
saved_article_files = []
saved_teaser_files = []

for article_card in articles_list:
    if not article_card.find_all("span", attrs={"class": "c-meta__type"})[0].text == "News":
        continue

    file_found_count += 1

    href = article_card.a.get('href')
    link = domain + href

    article_response = requests.get(link)

    if not article_response.status_code == 200:
        print(f"Couldn't access the article: \"{article_card.a.text}\", at the following url : {link}.\n")
        continue

    article_soup = BeautifulSoup(article_response.content, "html.parser")

    title = article_soup.find("title").text
    file_name = title.translate({ord(i): None for i in string.punctuation})
    file_name = file_name.translate({ord(i): '_' for i in string.whitespace})
    file_name = file_name + ".txt"

    article = article_soup.find('div', attrs={"class": "c-article-body main-content"})
    if article:
        article = article.p.text
        teaser_file = open(file_name, 'wb')
        teaser_file.writelines(article.encode())
        teaser_file.close()
        saved_article_files.append(file_name)
    else:
        print(f"Couldn't retrieve the article: \"{title}\", at the following url : {link}.")
        teaser = article_soup.find('p', attrs={"class": "article__teaser"}).text
        if teaser:
            teaser_count += 1
            teaser_file = open(file_name, 'ab')
            teaser_file.write(f"Article is not in free access.\n".encode())
            teaser_file.write(f"It can be consulted at the url: {link}.\n".encode())
            teaser_file.write(f"Following is the teaser for the article:\n\n".encode())
            teaser_file.write(teaser.encode())
            teaser_file.close()
            saved_teaser_files.append(file_name)
            print("Teaser has been retrieved instead.\n")

saved_files_length = len(saved_article_files)

if file_found_count > 0:
    if saved_files_length == 0:
        print(f"No article could be retrieved ({file_found_count} found).\n")
    else:
        print(f"Not all articles could be retrieved. Found {file_found_count}, saved {saved_files_length}.\n")
        print(f"Saved files:\n{saved_article_files}.\n")
    if len(saved_teaser_files) > 0:
        print(f"Available teaser(s) retrieved for the non accessible article(s):\n{saved_teaser_files}")
elif file_found_count == 0:
    print("No article found.\n")
else:
    print(f"{file_found_count} found and saved.\nSaved files:\n{saved_article_files}.\n")
