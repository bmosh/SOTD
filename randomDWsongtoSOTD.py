import spotipy
import creds
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

SPOTIPY_CLIENT_ID=creds.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET=creds.SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI=creds.SPOTIPY_REDIRECT_URI
user = '20mosherr'
scope = 'playlist-modify-public playlist-modify-private'


token = util.prompt_for_user_token(user, scope, SPOTIPY_CLIENT_ID, 
SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

sotd_uri = None
sp = None
playlists = None

if token:
    print("access token success")
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists('20mosherr')

else:
    print("try again, auth failure.")

while playlists:
        for i, playlist in enumerate(playlists['items']):

            if playlist['name'] == 'sotd':
                sotd_uri = playlist['uri']
                print(sotd_uri)

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

def createSOTDList(sotd_uri):
    if sotd_uri == None:
        sp.user_playlist_create(user, 'sotd')
        sotd_uri = sp._get_uri('playlist', 'sotd')
    
    rec = getRecs()
    songlist = recSongs(rec)
    for song_link in songlist:
        newuri = [song_link.split(":")[2]]
        sp.user_playlist_remove_all_occurrences_of_tracks(user, sotd_uri, newuri)
        sp.user_playlist_add_tracks(user, sotd_uri, newuri)
        print('song added!')

def getRecs():
    genres = {}
    lst = []
    genre_list = enumerate(sp.recommendation_genre_seeds()['genres'])

    for i, genre in genre_list:
        print (i+1, genre)
        genres[i] = genre
    
    selections = input("which genres do you select?")
    lst = selections.split(", ")

    final = []
    for j in lst:
        final.append(genres[int(j)])

    print(final)
    return final

def recSongs(recs):

    uri_list = []
    songs = sp.recommendations(seed_genres=recs, limit=5)
    
    for j in songs['tracks']:
        # print(j.keys())
        print(j['name'])
        print(j['id'])
        print(j['uri'])
        uri_list.append(j['uri'])

    return uri_list


# createSOTDList(sotd_uri)
sp.current_user_playlists()