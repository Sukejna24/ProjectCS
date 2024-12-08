import streamlit as st
import sqlite3
import pandas as pd
import bcrypt
import hashlib
from datetime import datetime
import os
import plotly.express as px
import time

def main():
    # Verzeichnis des aktuellen Skripts
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_name_spotify_songs = os.path.join(script_dir, "spotify_songs.csv")
    df = pd.read_csv(file_name_spotify_songs)

    # Erstelle drei Spalten, wobei die äußeren als Ränder dienen, um das Bild in der Mitte zu zentrieren
    col1, col2, col3 = st.columns([1, 3, 1])

    # Einfügen des Spotify Logos
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Spotify.png", width=150)
    
    st.title("Spotify Melody Match")

    # Hauptdatenbank für Benutzer
    file_name_users = os.path.join(script_dir, "users.db")
    conn_users = sqlite3.connect(file_name_users)
    c_users = conn_users.cursor()
    c_users.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT, password TEXT)''')
    conn_users.commit()

    # Hash-Funktion für Passwörter
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    # Funktion zur Erstellung einer Benutzer-ID
    def generate_user_id(username):
        timestamp = datetime.now().strftime("%H%M%S")  # Nur Stunden, Minuten, Sekunden
        data = f"{username}{timestamp}"
        user_hash = hashlib.md5(data.encode()).hexdigest()[:5]  # Kürze den Hash auf 5 Zeichen
        return user_hash

    # Funktion zum Erstellen und Befüllen der Benutzer-Datenbank
    def create_user_database(user_id):
        user_db_path = os.path.join(script_dir, f"{user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)
        df.to_sql('user_songs', conn_user_db, if_exists='replace', index=False)
        conn_user_db.commit()
        conn_user_db.close()

    # Registrierung
    def register_user(username, password):
        if user_exists(username):
            st.warning("Benutzername existiert bereits!")
        else:
            user_id = generate_user_id(username)
            hashed_password = hash_password(password)
            c_users.execute("INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", 
                            (user_id, username, hashed_password))
            conn_users.commit()

            # Erstelle individuelle Benutzer-Datenbank
            create_user_database(user_id)

            st.success(f"Registrierung erfolgreich! Ihre Benutzer-ID ist: {user_id}")

    # Überprüfen, ob Benutzer existiert
    def user_exists(username):
        c_users.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c_users.fetchone()

    # Login überprüfen
    def login_user(username, password):
        c_users.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c_users.fetchone()
        if user and check_password(password, user[2]):
            return user[0]  # Gibt die user_id zurück
        return None

    # Streamlit-Anwendung
    with st.sidebar:
        st.header("Login & Registrierung")

    # Session-Handling
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""

    # Login oder Registrierung anzeigen
    with st.sidebar:
        if not st.session_state.logged_in:
            option = st.selectbox("Aktion wählen", ["Login", "Registrieren"])
    
            username = st.text_input("Benutzername")
            password = st.text_input("Passwort", type="password")

            if option == "Registrieren":
                if st.button("Registrieren"):
                    register_user(username, password)
            elif option == "Login":
                if st.button("Login"):
                    user_id = login_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = user_id
                        st.success(f"Willkommen, {username}!")
                    else:
                        st.error("Falscher Benutzername oder Passwort.")
        else:
            st.sidebar.success(f"Eingeloggt als: {st.session_state.username}")
            st.sidebar.write(f"Ihre Benutzer-ID: {st.session_state.user_id}")
            st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": "", "user_id": ""}))

    # Nach erfolgreichem Login Benutzer-Datenbank anzeigen
    if st.session_state.logged_in:
        st.header("Ihre persönlichen Songs")
        user_db_path = os.path.join(script_dir, f"{st.session_state.user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)

        # Benutzer-spezifische Daten abrufen
        user_songs_df = pd.read_sql_query("SELECT * FROM user_songs", conn_user_db)
        st.write(user_songs_df)

        conn_user_db.close()

    # Musikpräferenzen
    st.write("Welcome to Melody Match! Find the perfect playlist for you and your friends.")
    st.header("Find your Match!")

    # Gruppiere die Songs nach Playlist-ID
    playlists = df.groupby('playlist_id')

    # Auswahl der Playlist
    playlist_ids = df['playlist_id'].unique()

    # Hinweis auf die maximale Auswahl
    st.write("Choose 2 playlists:")

    def get_sample_playlists(df):
        sampled_playlists = df.reset_index(drop=True)
        sampled_playlists['playlist_display_name'] = sampled_playlists.apply(
            lambda row: f"Playlist {row['playlist_name']} - Songs from Artists like '{row['track_artist']}'", axis=1
        )
        return sampled_playlists

    sampled_playlists = get_sample_playlists(df)

    if not sampled_playlists.empty:
        playlist_id_to_name = dict(zip(sampled_playlists['playlist_id'], sampled_playlists['playlist_display_name']))

        selected_playlist_display_names = st.multiselect(
            "Choose playlists",
            options=list(playlist_id_to_name.values()),
            format_func=lambda name: name
        )
        selected_playlist_ids = [
            playlist_id for playlist_id, display_name in playlist_id_to_name.items()
            if display_name in selected_playlist_display_names
        ]

        if len(selected_playlist_ids) > 2:
            st.warning("A maximum of 2 Playlists can be selected.")

        if selected_playlist_ids:
            mix_button = st.button("Mix up")
            if mix_button:
                st.write("Mixing up your preferences...")
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.05)
                    progress_bar.progress(percent_complete + 1)
                st.success("Loading complete!")

            for playlist_id in selected_playlist_ids:
                selected_playlist = df[df['playlist_id'] == playlist_id]
                st.write(f"Songs in {playlist_id_to_name[playlist_id]}:")
                st.write(selected_playlist[['track_name', 'track_artist', 'duration_ms']])
    else:
        st.error("No playlists available to display.")

    # Filterfunktion
    st.write("If there was no potential match found, click below.")

    if "expander_opened" not in st.session_state:
        st.session_state.expander_opened = False

    with st.expander("Choose the attributes of your desired Playlist", expanded=st.session_state.expander_opened):
        st.header("Choose the attributes of your desired Playlist")
    
        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            st.write("Slow")
        with col2:
            tempo_range = st.slider("Tempo", min_value=0.0, max_value=240.0, value=(0.0, 240.0), step=10.0, label_visibility="collapsed")
        with col3:
            st.write("Fast")

        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            st.write("Sad")
        with col2:
            valence_range = st.slider("Valence", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
        with col3:
            st.write("Happy")

        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            st.write("Low Energy")
        with col2:
            energy_range = st.slider("Energy", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
        with col3:
            st.write("High Energy")

        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            st.write("Less Danceable")
        with col2:
            danceability_range = st.slider("Danceability", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
        with col3:
            st.write("More Danceable")

    filtered_songs = df[
        (df['tempo'] >= tempo_range[0]) & (df['tempo'] <= tempo_range[1]) &
        (df['valence'] >= valence_range[0]) & (df['valence'] <= valence_range[1]) &
        (df['energy'] >= energy_range[0]) & (df['energy'] <= energy_range[1]) &
        (df['danceability'] >= danceability_range[0]) & (df['danceability'] <= danceability_range[1])
    ]

    st.write("### Songs that match your preferences")

    if not filtered_songs.empty:
        st.write(filtered_songs[['track_name', 'track_artist', 'tempo', 'valence', 'energy', 'danceability']])
    else:
        st.write("No songs match your preferences.")

if __name__ == "__main__":
    main()