import streamlit as st
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API-Anmeldeinformationen
CLIENT_ID = '503970174ce54084923698fe550336f4'
CLIENT_SECRET = '5b5397398bf84dd2a8e06b808c280e71'
REDIRECT_URI = 'https://projectcs-kfdnyesodcfqp5dnwrihwp.streamlit.app/'

# Funktion zur Authentifizierung und Erstellung eines Spotify-Objekts
def authenticate_spotify():
    scope = 'user-library-read user-top-read playlist-modify-public'
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope)
    
    auth_url = sp_oauth.get_authorize_url()
    st.write(f"Bitte [klicke hier, um dich anzumelden]({auth_url}) und kopiere den Code in das folgende Feld.")

    # Nutzer gibt den Code ein
    code = st.text_input("Füge den Authentifizierungs-Code hier ein:")

    if code:
        try:
            token_info = sp_oauth.get_access_token(code)
            sp = spotipy.Spotify(auth=token_info['access_token'])
            return sp  # Gibt das authentifizierte Spotify-Objekt zurück
        except Exception as e:
            st.error(f"Authentifizierungsfehler: {e}")
            return None
    return None

def main():

    # Seitenleiste mit Text und anderen Elementen
    st.sidebar.header("Do you like the application?")
    st.sidebar.write("Please rate your experience with us")
    
    # Setze die Sterne als Buttons
    ### Benutzer kann auf einen der Buttons klicken, um eine Bewertung abzugeben
    stars = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    rating = st.sidebar.radio("", options=stars, index=2)  # Standardwert auf "⭐⭐⭐" setzen

    # Ausgabe der gewählten Bewertung
    st.sidebar.write(f"Du hast {rating} vergeben.")

    # Erstelle drei Spalten, wobei die äußeren als Ränder dienen
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Bild-URL
        st.image("https://heise.cloudimg.io/v7/_www-heise-de_/imgs/18/2/3/3/6/7/4/2/spotify-1360002_1920-4bbacbcc4c3c6a37.jpeg?force_format=avif%2Cwebp%2Cjpeg&org_if_sml=1&q=30&width=1920", width=150)
    
    st.title("Spotify Melody Match")

    # Musikpräferenzen
    st.write("Welcome to Melody Match! Find the perfect playlist for you and your friends.")
    st.header("Find your Match!")

    # Hinweis auf die maximale Auswahl
    st.write("Choose 2 playlists:")

    #Liste der Playlists
    artists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5"]

    # Multiselect mit einer maximalen Auswahl von 2 Playlists
    selected_artists = st.multiselect("Choose at least one", artists, max_selections=2)  # Maximale Anzahl von auswählbaren Künstlern

    # Wenn mehr als 2 Künstler ausgewählt werden, zeige eine Warnung
    if len(selected_artists) > 2:
        st.warning("A maximum of 2 Playlists can be selected.")
    
    if len(selected_artists) > 0:
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
