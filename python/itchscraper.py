from bs4 import BeautifulSoup
import requests
import json

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

rootUrl = "https://itch.io/games"
tagPageUrl = "/tags"
pageUrl = "?page="
tagUrl = ""

gamesPerPage = 30
tagPageCount = 10

tags = []
# for i in range(1, tagPageCount):
#     getUrl = rootUrl + tagPageUrl + pageUrl + str(i)
#     getTagResponse = requests.get(getUrl, timeout=5)
#     getTagSoup = BeautifulSoup(getTagResponse.content, "html.parser")
#     for t in [tag.get("href") for tag in getTagSoup.findAll(attrs={"class": "tag_title"})]:
#         tags.append(t)


# tagPageUrl = rootUrl + str(tags[0]) + pageUrl
# tagResponse = requests.get(tagPageUrl, timeout=5)
# tagSoup = BeautifulSoup(tagResponse.content, "html.parser")
# pageCount = int(locale.atoi(tagSoup.find(
#     attrs={"class": "game_count"}).text[2:-9])/gamesPerPage) + 1

url = rootUrl
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

output = []

for game in soup.findAll(attrs={"class": "game_cell"}):
    output.append(
        {
            "title": game.find(attrs={"class": "game_title"}).find(attrs={"class": "title"}).string if game.find(attrs={"class": "game_title"}) is not None else None,
            "id": int(game.get("data-game_id")) if game.get("data-game_id") is not None else None,
            "desc": game.find(attrs={"class": "game_text"}).text if game.find(attrs={"class": "game_text"}) is not None else None,
            "author": game.find(attrs={"class": "game_author"}).string if game.find(attrs={"class": "game_author"}) is not None else None,
            "genre": [],
            "platform": [l.get("title")[13:] for l in [p.findAll("span")
                                                       for p in game.findAll(attrs={"class": "game_platform"})] for l in l]
        }
    )


def insertSort(list: list, append: list):
    for i in append:
        index = 0
        while list[index]["id"] < i["id"]:
            index = index + 1
        else:
            list.insert(index, i)


def binSearch(list: list, l: int, r: int, val: int) -> int:
    if r >= l:
        m = l + int((r - l)/2)
        if list[m]["id"] == val:
            return m
        elif list[m]["id"] > val:
            return binSearch(list, l, m-1, val)
        else:
            return binSearch(list, m + 1, r, val)
    else:
        return -1


with open('output.json', 'w') as outfile:
    json.dump(output, outfile)
