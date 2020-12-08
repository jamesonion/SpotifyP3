import os
import sys
import json
import requests
import PySimpleGUIQt as sg
import pandas as pd
import spotipy
import webbrowser
from spotipy.oauth2 import SpotifyClientCredentials

from queue import Queue

#ACCESSING THE SPOTIFY API#


#have to get a new spotify token before using this#
spotify_token = "BQBYkg8d4aut3Nr4pAWr2WBGLhuDP7NfDU688Fq4Q2q1NDAcQqlcz-dK4mzdcr-y1BU_SwyDpBZNdgI4PIZ9uhcE0IEr4kNvyJwFRAT4JrNmkejlSX3HI6053A8ZzKe3mDcKO8HhLsohB6g"
class songRec:

    def search_track(self, song_name):
        query = "https://api.spotify.com/v1/search?q=track%3A{}&type=track&offset=0&limit=20".format(
            song_name
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        #uri = songs[0]["uri"]
        return songs


    def search_track_and_artist(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?q=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        #uri = songs[0]["uri"]
        return songs

def findID2(_song, _artist):
    returnedSongs = songRec.search_track_and_artist("0f2a3b6474214d87b144419b7ac084cd", _song, _artist)
    return returnedSongs[0]["id"]


def findID(_song):
    returnedSongs = songRec.search_track("0f2a3b6474214d87b144419b7ac084cd", _song);
    if len(returnedSongs) > 1:
        return "input artist"
    else:
        return returnedSongs[0]["id"]

def findSample(_song):
     returnedSongs = songRec.search_track("0f2a3b6474214d87b144419b7ac084cd", _song);
     if len(returnedSongs) > 1:
        return "input artist"
     else:
        return returnedSongs[0]["id"]

def url(ID):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials("5d2c27886c8a4836844580b11c289dac","1372129a4a254c2a9642956dbe7b75f0"))
    track = spotify.track(ID)
    return track['preview_url']
    #track['album']['images'][0]['url']

#GUI IMPLEMENTATION#

layout = [[sg.Image(filename="Logo4.png", key="-IMAGE-")],
          [sg.Text("Song Suggestion Algorithm", key='-TITLE-', justification='left', background_color='NONE', auto_size_text=True, font=["Gotham Medium", 16])],
          [sg.Text("Add Songs you Enjoy One by One to Receive a Personalized Playlist", key='-SUBTITLE-', justification='center', background_color='NONE', auto_size_text=True)],
          [sg.Button('Like', visible=False), sg.Button('Play', visible=False), sg.Button('Next', visible=False)],
          [sg.InputText(default_text="Enter your song here", enable_events=True, do_not_clear=True, justification='center', size=(50,1), key='-SONG-'), sg.InputText(default_text="Enter artist name", enable_events=True, do_not_clear=True, justification='center', size=(50,1), key='-ARTIST-', visible=False)],
          [sg.Text(key='-OUTPUT-', background_color='NONE')],
          [sg.Button('Add Song', size=(25,1)), sg.Button('Add Artist', size=(25,1), visible=False), sg.Button('Submit', size=(25,1))],
          [sg.Checkbox("Tree Implementation", default=True, key='-Tree-', enable_events=True, background_color='NONE', visible=False), sg.Checkbox("Map Implementation", key='-Map-', enable_events=True, background_color='NONE')],
          [sg.Multiline(background_color='WHITE', default_text="Current Playlist:\n", key='-LIKED-')]]

window = sg.Window('Playlists to improve? Let’s find your groove.', layout, icon="Logo.ico", resizable=False, element_justification='center', background_image="backb.png", force_toplevel=True)

dschange = 0
idchange = 0
inputtedsongs = []
runtime = 0
songdata = Queue()
currentsong = ['Title','Artist',0,0,0,0]

output = open("LikedSongs.txt", "w")
output.write(str(idchange) + "\n")
output.write("Done\n")
output.close()
output2 = open("MorT.txt", "w")
output2.write(str(dschange) + "\n")
output2.write("tree\n")
output2.close()
dschange = 1
idchange = 1

def updateSongs():
    if os.path.isfile('suggestions.txt'):
        input = open('suggestions.txt')
        x = input.readline()
        global runtime
        if runtime != float(x):
            runtime = float(x)
            input.close()
            df = pd.read_csv('suggestions.txt', skiprows=1, names=['Title:','Artist:','Valence:','Danceability:','Energy:','Acousticness:'], delimiter="|")
            for index, row in df.iterrows():
                title = row[0]
                artist = row[1]
                valence = row[2]
                danceability = row[3]
                energy = row[4]
                acousticness = row[5]
                songdata.put([title,artist,valence,danceability,energy,acousticness])
            #window['-IMAGE-'].update(filename="")
            if window['-Map-'].get() == True:
                string = "map"
            else:
                string = "tree"
            window['-OUTPUT-'].update("Runtime using a " + string + " data structure: " + str(runtime) + " ms", visible=True)
            window['Like'].update(visible=True)
            window['Play'].update(visible=True)
            window['Next'].update(visible=True)
            global currentsong 
            currentsong = songdata.get()
            window['-TITLE-'].update(currentsong[0])
            window['-SUBTITLE-'].update(currentsong[1])
            songdata.put(currentsong)
        else:
            input.close()
    else:
        updateSongs()
        
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Add Song':
        song = values['-SONG-']
        try:
            songID = findID(song)
            if songID == "input artist":
                window['-SONG-'].update(visible=False)
                window['-ARTIST-'].update(visible=True)
                window['Add Artist'].update(visible=True)
                window['Add Song'].update(visible=False)
                window['-OUTPUT-'].update(visible=False)
            else:
                window['-OUTPUT-'].update('Song Added.', visible=True)
                window['-SONG-'].update(visible=True, value="Enter another song here")
                window['-ARTIST-'].update(visible=False, value="Enter artist name")
                window['-LIKED-'].update(value=song + " - " + artist + "\n", append=True)
                inputtedsongs.append(songID)    
        except:
            window['-OUTPUT-'].update('Song Not Found.')
    if event == 'Add Artist':
        try:
            song = values['-SONG-']
            artist = values['-ARTIST-']
            songID = findID2(song, artist)
            window['-OUTPUT-'].update('Song Added.')
            window['-SONG-'].update(visible=True, value="Enter another song here")
            window['-ARTIST-'].update(visible=False, value="Enter artist name")
            window['Add Artist'].update(visible=False)
            window['Add Song'].update(visible=True)
            window['-LIKED-'].update(value=song + " - " + artist + "\n", append=True)
            inputtedsongs.append(songID)
        except:
            window['-OUTPUT-'].update(visible=True, value='Song Not Found.')
            window['-SONG-'].update(visible=True, value="Enter another song here")
            window['-ARTIST-'].update(visible=False, value="Enter artist name")
            window['Add Artist'].update(visible=False)
            window['Add Song'].update(visible=True)
    if event == 'Submit':
        output = open("LikedSongs.txt", "w")
        output.write(str(idchange) + "\n")
        idchange += 1
        for x in inputtedsongs:
            output.write(x + "\n")
        output.write("Done\n")
        output.close()
        temp = open('test.txt', "w")
        temp.close()
        updateSongs()
        os.remove("test.txt")

    if event == '-Map-':
        output2 = open("MorT.txt", "w")
        output2.write(str(dschange) + "\n")
        if window['-Map-'].Get() == True:
            window['-Tree-'].update(value=False)
            output2.write("map\n")
        else:
            window['-Tree-'].update(value=True)
            output2.write("tree\n")
        dschange += 1
        output2.close()
    if event == 'Play':
        url = url(str(findID2(currentsong[0],currentsong[1])))
        webbrowser.open(url)
    if event == 'Next':
        currentsong = songdata.get()
        window['-TITLE-'].update(currentsong[0])
        window['-SUBTITLE-'].update(currentsong[1])
        songdata.put(currentsong)
    if event == 'Like':
        window['-LIKED-'].update(value=currentsong[0] + " - " + currentsong[1] + "\n", append=True)
        songID = findID2(currentsong[0],currentsong[1])
        inputtedsongs.append(songID)
        
window.close()