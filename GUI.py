import json
import requests
import PySimpleGUIQt as sg

#have to get a new spotify token before using this
spotify_token = "BQC-Vn0CIB-3JhhvIqpBusZ2PwmA9O4-6JGfHr74PdeQryS2hbYLIQ2vNnYdq9AES5hwVYdJLliK-bbBLmYqI6jP3kWOKoQlSdwGzi0uMHkkAaBo0b0FQsnHqMZ0fRTBhwJFIJH25AbspP8"
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



returnedSongs = songRec.search_track("0f2a3b6474214d87b144419b7ac084cd", "Feeling Whitney")
for i in returnedSongs:
    print(i["id"])


layout = [[sg.Image(filename="Logo4.png")],
          [sg.Text("Song Suggestion Algorithm", justification='center', size=(25,1))],
          [sg.Text("Add Songs you Enjoy One by One to Receive a Personalized Playlist", justification='center', size=(50,1))],
          [sg.InputText(default_text="Enter your song here", enable_events=True, do_not_clear=True, justification='center', size=(50,1), key='-SONG-'), sg.InputText(default_text="Enter the artist's name here", enable_events=True, do_not_clear=True, justification='center', size=(50,1), key='-ARTIST-', visible=False)],
          #[sg.Listbox(values = ["Artists"], visible=False, key='-ARTISTS-', enable_events=True, bind_return_key=True)],
          [sg.Text(size=(25,1), key='-OUTPUT-', justification='center')],
          [sg.Checkbox("Tree Implementation", default=True, key='-Tree-', enable_events=True), sg.Checkbox("Map Implementation", key='-Map-', enable_events=True)],
          [sg.Button('Add Song', size=(25,1)), sg.Button('Submit', size=(25,1))]]

window = sg.Window('Playlists to improve? Let’s find your groove.', layout, size=(540,960), icon="Logo.ico", resizable=True, element_justification='center', background_image="backb.png")

inputtedsongs = []
#input = open("input.txt", "r")
dschanged = 0

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Add Song':
        song = values['-SONG-']
        output = open("output.txt", "w")

        #ethan added
        songID = findID(song)
        if songID == "input artist":
            window['-SONG-'].update(visible=False)
            window['-ARTIST-'].update(visible=True)
            event2, values2 = window.read()
            if event2 == 'Add Song':
                artist = values2['-SONG-']
                songID = findID2(song, artist)
                window['-OUTPUT-'].update('Song Added.')
                window['-SONG-'].update(visible=True)
                window['-ARTIST-'].update(visible=False)
        output.write(songID + "\n")
        output.close()      
    if event == 'Submit':
        dschanged += 1
        output2 = open("MorT.txt", "w")
        output2.write(str(dschanged) + "\n")
        if window['-Map-'].Get() == True:
            output2.write("map\n")
        else:
            output2.write("tree\n")
        output2.close()
    if event == '-Map-':
        if window['-Map-'].Get() == True:
            window['-Tree-'].update(value=False)
        else:
            window['-Tree-'].update(value=True)
    if event == '-Tree-':
        if window['-Tree-'].Get() == True:
            window['-Map-'].update(value=False)
        else:
            window['-Map-'].update(value=True)

   # window['-OUTPUT-'].update('Finding songs similar to: ' + values['-INPUT-'])
   # after writing the IDs of all of the songs inputted, after submit must then read in from the suggested songs text file and display the suggested song along with the visual representation of the 4 elements
   # suggestions.txt is formatted as a csv file with the first thing being the song name, the second being the artist, then the following 4 being valence, then danceability, then energy, then acousticness
   # the first line of suggestions will be a number which corresponds to the runtime for the map or tree implementation, the number is in milliseconds

window.close()