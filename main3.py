import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_current_user_top_tracks():
    toptracks_response = sp.current_user_top_tracks(time_range="short_term"); print('.', end='')
    toptracks_info = toptracks_response["items"]
    #print(json.dumps(toptracks, indent=2))
    while toptracks_response["next"]:
        toptracks_response = sp.next(toptracks_response); print('.', end='')
        toptracks_info.extend(toptracks_response["items"])
    toptracks_info, artists = sp_clean_user_top_tracks(toptracks_info, True)
    return toptracks_info, artists
    #toptracks_str = json.dumps(toptracks, indent=2).replace("\n", "<br>\n").replace(" ", "&nbsp;")
    #return toptracks_str
def sp_clean_user_top_tracks(tracks, clean= True):
    artists={}
    trackInd = 0
    for tr in tracks:
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
            getArtistInfo(artists, tracks[trackInd]["artists"][artInd]["uri"],clean)
            artInd +=1
        trackInd +=1
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
    artist = sp.artist(artist_id); print('.', end='')
    if clean:
        del artist["external_urls"]
        del artist["followers"]["href"]
        del artist["id"]
        del artist["images"]
    #print("xartist:",artist)
    return artist

SCOPE = 'user-library-read,playlist-read-private,user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8d7cb1e90e734ddfa3f10120ecc5ecd6",
                                               client_secret="793a2b51873f4ccfa917efff8130f980",
                                               redirect_uri="http://localhost:8501/",
                                               scope=SCOPE))
print("Progress:", sep='',end='')
playlists_info, artists_info1=get_playlists()
toptracks_info, artists_info2=get_current_user_top_tracks()
artists_info1.update(artists_info2)

playlist_str = json.dumps(playlists_info, indent=2)
toptracks_str = json.dumps(toptracks_info, indent=2)
artistsInfo_str = json.dumps(artists_info1, indent=2)

print("Playlists:")
print(playlist_str)
print("\r\n\r\n\r\nTop Tracks:")
print(toptracks_str)
print("\r\n\r\n\r\nArtists:")
print(artistsInfo_str)

