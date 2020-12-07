import json
import requests
from PIL import Image

spotify_token = "BQCHsL2omf3m5pBWAtHv_K-EFb36BHDNZMl5qDVGrKLDBiRn09VB9SxEwnGbKY_vZvJj3-CCwYg3bIoCOxc7WyLuyhoocawsEPP79aAQnoRj_LCpVb-X1VpUshPZzOUrywexHX2AolOGWYdYp83WbSCNw3OTP_-Q0l8"
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

#returnedSongs = songRec.search_track("0f2a3b6474214d87b144419b7ac084cd", "I fall apart")
returnedSongs = songRec.search_track_and_artist("0f2a3b6474214d87b144419b7ac084cd", "I fall apart", "Post Malone")
for i in returnedSongs:
    print(i["external_urls"]) #urls for link to spotify
    print(i["preview_url"])#link to  a preview of the song
    print(i["id"]) #ids of songs
    #i["images"]
    #image = Image.open(i["images"])
    #image.show()#attempting to find album covers
    

