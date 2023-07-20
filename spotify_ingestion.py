import requests
import base64
import datetime

client_id = "86d0905c767c4334b63a784fad23f81e"
client_secret = "68d217c270ef43fb906f4ad7aa0dd462"

#access token
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

# client_creds = f"{client_id}:{client_secret}"
# client_creds_b64 = base64.b64encode(client_creds.encode())

#spotify api information
playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
market = "US"
fields = "items(added_at,track.artists(name))"
limit = 1
offset = 0

token_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?market={market}&fields={fields}&limit={limit}&offset={offset}"
method = "GET"
token_data = {}
token_headers = {
    "Authorization": f'Bearer {access_token}'
}

req = requests.get(token_url, data=token_data, headers = token_headers)
token_response_data = req.json()

print (token_response_data)


"""credit and citation
    1. how to get bearer auth: https://stmorse.github.io/journal/spotify-api.html
    2. how to use requests library: https://medium.com/@lorelablaka/extract-data-using-spotify-api-889222835bf4
    3. 
"""



