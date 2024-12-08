import streamlit as st
import sqlite3
import pandas as pd
import bcrypt
import hashlib
from datetime import datetime
import os

def main():
    # Verzeichnis des aktuellen Skripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    songs_dir = os.path.join(script_dir, "songs")

    # Stelle sicher, dass das Verzeichnis "songs" existiert
    if not os.path.exists(songs_dir):
        os.makedirs(songs_dir)

    file_name_spotify_songs = os.path.join(script_dir, "spotify_songs.csv")
    df = pd.read_csv(file_name_spotify_songs)

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
        user_db_path = os.path.join(songs_dir, f"{user_id}.db")
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

        # Zugriff auf die Datenbank des Benutzers
        user_db_path = os.path.join(songs_dir, f"{st.session_state.user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)

        # Benutzer-spezifische Daten abrufen
        query = """SELECT playlist_name, playlist_genre, playlist_subgenre, track_artist, track_album_name, track_name, playlist_name FROM user_songs"""
        user_songs_df = pd.read_sql_query(query, conn_user_db)
        conn_user_db.close()

        # Scrollbare Tabelle anzeigen
        st.dataframe(user_songs_df, use_container_width=True, height=600)

if __name__ == "__main__":
    main()
