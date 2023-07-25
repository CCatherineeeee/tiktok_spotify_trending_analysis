import requests
import pandas as pd
import datetime



def request_bearer_token(client_id, client_secret):
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']
    return access_token

class Spotify_Ingestion:
    def __init__(self, playlist_id, market, fields, limit, offset, access_token):
        self.playlist_id = playlist_id
        self.market = market
        self.fields = fields
        self.limit = limit
        self.offset = offset
        self.access_token = access_token
        self.added_at = []
        self.artist = []
        self.song_id = []
        self.song_name = []
        self.song_dict = {}
        self.song_df = None
        
    def spotify_data_ingestion(self):
        token_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?market={self.market}&fields={self.fields}&limit={self.limit}&offset={self.offset}"
        # method = "GET"
        token_data = {}
        token_headers = {
            "Authorization": f'Bearer {self.access_token}'
        }

        req = requests.get(token_url, data=token_data, headers = token_headers)
        token_response_data = req.json()

        
        for songs in token_response_data['items']:
            self.added_at.append(songs['added_at'])
            
            artists = ""
            if len(songs['track']['artists']) > 1:
                for track_artists in range(len(songs['track']['artists'])-1):
                    artists += (songs['track']['artists'][track_artists]['name'])
                    artists += ", "
                artists += (songs['track']['artists'][-1]['name'])
            else:
                artists = (songs['track']['artists'][0]['name'])
            
            self.artist.append(artists)
            self.song_id.append(songs['track']['id'])
            self.song_name.append(songs['track']['name'])
        
        self.song_dict = {
            "song_id": self.song_id,
            "added_at": self.added_at,
            "artist": self.artist,
            "song_name": self.song_name
        }
        
    def convert_dictionary_to_dataframe(self):
        self.song_df = pd.DataFrame(self.song_dict, columns = ["song_id", "added_at", "artist", "song_name"])
    
    def quality_check(self):
        if self.song_df.empty == True:
            raise Exception("Error - No Song Extracted")
        if pd.Series(self.song_df['song_id']).is_unique:
            pass
        else:
            #The Reason for using exception is to immediately terminate the program and avoid further processing
            raise Exception("Primary Key Exception,Data Might Contain duplicates")
        if self.song_df.isnull().values.any():
            raise Exception("Null values found")
        return self.song_df

    
        
    

def main():
    client_id = "86d0905c767c4334b63a784fad23f81e"
    client_secret = "68d217c270ef43fb906f4ad7aa0dd462"  
    access_token = request_bearer_token(client_id, client_secret)
    market = "US"
    fields = "items(added_at,track.artists(name), track.name, track.id)"
    limit = 2
    offset = 0
    spotify_trending = Spotify_Ingestion("37i9dQZEVXbLRQDuF5jeBp", market, fields, limit, offset, access_token)
    spotify_trending.spotify_data_ingestion()
    spotify_trending.convert_dictionary_to_dataframe()
    spotify_trending_df = spotify_trending.quality_check()
    billboard_hot_100 = Spotify_Ingestion("6UeSakyzhiEt4NB3UAd6NQ", market, fields, limit, offset, access_token)
    billboard_hot_100.spotify_data_ingestion()
    billboard_hot_100.convert_dictionary_to_dataframe()
    billboard_hot_100_df = billboard_hot_100.quality_check()
    return (spotify_trending_df, billboard_hot_100_df)
    






"""credit and citation
    1. how to get bearer auth: https://stmorse.github.io/journal/spotify-api.html
    2. how to use requests library: https://medium.com/@lorelablaka/extract-data-using-spotify-api-889222835bf4
    3. quality check: https://blog.devgenius.io/data-engineering-project-2-building-spotify-etl-using-python-and-airflow-432dd8e4ffa3
"""



