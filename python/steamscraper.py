from bs4 import BeautifulSoup
import requests
import json

root = "https://store.steampowered.com/app/" 
gameUrl = "601150/Devil_May_Cry_5/"		 #example
url = root + gameUrl
response = requests.get(url, timeout=5)
soup = BeautifulSoup(response.content, "html.parser")

output = []
output.append(
	{
		"title": soup.find(attrs={"class":"apphub_AppName"}).text,
		"franchise": soup.find(text="Franchise:").parent.next_sibling.next_sibling.text,
		"developer": soup.findAll(attrs={"class": "dev_row"})[1].find("a").text,
		"publisher": soup.find(attrs={"class": "dev_row"}).find("a").text,
		"releaseDate": soup.find(attrs={"class":"release_date"}).find(attrs={"class":"date"}).text,
		"price": soup.find(attrs={"class":"game_purchase_price"}).string.strip(),
		"genre": soup.find(attrs={"class":"details_block"}).find("a", href=lambda href: href and "genre" in href).text.strip(),
		"esrb": soup.find("img", src=lambda src: src and "ratings" in src).get("src")[-5:-4].capitalize(),
		"review": soup.find(attrs={"class":"game_review_summary"}).text,
		"reviewCount": soup.find(attrs={"itemprop":"reviewCount"}).get("content")
		# "tags": [].append(soup.find(attrs={"class":"app_tag"})),
	}
)

# print(list(filter(lambda style: "none" not in style, )))
# print(soup.findAll("a", attrs={"class":"app_tag"}, style=lambda style: style and "none" not in style))
# print(output);
with open('output.json', 'w') as outfile:
	json.dump(output, outfile);