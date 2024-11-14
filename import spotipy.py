import streamlit
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
