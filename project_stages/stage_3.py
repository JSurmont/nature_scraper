import requests


# Project stage 3/5: What the File?
#
url = input("Input the URL:\n")

response = requests.get(url)

if response.status_code == 200:
    page_content = response.content
    source_file = open("source.html", 'wb')
    source_file.write(page_content)
    source_file.close()
    print("Content saved.")
else:
    print("The URL returned " + str(response.status_code))
