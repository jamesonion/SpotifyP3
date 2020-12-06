import json
import requests

spotify_token = "BQCzntyVB7RRFhJbYwqvtPx2nAdBWDYXu8VsWgmMBQoSgzwA7xQFveJit_qbY6Km3mVFT4VOH9DhFdYMKW3qH27sEhB6eX94OFKRnsxGfWZ2u8JClwytG4KFZyuUQlfsWun6vJ3Bvc6HE2LrubYpsKw4Pv-IY4L7dDU"
class songRec:

    def search_track(self, song_name):
        query = "https://api.spotify.com/v1/search?q=track%3A{}&type=track&offset=0&limit=20".format(
            song_name
        )
        #query = "https://api.spotify.com/v1/search?q=tania%20bowra&type=artist"
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
        #query = "https://api.spotify.com/v1/search?q=tania%20bowra&type=artist"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        uri = songs[0]["uri"]
        return uri

returnedSongs = songRec.search_track("0f2a3b6474214d87b144419b7ac084cd", "Sugar Wraith")
for i in returnedSongs:
    print(i["uri"])

