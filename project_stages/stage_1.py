import requests


# Project stage 1/5: Wanna Talk to the Internet?
#
url = input("Input the URL:\n")

response = requests.get(url)
content = response.json().get("content")

if response.status_code != 200 or not content:
    print("Invalid quote resource!")
else:
    print(content)
