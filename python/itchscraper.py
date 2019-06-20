from bs4 import BeautifulSoup
import requests
import json

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def insertSort(list: list, append: list):
    for i in append:
        index = 0
        if(len(list) > 0):
            while list[index]["id"] < i["id"]:
                index = index + 1
                if(index >= len(list)):
                    break
            list.insert(index, i)
        else:
            list.append(i)


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


rootUrl = "https://itch.io"
tagPageUrl = "/tags"
pageUrl = "?page="
tagUrl = ""

gamesPerPage = 30
tagPageCount = 10

# tags = []
# for i in range(0, tagPageCount):
#     getUrl = rootUrl + tagPageUrl + pageUrl + str(i)
#     getTagResponse = requests.get(getUrl, timeout=5)
#     getTagSoup = BeautifulSoup(getTagResponse.content, "html.parser")
#     for t in [tag.get("href") for tag in getTagSoup.findAll(attrs={"class": "tag_title"})]:
#         tagPageUrl = rootUrl + str(t) + pageUrl
#         tagResponse = requests.get(tagPageUrl, timeout=5)
#         tagSoup = BeautifulSoup(tagResponse.content, "html.parser")
#         gameCount = locale.atoi(tagSoup.find(
#             attrs={"class": "game_count"}).text[2:-9])
#         pageCount = int(gameCount/gamesPerPage) + 1
#         tags.append({
#             "tag": str(t)[11:] if str(t).find("genre") == -1 else str(t)[13:],
#             "tagUrl": t,
#             "count": gameCount,
#             "pageCount": pageCount})

# with open('tags.json', 'w') as outfile:
# 		json.dump(tags, outfile)

urlByTag = []
with open('tags.json', 'r') as tagsIn:
    for tag in json.load(tagsIn):
        urls = []
        for page in range(1, tag["pageCount"]):
            tagEnder = tag["tagUrl"] + pageUrl + str(page)
            url = rootUrl + tagEnder
            urls.append(url)
        urlByTag.append({"tag": tag["tag"], "urls": urls})


for tag in urlByTag:
    output = []

    for url in tag["urls"]:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        append = []
        for game in soup.findAll(attrs={"class": "game_cell"}):
            append.append(
                {
                    "title": game.find(attrs={"class": "game_title"}).find(attrs={"class": "title"}).string if game.find(attrs={"class": "game_title"}) is not None else None,
                    "id": int(game.get("data-game_id")) if game.get("data-game_id") is not None else None,
                    "desc": game.find(attrs={"class": "game_text"}).text if game.find(attrs={"class": "game_text"}) is not None else None,
                    "author": game.find(attrs={"class": "game_author"}).string if game.find(attrs={"class": "game_author"}) is not None else None,
                    "genre": [],
                    "platform": ([(platform.get("title")[13:] if platform.has_attr("title") else "Browser") for platform in game.find(attrs={"class": "game_platform"}).findAll("span")] if game.find(attrs={"class": "game_platform"}) is not None else [])
                }
            )
        # print(append)

        insertSort(output, append)  # sort as chunk or individual?

    with open(tag["tag"] + '.json', 'w') as outfile:
        json.dump(output, outfile)

# itch = []

# for tag in urlByTag:
#     with open(tag["tag"] + '.json', 'r') as infile:
#         for game in json.load(infile):
#             find = binSearch(itch, 0, len(itch)-1, game["id"])
#             if(find != -1):
#                 itch[find]["genre"].append(tag["tag"])
#             else:
#                 insertSort(itch, [game])

# with open('itch.json', 'w') as outfile:
#     json.dump(itch, outfile)
