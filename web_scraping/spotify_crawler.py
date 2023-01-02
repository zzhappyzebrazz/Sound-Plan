'''
The goal is to crawl 500 song from spotify
the out put data will be save csv files to inport to database
artist:
    id(PK)  name    event   avatar
    
list of artist:
    Ariana Grande
    Adele
    BingBang
    BlackPink
    Đen
    Bruno Mars
    Sam Smith
    Image Dragons
    Justin Timberlake
    Justin Bieber
    Lana Del Rey
    Taylor Swift
    LANY
    Chillies
    Ngọt
    Dua Lipa
    Jay Chou
    HONNE
    Hozier
    Phúc Du
    Post Malone
    Nujabes
    JustaTee
    Kimmese
    Binz
    ST M-TP
    AnnenMayKantereit
    Khalid
    Epik High
    Giveon
    Lady Gaga
    Bùi Lan Hương
    Westlife
    Nguyên Hà
    Cigarettes After Sex
    dhruv
album:
    id(PK)  name    artists(FK) cover   publish_day
    One Album for each Artist
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
    # print(page_content.find_all('img', attrs={"data-testid":"artist-entity-image"})[0])
    artist_avatar = page_content.find_all('img', attrs={"data-testid":"artist-entity-image"})[0]['src']
    result_artist = {
        'name' : artist_name,
        'avatar' : artist_avatar,
    }
    
    #get artist album
    result_album = {}
    albums_tag = page_content.find('h2', string="Albums")
    artist_albums = albums_tag.find_parent().find_parent()
    artist_albums = artist_albums.findAll('a', attrs={"draggable" : "false"})
    # print(artist_albums)
    album_link = SPOTIFY_URL + artist_albums[0]['href']
    album_cover = artist_albums[0].find('img')['src']
    album_name = artist_albums[0].find('span').contents[0]
    album_publish = artist_albums[0].find('div', attrs={"dir":"auto"}).contents[0]
    result_album[album_name] = [album_link, album_cover, album_publish]

    #get artist songs
    result_song = []
    for album in result_album:
        page_response = requests.get(result_album.get(album)[0])
        page_content = BeautifulSoup(page_response.content, 'html.parser')
        song_detail = page_content.find_all('div', attrs={"data-testid" : "track-row"})
        for temp in song_detail:
            song = []
            song.append(temp('a')[0].contents[0])
            link = temp('a')[0]['href']
            song.append(SPOTIFY_URL + link)
            for i in range(1, len(temp('a'))):
                song.append(temp('a')[i].contents[0])
            result_song.append(song)

    result['artist'] = result_artist
    result['albums'] = result_album
    result['song'] = result_song
    # print(result)
    return result
    
    
def csv_saver(result):
    lst_artist_name = []
    lst_artist_avartar = []
    lst_album_name = []
    lst_album_cover = []
    lst_public_day = []
    lst_song_name = []
    lst_audio  = []
    
    for temp in result:
        lst_artist_name.append(temp.get('artist').get('name'))
        lst_artist_avartar.append(temp.get('artist').get('avatar'))
        album_name, album_value = list(temp.get('albums').items())[0]
        lst_album_name.append(album_name)
        lst_album_cover.append(album_value[1])
        lst_public_day.append(album_value[2])
        songs = temp.get('song')
        
        for song in songs:
            # print(song)
            lst_song_name.append(song[0])
            lst_audio.append(song[1])
        
    print(lst_song_name)
    print(lst_audio)
    # print(lst_album_name)
    # print(lst_album_cover)
    # print(lst_public_day)
    #Save artist data
    dict_artist = {
        'id': [_id for _id in range(1, len(lst_artist_name) + 1)],
        'artist_name': lst_artist_name,
        'event': [_id for _id in range(1, len(lst_artist_name) + 1)],
        'avartar': lst_artist_avartar
    }
    with open('player_artist.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(dict_artist.keys())
        writer.writerows(zip(*dict_artist.values()))
        
    #Save album data
    dict_album = {
        'id': [_id for _id in range(1, len(lst_album_name) + 1)],
        'album_name': lst_album_name,
        'album_cover': lst_album_cover,
        'public_day': lst_public_day,
        'artists_id' : [_id for _id in range(1, len(lst_album_name) + 1)]
    }
    with open('player_album.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(dict_album.keys())
        writer.writerows(zip(*dict_album.values()))
        
    #Save songs data
    dict_song = {
        'id': [_id for _id in range(1, len(lst_song_name) + 1)],
        'song_name': lst_song_name,
        'audio': lst_audio,
        'album_id' : [_id for _id in range(1, len(lst_song_name) + 1)]
    }
    with open('player_song.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(dict_song.keys())
        writer.writerows(zip(*dict_song.values()))
        
    return

def main():
    artist_list = [
        'https://open.spotify.com/artist/66CXWjxzNUsdJxJ2JdwvnR', #Ariana Grande
        'https://open.spotify.com/artist/4dpARuHxo51G3z768sgnrY', #Adele
        'https://open.spotify.com/artist/4Kxlr1PRlDKEB0ekOCyHgX', #BingBang
        'https://open.spotify.com/artist/41MozSoPIsD1dJM0CLPjZF', #BlackPink
        'https://open.spotify.com/artist/1LEtM3AleYg1xabW6CRkpi', #Đen
        'https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C', #Bruno Mars
        'https://open.spotify.com/artist/2wY79sveU1sp5g7SokKOiI', #Sam Smith
        'https://open.spotify.com/artist/53XhwfbYqKCa1cC15pYq2q', #Image Dragons
        'https://open.spotify.com/artist/31TPClRtHm23RisEBtV3X7', #Justin Timberlake
        'https://open.spotify.com/artist/1uNFoZAHBGtllmzznpCI3s', #Justin Bieber
        'https://open.spotify.com/artist/00FQb4jTyendYWaN8pK0wa', #Lana Del Rey
        'https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02', #Taylor Swift
        'https://open.spotify.com/artist/49tQo2QULno7gxHutgccqF', #LANY
        'https://open.spotify.com/artist/2xvW7dgL1640K8exTcRMS4', #Chillies
        'https://open.spotify.com/artist/0V2DfUrZvBuUReS1LFo5ZI', #Ngọt
        'https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we', #Dua Lipa
        'https://open.spotify.com/artist/2elBjNSdBE2Y3f0j1mjrql', #Jay Chou
        'https://open.spotify.com/artist/0Vw76uk7P8yVtTClWyOhac', #HONNE
        'https://open.spotify.com/artist/2FXC3k01G6Gw61bmprjgqS', #Hozier
        'https://open.spotify.com/artist/246dkjvS1zLTtiykXe5h60', #Post Malone
        'https://open.spotify.com/artist/3Rq3YOF9YG9YfCWD4D56RZ', #Nujabes
        'https://open.spotify.com/artist/5dfZ5uSmzR7VQK0udbAVpf', #Sơn Tùng-MTP
        'https://open.spotify.com/artist/23xqmJEN3oVxwzqtNIyR5m', #AnnenMayKantereit
        'https://open.spotify.com/artist/6LuN9FCkKOj5PcnpouEgny', #Khalid
        'https://open.spotify.com/artist/5snNHNlYT2UrtZo5HCJkiw', #Epik High
        'https://open.spotify.com/artist/4fxd5Ee7UefO4CUXgwJ7IP', #Giveon
        'https://open.spotify.com/artist/1HY2Jd0NmPuamShAr6KMms', #Lady Gaga
        'https://open.spotify.com/artist/2XtMx7EHHODQSeBzDCBec9', #Bùi Lan Hương
        'https://open.spotify.com/artist/5Z1CCuBsyhEHngq3U5IraY', #Westlife
        'https://open.spotify.com/artist/5Ib3D8UtLdYZjhVNWzwfoH', #Nguyên Hà
        'https://open.spotify.com/artist/1QAJqy2dA3ihHBFIHRphZj', #Cigarettes After Sex
        'https://open.spotify.com/artist/70NcAr4ZtA3FAqU16iQZSb', #dhruv
    ]
    result = []
    for i in artist_list:
        print(i)
        result.append(bs4_parser(i))
    # result.append(bs4_parser(artist_list[0]))
    csv_saver(result)
    # url = 'https://i.scdn.co/image/ab67616d00001e02c6b577e4c4a6d326354a89f7'
    # url = '{}'.format(url)           
    # with open("image.png", 'wb') as f:
    #     response = requests.get(url)
    #     f.write(response.content)
    # return

if __name__ == "__main__":
    main()