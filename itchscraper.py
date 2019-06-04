from bs4 import BeautifulSoup
import requests
import json
import itertools

url = "https://itch.io/games"
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

output = []
for game in soup.findAll(attrs={"class": "game_cell"})[:20]:
    # game = soup.find(attrs={"class":"game_cell"})
    output.append(
        {
            "title": game.find(attrs={"class": "game_title"}).find(attrs={"class": "title"}).string,
            "id": game.get("data-game_id"),
            "desc": game.find(attrs={"class": "game_text"}).text,
            "author": game.find(attrs={"class": "game_author"}).string,
            "genre": game.find(attrs={"class": "game_genre"}).text if game.find(attrs={"class": "game_genre"}) is not None else None,
            "platform": [l.get("title")[13:] for l in [p.findAll("span")
                                                       for p in game.findAll(attrs={"class": "game_platform"})] for l in l]
        }
    )
# for game in soup.findAll(attrs={"class": "game_cell"})[15:20]:
#     print([l.get("title")[13:] for l in [p.findAll("span")
#                                          for p in game.findAll(attrs={"class": "game_platform"})] for l in l])
    # print(list(map(lambda game: game.find("span").get("title")[13:],game.findAll(attrs={"class":"game_platform"}))))
with open('test.json', 'w') as outfile:
    json.dump(output, outfile)
