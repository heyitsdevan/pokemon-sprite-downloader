import requests
from bs4 import BeautifulSoup
import os 
import threading
import json

# Change directory to store images into new path
os.chdir("")
url = "https://pokemondb.net/pokedex/shiny"

# Progress bar
# Panda DF for data

def main():
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    container = soup.find(id="main").find("div", class_="infocard-list infocard-list-pkmn-lg")
    pokemons = container.find_all('div', class_="infocard")
    threads = []
    pokedex = {}
    
    for pokemon in pokemons:
        # Grab data (id, name, type)
        id = pokemon.find("span", class_="infocard-lg-data text-muted").find('small').text[1:]
        name = pokemon.find('span', class_='img-fixed shinydex-sprite shinydex-sprite-normal').get('data-alt').split(" ")[0]
        typing = pokemon.find("span", class_="infocard-lg-data text-muted").find_all('small')[1].find_all('a')
        typing = [type.text for type in typing]
        pokedex[name] = [id, typing]

        # Grab image urls (normal, shiny)
        normal_sprite_url = pokemon.find("span", class_="infocard-lg-img").find('span', class_='img-fixed shinydex-sprite shinydex-sprite-normal').get('data-src')
        shiny_sprite_url = pokemon.find("span", class_="infocard-lg-img").find('span', class_='img-fixed shinydex-sprite shinydex-sprite-shiny').get('data-src')

        # Download Images
        shiny_image = requests.get(shiny_sprite_url).content
        normal_image = requests.get(normal_sprite_url).content
        # saveImage(id, name, typing, shiny_image, normal_image)
        save = threading.Thread(target=saveImage(id, name, shiny_image, normal_image))
        threads.append(save)
        save.start()

    for thread in threads:
        thread.join() 
    # saveData(pokedex)


def saveImage(id, name, shiny_image, normal_image):
    normal_title = f"{id}-{name}.jpg"
    shiny_title = f"{id}-Shiny {name}.jpg"
    with open(normal_title, 'wb') as file:
        file.write(normal_image)
    with open(shiny_title, 'wb') as file:
        file.write(shiny_image)


def saveData(data):
    os.chdir("C:\\Users\\Devan\Documents\\Python Projects\\Sword&Shield")    
    with open('pokedex.txt', 'w') as file:
        file.write(json.dumps(data))


if __name__ == '__main__':
    main()
