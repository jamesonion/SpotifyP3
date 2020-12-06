import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials("5d2c27886c8a4836844580b11c289dac", "1372129a4a254c2a9642956dbe7b75f0")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

import PySimpleGUIQt as sg

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
        output.write(song + "\n")
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

window.close()