# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 08:35:20 2024

@author: Anne-Sophie Meier
"""

# MYSQL API FOR usr, playlists(), album, artists
import mysql.connector
import json

debug=True
def connect(): # Connect to the database "data", password should not be in code in production version
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL@2019",
        database="data"
    )
    return mydb
#######
# usr
def userExists(mydb, user): # check if unique
    str="select count(*) cnt from usr where user_uri='{uri}';".format(uri=user["uri"])
    cur = mydb.cursor()
    cur.execute(str)
    myres = cur.fetchall()
    if myres[0][0]==1: # cnt is 1 ==> user found
        if debug: print("userExists:", myres[0][0])
        return True
    if debug: print("userExists:", myres[0][0])
    return False # user not found
def addUser(mydb, user):
    sql="INSERT INTO `usr` (`user_uri`, `email`, `display_name`, `followers`, `country`) VALUES (%s, %s, %s, %s, %s)"
    if "email" in user:
        val = (user["uri"], user["email"], user["display_name"], user["followers"]["total"], user["country"])
    else:
        val = (user["uri"], '', user["display_name"], user["followers"]["total"], '')
    # Felder: https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    if debug: print("addUser: insert into usr:", val)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit() # send
    if debug: print(mycursor.rowcount, "addUser: record inserted.")
    return None
def getUser(mydb, user_uri):
    sql = "SELECT `user_uri`, `email`, `display_name`, `followers`, `country` FROM `usr` WHERE user_uri=%s"
    val = (user_uri, )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    return user
########
# plylst
def playlistExists(mydb, playlist): # check if unique
    if debug: print("playlistExists: uri:", playlist["uri"])
    str = "select count(*) cnt from plylst where playlist_uri='{uri}';".format(uri=playlist["uri"])
    cur = mydb.cursor()
    cur.execute(str)
    myres = cur.fetchall()
    if myres[0][0] == 1:  # cnt is 1 ==> user found
        if debug: print("playlistExists:", myres[0][0])
        return True
    if debug: print("playlistExists:", myres[0][0])
    return False  # user not found

def addPlaylist(mydb, playlist):
    if debug: print("addPlaylist:", playlist)
    sql = "INSERT INTO `plylst` (`playlist_uri`, `name`, `description`, `owner_uri`, `owner_display_name`, `collaborative`, `public`, `tracks_total`, `type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (playlist["uri"],
           playlist["name"],
           playlist["description"],
           playlist["owner"]["uri"],
           playlist["owner"]["display_name"],
           playlist["collaborative"],
           playlist["public"],
           playlist["tracks"]["total"],
           playlist["type"])
    # Felder: https://developer.spotify.com/documentation/web-api/reference/get-playlist
    if debug: print("addPlaylist: insert into plylst:", val)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()  # send
    if debug: print(mycursor.rowcount, "addPlaylist: record inserted.")
    return playlist["uri"]

def getPlaylist(mydb, playlist_uri):
    playlist = {}
    sql = "SELECT `playlist_uri`, `name`, `description`, `owner_uri`, `owner_display_name`, `collaborative`, `public`, `tracks_total`, `type` FROM `plylst` WHERE playlist_uri = %s"
    val = (playlist_uri, )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, val)
    playlist = mycursor.fetchone()
    return playlist
########
# trck
def trackExists(mydb, track):  # check if unique
    if debug: print("trackExists:", track["track"]["uri"])
    str="select count(*) cnt from trck where track_uri='{uri}';".format(uri=track["track"]["uri"])
    cur = mydb.cursor()
    cur.execute(str)
    myres = cur.fetchall()
    if myres[0][0] == 1:  # cnt is 1 ==> user found
        if debug: print("trackExists:", myres[0][0])
        return True
    if debug: print("trackExists:", myres[0][0])
    return False # user not found
def addTrack(mydb, track, playlist_uri):
    sql="INSERT INTO `trck`(`track_uri`, `playlist_uri`, `track`, `album_name`, `album_type`," \
        "`total_tracks`, `disc_number`, `track_number`, `duration_ms`, `release_date`, " \
        "`release_date_prescision`, `popularity`, `item_added_at`, `item_added_by_uri`, " \
        "`track_id`, `acousticness`, `danceability`, `energy`, `instrumentalness`, " \
        "`pitchKey`, `liveness`, `loudness`, `mode`, `speechiness`, " \
        "`tempo`, `valence`) VALUES " \
        "(%s, %s, %s, %s, %s," \
         "%s, %s, %s, %s, %s," \
         "%s, %s, %s, %s," \
         "%s, %s, %s, %s, %s," \
         "%s, %s, %s, %s, %s," \
         "%s, %s)"
    val = (track["track"]["uri"], playlist_uri, track["track"]["track"], track["track"]["album"]["name"], track["track"]["album"]["album_type"],
           track["track"]["album"]["total_tracks"], track["track"]["disc_number"], track["track"]["track_number"], track["track"]["duration_ms"], track["track"]["album"]["release_date"],
           track["track"]["album"]["release_date_precision"], track["track"]["popularity"], track["added_at"], track["added_by"]["uri"],
           track["track"]["id"], track["track"]["acousticness"], track["track"]["danceability"], track["track"]["energy"], track["track"]["instrumentalness"],
           track["track"]["key"], track["track"]["liveness"], track["track"]["loudness"], track["track"]["mode"], track["track"]["speechiness"],
           track["track"]["tempo"], track["track"]["valence"]
          )
    # Felder: https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    if debug: print("addTrack: insert into trck:", val)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit() # send
    if debug: print(mycursor.rowcount, "addTrack: record inserted.")
    return None
def getTrack(mydb, track_uri):
    if debug: print("getTrack:", track_uri)
    sql = "SELECT `track_uri`, `playlist_uri`, `track`, `album_name`, `album_type`, `total_tracks`, `disc_number`, `track_number`, " \
          "`duration_ms`, `release_date`, `release_date_prescision`, `popularity`, `item_added_at`, `item_added_by_uri`, " \
          "`track_id`, `acousticness`, `danceability`, `energy`, `instrumentalness`, `pitchKey`, `liveness`, `loudness`, `mode`, `speechiness`, " \
          "`tempo`, `valence` FROM `trck` WHERE track_uri= %s"
    val = (track_uri, )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, val)
    track = mycursor.fetchone()
    return track
########
# artst
def artistExists(mydb, artist_uri): # check if unique
    str="select count(*) cnt from artst where artist_uri='{uri}';".format(uri=artist_uri)
    cur = mydb.cursor()
    cur.execute(str)
    myres = cur.fetchall()
    if myres[0][0]==1: # cnt is 1 ==> artist found
        if debug: print("artistExists:", myres[0][0])
        return True
    if debug: print("artistExists:", myres[0][0])
    return False # user not found
def addArtist(mydb, artist):
    sql = "INSERT INTO `artst`(`artist_uri`, `name`, `popularity`, `followers`, `artist_type`) VALUES (%s, %s, %s, %s, %s)"
    val = (artist["uri"], artist["name"], artist["popularity"], artist["followers"]["total"], artist["type"])
    # Felder: https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    if debug: print("addArtist: insert into artst:", val)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit() # send
    if debug: print(mycursor.rowcount, "addArtist: record inserted.")
    for g in artist["genres"]:
        if not artistGenresExists(mydb, artist["uri"], g):
            addArtistGenre(mydb, artist["uri"], g)
    return None
def getArtist(mydb, artist_uri):
    sql = "SELECT `artist_uri`, `name`, `popularity`, `followers`, `artist_type` FROM `artst` WHERE artist_uri=%s"
    val = (artist_uri, )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, val)
    artist = mycursor.fetchone()
    genres = getArtistGenres(mydb, artist_uri)
    artist[genres]=list(genres.values())
    return artist
########
# gnrs
def artistGenresExists(mydb, artist_uri, genre): # check if unique
    if debug: print("artistGenresExists:", artist_uri, genre)
    str="select count(*) cnt from gnrs where artist_uri='{uri}' and genres_name='{genre}';".format(uri=artist_uri, genre=genre)
    cur = mydb.cursor()
    cur.execute(str)
    myres = cur.fetchall()
    if myres[0][0]==1: # cnt is 1 ==> user found
        if debug: print("artist genre exists:", myres[0][0])
        return True
    if debug: print("artist genre exists:", myres[0][0])
    return False # user not found
def addArtistGenre(mydb, artist_uri, genre):
    sql="INSERT INTO `gnrs`(`artist_uri`, `genres_name`) VALUES (%s, %s)"
    val = (artist_uri, genre)
    # Felder: https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    if debug: print("addArtistGenre: insert into gnrs:", val)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit() # send
    if debug: print(mycursor.rowcount, "addArtistGenre: record inserted.")
    return None
def getArtistGenres(mydb, artist_uri):
    sql = "SELECT `artist_uri`, `genres_name` FROM `gnrs` WHERE artist_uri=%s"
    val = (artist_uri)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, val)
    genres = mycursor.fetchall()
    return genres

########
# persistence layer: stores playlists, artists and toptracks in tables  plylst, trck, artists
def persist_playlists(mydb, playlists_info):
    if debug: print("persist_playlists:")
    for playlist in playlists_info: # is a tuple
        if debug: print("persist_playlists: playlist:", playlist[0]["uri"], "tracks:") #, playlist[1])
        if playlist != None:
            if not playlistExists(mydb, playlist[0]):
                if debug: print("start adding playlist uri:", playlist[0]["uri"])
                addPlaylist(mydb, playlist[0])
            for (ind, track) in enumerate(playlist[1]):
                if debug: print("persist_playlists: tracks", ind, ":", track["track"]["uri"])
                if not trackExists(mydb, track):
                    if debug: print("start adding track:", ind)
                    addTrack(mydb, track, playlist[0]["uri"])

def persist_artists(mydb, artists_info1):
    # str=json.dumps(artists_info1, indent=4); if debug: print("persist_artists:", len(artists_info1), "artists:", str)
    if debug: print("persist_artists:", len(artists_info1))
    for (key, value) in artists_info1.items():
        if debug: print("persit_artists: artist:", key)
        if not artistExists(mydb, key):
            addArtist(mydb, value)
            if debug: print("added artist")
def persist_toptracks(mydb, toptracks_info):
    if debug: print("persist_toptracks: not implemented")
