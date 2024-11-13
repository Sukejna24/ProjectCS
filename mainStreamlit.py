# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 12:35:20 2024

@author: Anne-Sophie Meier
"""
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
# Geheimnis (besser wäre in Verzeichnis .streamlit Datei secrets.toml
# Beispiel:
# SPOTIPY_CLIENT_ID = '8d7cb1e90e734ddfa3f10120ecc5ecd6'
# SPOTIPY_CLIENT_SECRET = '793a2b51873f4ccfa917efff8130f980'
# SPOTIPY_REDIRECT_URI = 'http://localhost:8501/'
client_id="8d7cb1e90e734ddfa3f10120ecc5ecd6"
client_secret="793a2b51873f4ccfa917efff8130f980"
redirect_uri="http://localhost:8501/"
scope='user-library-read,playlist-read-private,user-top-read'

debug = True
# spotify/streamlit login
def get_token(oauth, code):
    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    if debug: print("get_token token:", token[0:10])
    return token

def sign_on(token):
    sp = spotipy.Spotify(auth=token)
    if debug: print("Sign on!")
    return sp

def app_get_token():
    try:
        # test
        if st.session_state["oauth"] == None:
            # besser ware die Parameter von .streamlit/screts.toml
            # cid = st.secrets["SPOTIPY_CLIENT_ID"]
            # csecret = st.secrets["SPOTIPY_CLIENT_SECRET"]
            # uri = st.secrets["SPOTIPY_REDIRECT_URI"]
            cid=client_id
            csecret=client_secret
            uri=redirect_uri
            scopes = scope # Rechte
            oauth = SpotifyOAuth(scope=scopes,
                                 redirect_uri=uri,
                                 client_id=cid,
                                 client_secret=csecret)
            st.session_state["oauth"] = oauth
        # end test
        if debug: print("app_get_token: oauth:", st.session_state["oauth"], "code:", st.session_state["code"][0:10])
        token = get_token(st.session_state["oauth"], st.session_state["code"])
    except Exception as e:
        st.error("Fehler während Token-Abfrage!")
        st.write("Fehler:")
        st.write(e)
    else:
        if debug: print("app_get_token: setze Token in session_state['cached_token']", st.session_state['cached_token'])
        st.session_state["cached_token"] = token

def app_sign_in():
    try:
        sp = sign_on(st.session_state["cached_token"])
    except Exception as e:
        st.error("Fehler in sign-in!")
        st.write("Fehler:")
        st.write(e)
    else:
        st.session_state["signed_in"] = True
        willkomens_mldg()
        st.success("Sign-in erfolgreich!")
    return sp

def willkomens_mldg():
    # vom Spotify Dashboard für dieses Projekt
    # besser ware die Parameter von .streamlit/screts.toml
    # cid = st.secrets["SPOTIPY_CLIENT_ID"]
    # csecret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    # uri = st.secrets["SPOTIPY_REDIRECT_URI"]
    cid = client_id
    csecret = client_secret
    uri = redirect_uri
    scopes = scope  # Rechte
    # Authentifizierung
    oauth = SpotifyOAuth(scope=scopes,
                         redirect_uri=uri,
                         client_id=cid,
                         client_secret=csecret)
    st.session_state["oauth"] = oauth

    # Authorizierungs URL von Spotify
    auth_url = oauth.get_authorize_url()

    # öffnet im selben Browserfenster über Redirects den Link
    redirect_link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Melde dich mit dem untenstehenden Link an:"
    )
    # define welcome
    willkommen = """
    Diese Applikation erlaubt das Konsolidieren von Playlists.
    """
    st.title("Konsolidierung von Spotify Playlist")

    if not st.session_state["signed_in"]:
        st.markdown(willkommen)
        st.write(" ".join(["Kein Token gefunden",
                           "Folge dem Link."]))
        st.markdown(redirect_link_html, unsafe_allow_html=True)
# end spotify/streamlite login

# get current user top tracks
def get_current_user_top_tracks():
    toptracks_response = sp.current_user_top_tracks(time_range="short_term"); print('.', end='')
    toptracks_info = toptracks_response["items"]
    # if debug: print(json.dumps(toptracks, indent=2))
    while toptracks_response["next"]:
        toptracks_response = sp.next(toptracks_response); print('.', end='')
        toptracks_info.extend(toptracks_response["items"])
    toptracks_info, artists = sp_clean_user_top_tracks(toptracks_info, True)
    return toptracks_info, artists

def sp_clean_user_top_tracks(tracks, clean= True):
    artists={}
    for trackInd, tr in enumerate(tracks):
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
        for artInd, artist in enumerate(tr["album"]["artists"]):
            del tracks[trackInd]["album"]["artists"][artInd]["external_urls"]
            del tracks[trackInd]["album"]["artists"][artInd]["href"]
            del tracks[trackInd]["album"]["artists"][artInd]["id"]
        for artInd, artist in enumerate(tr["artists"]):
            del tracks[trackInd]["artists"][artInd]["external_urls"]
            del tracks[trackInd]["artists"][artInd]["href"]
            del tracks[trackInd]["artists"][artInd]["id"]
            getArtistInfo(artists, tracks[trackInd]["artists"][artInd]["uri"],clean)
    return tracks, artists
def get_playlists():
    playlists = sp.current_user_playlists(); print('.', end='')
    playlists_info=[]
    for pl in playlists['items']:
        plinfo, artists_info = get_playlist(pl['id'], True)
        playlists_info.append((pl['name'], pl['external_urls']['spotify'], plinfo, artists_info))
    return playlists_info, artists_info
    # playlist_str = json.dumps(playlists_info, indent=2).replace("\n", "<br>\n").replace(" ", "&nbsp;")
    # artistsInfo_str = json.dumps(artists_info, indent=2).replace("\n", "<br>\n").replace(" ", "&nbsp;")
    # return playlist_str + "<br><br><br>\r\n\r\n\r\nTOPTRACKS:\r\n<br>"+artistsInfo_str+"\r\n<br>" # + toptracks_str

def get_playlist(pl_id, clean=True):
    playlist_html = "pl_id:" + pl_id + "\r\n"
    pl = sp.playlist(pl_id, fields="name,id,items(track)"); print('.', end='')
    tracks,artists = get_all_tracks_from_playlist(pl_id, clean)
    return tracks, artists
def get_all_tracks_from_playlist(playlist_id, clean=True):
    tracks_response = sp.playlist_tracks(playlist_id); print('.', end='')
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response); print('.', end='')
        tracks.extend(tracks_response["items"])
    tracks, artists = sp_clean_tracks(tracks)
    return tracks, artists
def sp_clean_tracks(tracks,clean=True):
    artists={}
    # print("tracks:", tracks,"\r\n\r\n\r\n")
    for trackInd, track in enumerate(tracks):
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
        for artistInd, artist in enumerate(tr["album"]["artists"]):
            if clean:
                del tracks[trackInd]["track"]["album"]["artists"][artistInd]["id"]            #del artist["id"]
                del tracks[trackInd]["track"]["album"]["artists"][artistInd]["external_urls"] #del artist["external_urls"]
                del tracks[trackInd]["track"]["album"]["artists"][artistInd]["href"]          #del artist["href"]
                # del tracks[trackInd]["track"]["album"]["artists"][artistInd]["uri"]           #del artist["uri"]
        for artistInd, artist in enumerate(tr["artists"]):
            if clean:
                del tracks[trackInd]["track"]["artists"][artistInd]["id"]             #del artist["id"]
                del tracks[trackInd]["track"]["artists"][artistInd]["external_urls"]  #del artist["external_urls"]
                del tracks[trackInd]["track"]["artists"][artistInd]["href"]           #del artist["href"]
                # del tracks[trackInd]["track"]["artists"][artistInd]["uri"]            #del artist["uri"]
            getArtistInfo(artists, tracks[trackInd]["track"]["artists"][artistInd]["uri"],clean)
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
    artist = sp.artist(artist_id); print('.', end='')
    if clean:
        del artist["external_urls"]
        del artist["followers"]["href"]
        del artist["id"]
        del artist["images"]
    #print("xartist:",artist)
    return artist
# Hauptprogramm
if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
    print("st.session_state['signed_in'] = False")
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = ""
    print('st.session_state["cached_token"] = ""')
if "code" not in st.session_state:
    st.session_state["code"] = ""
    print('st.session_state["code"] = ""')
if "oauth" not in st.session_state:
    st.session_state["oauth"] = None
    print('st.session_state["oauth"] = None')
url_params = st.query_params
if st.session_state["cached_token"] != "":
    st.write("Cached token != '', hence app_sign_in")
    if debug: print("Cached token != '', hence app_sign_in")
    sp = app_sign_in()
elif "code" in url_params: # hole den code für die Spotify Session
    st.session_state["code"] = url_params["code"] # [0] this takes only the frist letter. url_params["code"][0] changed
    if debug: print("get code from url_params into session_state['code']:", st.session_state["code"][0:10])
    app_get_token()
    sp = app_sign_in()
# otherwise, prompt for redirect
else:
    if debug: print("Willkommen-Meldung!")
    willkomens_mldg()
# hier beginnt jetzt das wirkliche Programm
### is there another way to do this? clunky to have everything in an if:
if st.session_state["signed_in"]:
    if debug: print("Hauptprogramm beginnt: sp.current_user(), session_state:", st.session_state['cached_token'][0:10])
    user = sp.current_user()
    if debug: print("passed sp.current_user()")
    name = user["display_name"]
    username = user["id"]
    st.markdown("Hallo {user}! Hier sind die Playlists, Top Tracks und Künstler:".format(user=name))

    # SCOPE = 'user-library-read,playlist-read-private,user-top-read'
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8d7cb1e90e734ddfa3f10120ecc5ecd6",
    #                                               client_secret="793a2b51873f4ccfa917efff8130f980",
    #                                               redirect_uri="http://localhost:8501/",
    #                                               scope=SCOPE))
    if debug: print("Progress:", sep='',end='')

    if debug: print("\r\nPlaylists started!")
    st.text("Jetzt werden Playlists, Top Tracks und alle Künstler zu diesen geladen. Etwas Geduld ...")
    st.subheader("Playlists:")
    #important keep get_playlists
    playlists_info, artists_info1=get_playlists() 
    playlist_str = json.dumps(playlists_info, indent=2)
    st.code(playlist_str, language="json", line_numbers=True)


    if debug: print("\r\nTop Tracks started!")
    st.subheader("\r\nTop Tracks:")
    #important keep get_current_user_top_tracks
    toptracks_info, artists_info2=get_current_user_top_tracks()
    toptracks_str = json.dumps(toptracks_info, indent=2)
    st.code(toptracks_str, language="json", line_numbers=True)

    if debug: print("\r\nKünstler started!")
    st.subheader("Künstler:")
    artists_info1.update(artists_info2)
    artistsInfo_str = json.dumps(artists_info1, indent=2)
    st.code(artistsInfo_str, language="json", line_numbers=True)

    if debug: print("\r\nFertig!")
    st.write("Fertig!")
