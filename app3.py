import streamlit as st
import time
import sqlite3
import pandas as pd
import bcrypt
import kagglehub
import plotly.express as px


def main():

    url = "https://raw.githubusercontent.com/Sukejna24/ProjectCS/13fa67d4859f3823f8dada76f37cb27520f9bf06/spotify_songs.csv"

    #Lade die CSV-Datei direkt von GitHub
    df = pd.read_csv(url)

    # Erstelle drei Spalten, wobei die äußeren als Ränder dienen um das Bild in der Mitte zu zentrieren
    col1, col2, col3 = st.columns([1, 3, 1])

    #Einfügen des Spotify logos
    with col2:
        # Bild-URL
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Spotify.png", width=150)
    
    st.title("Spotify Melody Match")

    # Datenbank einrichten für den Login einrichten
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    conn.commit()

    # Hash-Funktion für Passwörter
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    # Registrierung
    def register_user(username, password):
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

    # Überprüfen, ob Benutzer existiert
    def user_exists(username):
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c.fetchone()

    # Login überprüfen
    def login_user(username, password):
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and check_password(password, user[1]):
            return True
        return False

    #Streamlit-Anwendung
    with st.sidebar:
        st.header("Login & Registrierung")

    # Session-Handling
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

        # Login oder Registrierung anzeigen
    with st.sidebar:
        if not st.session_state.logged_in:
            option = st.selectbox("Aktion wählen", ["Login", "Registrieren"])
    
            username = st.text_input("Benutzername")
            password = st.text_input("Passwort", type="password")

            if option == "Registrieren":
                if st.button("Registrieren"):
                    if user_exists(username):
                        st.warning("Benutzername existiert bereits!")
                    else:
                        register_user(username, password)
                        st.success("Registrierung erfolgreich! Bitte einloggen.")
            elif option == "Login":
                if st.button("Login"):
                    if login_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"Willkommen, {username}!")
                    else:
                        st.error("Falscher Benutzername oder Passwort.")
        else:
            st.sidebar.success(f"Eingeloggt als: {st.session_state.username}")
            st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": ""}))

    
        # Extrahiere Songnamen (angenommen, 'track_name' ist der Name der Song-Spalte)
    song_names = df['track_name'].unique()

    # Songauswahl mit Selectbox
    selected_song = st.selectbox("Wähle einen Song aus", song_names)

    # Informationen zum ausgewählten Song filtern
    song_info = df[df['track_name'] == selected_song]

    # Songdetails anzeigen
    st.write(f"Details zum Song: {selected_song}")
    st.write(song_info)

    #Visualisierung zur Tanzbarkeit des Songs
    if 'danceability' in song_info.columns:
        st.line_chart(song_info['danceability'])

    #Weitere interaktive Features, z.B. für Bewertung oder Genre-Auswahl
    genre = st.radio("Wähle ein Genre:", df['playlist_genre'].unique())
    genre_data = df[df['playlist_genre'] == genre]
    
    st.write(f"### Songs im Genre: {genre}")
    st.write(genre_data)

    def plot_genre_distribution(df):
        genre_counts = df['playlist_genre'].value_counts()
        fig = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genre', 'y': 'Anzahl Songs'})
        st.plotly_chart(fig)

    #In deinem main()-Code
    plot_genre_distribution(df)

    # Seitenleiste mit Text und anderen Elementen
    st.sidebar.header("Do you like the application?")
    st.sidebar.write("Please rate your experience with us")
    
    # Setze die Sterne als Buttons
    ### Benutzer kann auf einen der Buttons klicken, um eine Bewertung abzugeben
    stars = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    rating = st.sidebar.radio("", options=stars, index=2)  # Standardwert auf "⭐⭐⭐" setzen

    # Ausgabe der gewählten Bewertung
    st.sidebar.write(f"Du hast {rating} vergeben.")


    # Musikpräferenzen
    st.write("Welcome to Melody Match! Find the perfect playlist for you and your friends.")
    st.header("Find your Match!")

    # Gruppiere die Songs nach Playlist-ID
    playlists = df.groupby('playlist_id')

    # Auswahl der Playlist
    playlist_ids = df['playlist_id'].unique()

    # Hinweis auf die maximale Auswahl
    st.write("Choose 2 playlists:")


    # Multiselect mit einer maximalen Auswahl von 2 Playlists
    selected_playlist_id = st.multiselect("Choose at least one", playlist_ids, max_selections=2)  # Maximale Anzahl von auswählbaren Künstlern

    # Wenn mehr als 2 Künstler ausgewählt werden, zeige eine Warnung
    if len(selected_playlist_id) > 2:
        st.warning("A maximum of 2 Playlists can be selected.")
    
    if len(selected_playlist_id) > 0:
        mix_button = st.button("Mix up")  # Der Button wird hier einmalig definiert
        
        if mix_button:
            st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik
            
            # Ladebalken mit st.progress erstellen
            progress_bar = st.progress(0)

            # Beispielhafte Ladeaktion, die 100 Schritte dauert
            for percent_complete in range(100):
                time.sleep(0.05)  # Wartezeit simuliert das Laden
                progress_bar.progress(percent_complete + 1)  # Ladebalken erhöhen
            st.success("Loading complete!")  # Erfolgsmeldung nach Abschluss
        # Zeige die Songs der ausgewählten Playlist an
        for selected_playlist_id in selected_playlist_ids:
            if selected_playlist_id in playlists.groups:
                selected_playlist = playlists.get_group(selected_playlist_id)
                st.write(f"Songs in Playlist ID {selected_playlist_id}:")
                st.write(selected_playlist[['song_name', 'artist', 'duration']])
            else:
                st.error(f"Playlist mit ID {selected_playlist_id} existiert nicht.")
    else:
        # Wenn keine Auswahl getroffen wurde, wird der Button deaktiviert
        st.button("Mix up", disabled=True)

   
    #Falls kein möglicher Match
    st.write("If there was no potential match found, click below.")

    # Zustand für den Expander initialisieren
    if "expander_opened" not in st.session_state:
        st.session_state.expander_opened = False  # Beim ersten Laden offen

    # Funktion zum Öffnen des Expanders, falls noch nicht offen
    def open_expander():
        if not st.session_state.expander_opened:
            st.session_state.expander_opened = True

    # Widgets innerhalb des Containers anzeigen
    with st.expander("Choose the attributes of your desired Playlist", expanded=st.session_state.expander_opened):
        st.header("Choose the attributes of your desired Playlist")
        st.slider("Tempo", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
        st.slider("Valence", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
        st.slider("Energy", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
        st.slider("Danceability", min_value=0.0, max_value=1.0, value=0.4, step=0.2)

    if st.button("Search Playlists"):
        st.write("Recommended songs for you could be: ...")
if __name__ == "__main__":
    main()
