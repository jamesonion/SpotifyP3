import json
import requests
import PySimpleGUIQt as sg

#have to get a new spotify token before using this
spotify_token = "BQDhJTSJ8nq7tBVg2Jxac7EvTlffeFTaD1T72mpydHqnWqrl4CDoSmC-KKl2Sr-u43mMo4x5IlfoZDg2n8lDoq09TPW9UkHJpkEbXS3W7TXNj-LbOFT-3ZxvdDvZn6QD2LOyrPJRRFcuei20ia-BrDbyTFU2Ngq-usM"
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
          [sg.InputText(default_text="Enter your song here", enable_events=True, do_not_clear=True, justification='center', size=(50,1), key='-INPUT-')],
          [sg.Listbox(values = ["Artists"], visible=False, key='-ARTISTS-', enable_events=True, bind_return_key=True)],
          [sg.Text(size=(25,1), key='-OUTPUT-', justification='center')],
          [sg.Checkbox("Tree Implementation", default=True, key='-Tree-', enable_events=True), sg.Checkbox("Map Implementation", key='-Map-', enable_events=True)],
          [sg.Button('Add Song', size=(25,1)), sg.Button('Submit', size=(25,1))]]

window = sg.Window('Playlists to improve? Let’s find your groove.', layout, size=(540,960), icon="Logo.ico", resizable=True, element_justification='center', background_image="backb.png")

inputtedsongs = []
input = open("input.txt", "r")

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Add Song':
        song = values['-INPUT-']
        output = open("output.txt", "w")

        #ethan added
        songID = findID(song)
        if songID == "input artist":
            #FIXME prompt the user to input an artist
            artist = values['-INPUT-']
            songID = findID2(song, artist)

        output.write(songID + "\n")
        output.close()
        result = input.readline()
        if result == "Success.\n":
            lines = input.readlines()
            window['-ARTISTS-'].update(visible=True, values=lines)
            event2, values2 = window.read()
            if event2 == '-ARTISTS-':
                artist = window['-ARTISTS-'].get()
                inputtedsongs.append(song + ", " + artist[0])
                window['-OUTPUT-'].update('Song Added.')
        else:
            window['-OUTPUT-'].update('Song Does Not Exist. Try Again.')
    if event == 'Submit':
        input.close()
        output = open("output.txt", "a")
        if window['-Map-'].Get() == True:
            output.write("Map\n")
        else:
            output.write("Tree\n")
        for x in inputtedsongs:
            output.write(x)
        output.close()
    # if its a map, must write map to the MorT.txt file, if its a tree write tree
    # first line of MorT.txt will be an int that gets incremented when the mode is changed
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