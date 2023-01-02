'''
The goal is to crawl 500 song from spotify
the out put data will be save csv files to inport to database
artist:
    id(PK)  name    event   avatar
    
album:
    id(PK)  name    artists(FK) cover   publish_day
    
song:
    id(PK)  name    audio   artists(FK) albums(FK)
    
'''

from bs4 import BeautifulSoup
import requests
import re
import csv

SPOTIFY_URL = 'https://open.spotify.com'

def bs4_parser(page_link):
    #final result
    result = {}
    
    page_response = requests.get(page_link)
    page_content = BeautifulSoup(page_response.content, 'html.parser')
    
    #get artist info
    artist_name = page_content.find('h1').contents[0]
    artist_avatar = page_content.find_all('img', attrs={"data-testid":"artist-entity-image"})[0]['src']
    print(artist_name)
    print(artist_avatar)
    result_artist = {
        'name' : artist_name,
        'avatar' : artist_avatar,
    }
    
    #get artist album
    resutl_albums = {}
    albums_tag = page_content.find('h2', string="Albums")
    artist_albums = albums_tag.find_parent()
    artist_albums = artist_albums.findAll('a', attrs={"draggable" : "false"})
    for album in artist_albums:
        album_link = SPOTIFY_URL + album['href']
        album_cover = album.find('img')['src']
        album_name = album.find('span').contents[0]
        album_publish = album.find('div', attrs={"dir":"auto"}).contents[0]
        resutl_albums[album_name] = [album_link, album_cover, album_publish]

    #get artist song
    # for album in resutl_albums:
    first_value = next(iter(resutl_albums.values()))[0]
    print(first_value)  # 👉️ Bobby
    page_response = requests.get(first_value)
    page_content = BeautifulSoup(page_response.content, 'html.parser')
    song_detail = page_content.find_all('span', attrs={"dir" : "auto"})
    print(song_detail['src'])
        # print(song_detail[-1].findAll('a').contents)

    result['artist'] = result_artist
    result['albums'] = resutl_albums
    # print(result)
    return result
    
    
def csv_saver():
    
    return

def main():
    page_link = "https://open.spotify.com/artist/66CXWjxzNUsdJxJ2JdwvnR"
    bs4_parser(page_link)
    # csv_saver()
    return

if __name__ == "__main__":
    main()