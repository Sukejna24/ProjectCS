import os

import flask
import json
from flask import Flask, request, redirect, session, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
first = True
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '8d7cb1e90e734ddfa3f10120ecc5ecd6'
client_secret = '793a2b51873f4ccfa917efff8130f980'
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private,user-top-read'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

@app.route('/') # root web app in flask
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_cutt'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    #return redirect(url_for('get_current_user_top_tracks'))
    return redirect(url_for('get_playlists'))

@app.route('/get_cutt')
def get_current_user_top_tracks():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    toptracks_response = sp.current_user_top_tracks(time_range="short_term")
    toptracks = toptracks_response["items"]
    #print(json.dumps(toptracks, indent=2))
    while toptracks_response["next"]:
        toptracks_response = sp.next(toptracks_response)
        toptracks.extend(toptracks_response["items"])
    toptracks, artists = sp_clean_user_top_tracks(toptracks, True)
    toptracks_str = json.dumps(toptracks, indent=2).replace("\n", "<br>\n").replace(" ", "&nbsp;")
    return toptracks_str
def sp_clean_user_top_tracks(tracks, clean= True):
    global first
    artists={}
    trackInd = 0
    for tr in tracks:
        if first:
            #print ("tr:", json.dumps(tr,indent=2))
            first=False
        if clean:
            del tracks[trackInd]["available_markets"] 
            del tracks[trackInd]["external_ids"]
            del tracks[trackInd]["external_urls"]
            del tracks[trackInd]["href"]
            del tracks[trackInd]["id"]
            del tracks[trackInd]["preview_url"]
            del tracks[trackInd]["album"]["available_markets"] # del tr["album"]["available_markets"]
            del tracks[trackInd]["album"]["images"] # del tr["album"]["images"]
            del tracks[trackInd]["album"]["external_urls"] # del tr["album"]["external_urls"]
            del tracks[trackInd]["album"]["href"] # del tr["album"]["href"]
            del tracks[trackInd]["album"]["uri"] # del tr["album"]["uri"]
            del tracks[trackInd]["album"]["type"] # del tr["album"]["type"]
            del tracks[trackInd]["album"]["id"] # del tr["album"]["id"]   
        artInd = 0 
        for artist in tr["album"]["artists"]:
            del tracks[trackInd]["album"]["artists"][artInd]["external_urls"]
            del tracks[trackInd]["album"]["artists"][artInd]["href"]
            del tracks[trackInd]["album"]["artists"][artInd]["id"]
            artInd +=1
        artInd = 0 
        for artist in tr["artists"]:
            del tracks[trackInd]["artists"][artInd]["external_urls"]
            del tracks[trackInd]["artists"][artInd]["href"]
            del tracks[trackInd]["artists"][artInd]["id"]
            getArtistInfo(artists, tracks[trackInd]["artists"][artistInd]["uri"],clean)
            artInd +=1
        trackInd +=1      
    return tracks, artists
@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    #toptracks = sp.current_user_top_tracks()
    #toptracks_str = json.dumps(toptracks, indent=2).replace("\n", "<br>\n").replace(" ", "&nbsp;")

    playlists = sp.current_user_playlists()
    playlists_info=[]
    for pl in playlists['items']:
        plinfo, artistsInfo = get_playlist(pl['id'], True)
        playlists_info.append((pl['name'], pl['external_urls']['spotify'], plinfo, artistsInfo))
    playlist_str = json.dumps(playlists_info, indent=2).replace("\n", "<br>\n").replace(" ", "&nbsp;")

    return playlist_str + "<br><br><br>\r\n\r\n\r\nTOPTRACKS:\r\n<br>" # + toptracks_str
def get_playlist(pl_id, clean=True):
    playlist_html = "pl_id:" + pl_id + "\r\n"
    pl = sp.playlist(pl_id, fields="name,id,items(track)")
    tracks,artists = get_all_tracks_from_playlist(pl_id, clean)
    return tracks, artists
def get_all_tracks_from_playlist(playlist_id, clean=True):
    tracks_response = sp.playlist_tracks(playlist_id)
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response["items"])
    tracks, artists = sp_clean_tracks(tracks)
    return tracks, artists
def sp_clean_tracks(tracks,clean=True):
    trackInd=0
    artists={}
    # print("tracks:", tracks,"\r\n\r\n\r\n")
    First = True
    for track in tracks:
        tr = track["track"]
        # print("track:", track, "\r\n\r\n\r\n")
        if clean: 
            del tracks[trackInd]["added_by"]["external_urls"]  # del tr["added_by"]
            del tracks[trackInd]["added_by"]["id"]
            del tracks[trackInd]["track"]["preview_url"]  # del tr["preview_url"]
            del tracks[trackInd]["track"]["episode"]  #del tr["episode"]
            del tracks[trackInd]["track"]["available_markets"]  #del tr["available_markets"]
            del tracks[trackInd]["track"]["explicit"]  #del tr["explicit"]
            del tracks[trackInd]["track"]["type"]  #del tr["type"]
            del tracks[trackInd]["track"]["external_ids"]  #del tr["external_ids"]
            del tracks[trackInd]["track"]["external_urls"]  #del tr["external_urls"]
            del tracks[trackInd]["track"]["href"]  #del tr["href"]
            del tracks[trackInd]["track"]["uri"]  #del tr["uri"]
            del tracks[trackInd]["track"]["album"]["available_markets"] # del tr["album"]["available_markets"]
            del tracks[trackInd]["track"]["album"]["images"] # del tr["album"]["images"]
            del tracks[trackInd]["track"]["album"]["external_urls"] # del tr["album"]["external_urls"]
            del tracks[trackInd]["track"]["album"]["href"] # del tr["album"]["href"]
            del tracks[trackInd]["track"]["album"]["uri"] # del tr["album"]["uri"]
            del tracks[trackInd]["track"]["album"]["type"] # del tr["album"]["type"]
            del tracks[trackInd]["track"]["album"]["id"] # del tr["album"]["id"]
        artistInd=0
        for artist in tr["album"]["artists"]:
            if clean:
                del tracks[trackInd]["track"]["album"]["artists"][artistInd]["id"]            #del artist["id"]
                del tracks[trackInd]["track"]["album"]["artists"][artistInd]["external_urls"] #del artist["external_urls"]
                del tracks[trackInd]["track"]["album"]["artists"][artistInd]["href"]          #del artist["href"]
                # del tracks[trackInd]["track"]["album"]["artists"][artistInd]["uri"]           #del artist["uri"]
            artistInd+=1
        artistInd=0
        for artist in tr["artists"]:
            if clean:
                del tracks[trackInd]["track"]["artists"][artistInd]["id"]             #del artist["id"]
                del tracks[trackInd]["track"]["artists"][artistInd]["external_urls"]  #del artist["external_urls"]
                del tracks[trackInd]["track"]["artists"][artistInd]["href"]           #del artist["href"]
                # del tracks[trackInd]["track"]["artists"][artistInd]["uri"]            #del artist["uri"]
            getArtistInfo(artists, tracks[trackInd]["track"]["artists"][artistInd]["uri"],clean)
            artistInd += 1
        trackInd += 1
    return tracks, artists
def getArtistInfo(artists, artist_uri, clean=True):
    if artist_uri not in artists:
        artists[artist_uri]=spArtistInfo(artist_uri,clean)
def spArtistInfo(artist_id, clean=True): #artist: {'followers': {'total': nb}, 
                                         #         'genres': [], 
                                         #         'href':'https://api.spotify.com/v1/artists/id', 
                                         #         'name': '', 
                                         #         'popularity': nb, 
                                         #         'type': 'artist', 
                                         #         'uri': 'spotify:artist:id'}
    artist = sp.artist(artist_id)
    if clean:
        del artist["external_urls"]
        del artist["followers"]["href"]
        del artist["id"]
        del artist["images"]
    #print("xartist:",artist)
    return artist
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
