from bs4 import BeautifulSoup
import requests
import json
from functools import reduce

url = "https://itch.io/games"
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

output = []
for game in soup.findAll(attrs={"class":"game_cell"})[15:20]:
# game = soup.find(attrs={"class":"game_cell"})
	output.append(
		{
			"title": game.find(attrs={"class":"game_title"}).string,
			"id": game.get("data-game_id"),
			"desc": game.find(attrs={"class":"game_text"}).text,
			"author": game.find(attrs={"class":"game_author"}).string,
			"genre": game.find(attrs={"class":"game_genre"}).text if game.find(attrs={"class":"game_genre"}) is not None else None,
			"platform": list(map(lambda game: game.find("span").get("title")[13:],game.findAll(attrs={"class":"game_platform"})))
		}
	)
for game in soup.findAll(attrs={"class":"game_cell"})[15:20]:
	print(game.findAll(attrs={"class":"game_platform"}).map(lambda p: p.find("span")))
	# print(list(map(lambda game: game.find("span").get("title")[13:],game.findAll(attrs={"class":"game_platform"}))))
with open('test.json', 'w') as outfile:
	json.dump(output, outfile);