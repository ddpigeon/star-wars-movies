from bs4 import BeautifulSoup
import requests
import lxml

import json

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
link = "https://www.imdb.com/list/ls029559286/"

site = BeautifulSoup(requests.get(link,headers=headers).content,features="lxml")

complete_list = site.find("div", {"class" : "list-description"}).findAll("li")

data = [x.split(">")[1].split("<")[0] for x in str(complete_list).split(",")]

movie_dict = []
counter = 1

for i in data:

    name = i

    try:
        year = i.split("(")[1].split(")")[0]
    except IndexError:
        year = "Not Found"
    new_string = ""

    for j in i:
        if j == " ":
            new_string += "%20"
        elif j == ":":
            new_string += "%3A"
        else:
            new_string += j

    new_link = f"https://www.imdb.com/find/?q={new_string}"

    site = BeautifulSoup(requests.get(new_link,headers=headers).content,features="lxml")
    new_movie_link = site.find("a", {"class" : "ipc-metadata-list-summary-item__t"})["href"]

    new_movie_link = f"https://www.imdb.com{new_movie_link}"

    site_data = BeautifulSoup(requests.get(new_movie_link,headers=headers).content,features="lxml")

    try:
        rating = str(site_data.find("span", {"class" : "sc-bde20123-1 iZlgcd"})).split(">")[1].split("<")[0]
    except IndexError:
        rating = "Not Found"

    try:
        var1 = site_data.find("div", {"class" : "sc-e226b0e3-6 hfusNC"}).findAll("li", {"class" : "ipc-metadata-list__item ipc-metadata-list-item--link"})[-1]
        var2 = str(var1.findAll("li", {"class" : "ipc-inline-list__item"})).split(",")

        stars = []

        for i in var2:
            star = i.split(">")[2].split("<")[0]
            stars.append(star)

        star_string = ""

        for i in stars[:-1]:
            star_string += f"{i}, "

        star_string += stars[-1]

    except:
        star_string = "Not Found"

    movie_dict.append({
        "Name" : name,
        "Year" : year,
        "Rating" : rating,
        "Stars" : star_string
    })

    counter += 1

with open("movies.json", "w") as f:
    json.dump(movie_dict, f, indent = 2)