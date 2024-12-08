import streamlit as st
import sqlite3
import pandas as pd
import bcrypt
import hashlib
from datetime import datetime
import os

def main():
    # Initialisierung der Session-States
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    if 'show_legend' not in st.session_state:
        st.session_state.show_legend = False
    if 'expander_opened' not in st.session_state:
        st.session_state.expander_opened = False  # Initialisierung von expander_opened

    # Erstelle drei Spalten, wobei die äußeren als Ränder dienen um das Bild in der Mitte zu zentrieren
    col1, col2, col3 = st.columns([1, 3, 1])

    # Einfügen des Spotify Logos
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Spotify.png", width=150)
    
    st.title("Spotify Melody Match")

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
            st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": "", "user_id": "", "show_legend": False}))

    # Nach erfolgreichem Login Benutzer-Datenbank anzeigen (nur einen kleinen Teil)
    if st.session_state.logged_in:
        st.header("Ihre persönlichen Songs")

        # Zugriff auf die Datenbank des Benutzers
        user_db_path = os.path.join(songs_dir, f"{st.session_state.user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)

        # Daten für einen Overview abrufen
        query_playlist_overview = """SELECT DISTINCT playlist_name, playlist_genre, playlist_subgenre, track_artist, track_album_name, track_name FROM user_songs"""
        user_songs_df_overview = pd.read_sql_query(query_playlist_overview, conn_user_db)

        # Scrollbare Tabelle anzeigen
        st.dataframe(user_songs_df_overview, use_container_width=True, height=200)

        with st.expander("Suche", expanded=st.session_state.expander_opened):

            # Dynamische Suchoption hinzufügen
            search_column_1 = st.selectbox("Suche nach:", ["track_artist", "track_name", "playlist_name"], key="search_column_1")
            search_query_1 = st.text_input(f"Geben Sie den {search_column_1} ein:", key="search_query_1")

            # Suchergebnisse anzeigen
            if search_query_1:
                query_playlist_search_1 = f"""SELECT DISTINCT playlist_name, track_artist, track_name, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms FROM user_songs WHERE {search_column_1} LIKE ?"""
                user_songs_df_search_1 = pd.read_sql_query(query_playlist_search_1, conn_user_db, params=(f"%{search_query_1}%",))
                if not user_songs_df_search_1.empty:
                    # Ergebnisse anzeigen, wenn etwas gefunden wurde
                    st.dataframe(user_songs_df_search_1, use_container_width=True, height=400)

                    # Zeige "Legende"-Button nach erfolgreicher Suche
                    if st.button("Erklärung der Audio Features", key="audio_features"):
                        st.session_state.show_legend = not st.session_state.show_legend

                    # Beschreibungen anzeigen, wenn "Legende" aktiviert ist
                    if st.session_state.show_legend:
                        st.markdown("""
                        ### Danceability
                        Gibt an, wie geeignet ein Track für das Tanzen ist. Basierend auf einer Kombination von Elementen wie Tempo, Rhythmus-Stabilität, Beat-Stärke und Gesamtrhythmus.  
                        **Skala:** 0.0 bis 1.0 (höherer Wert = tanzbarer).

                        ### Energy
                        Gibt das Maß an Intensität und Aktivität eines Tracks an. Tracks mit hoher Energie haben ein schnelles Tempo, einen starken Beat und laute Instrumente.  
                        **Skala:** 0.0 bis 1.0 (höherer Wert = energischer).

                        ### Valence
                        Gibt die musikalische Positivität eines Tracks an. Tracks mit hoher Valence klingen fröhlich, glücklich und euphorisch.  
                        **Skala:** 0.0 bis 1.0 (höherer Wert = positiver).

                        ### Tempo
                        Das geschätzte Tempo des Tracks in Schlägen pro Minute (BPM).  
                        **Einheit:** Beats pro Minute (BPM).

                        ### Speechiness
                        Gibt den Anteil der gesprochenen Worte in einem Track an. Hohe Werte deuten auf mehr gesprochene Inhalte hin (z. B. Podcasts, Audiobooks, Rap).  
                        **Skala:** 
                        - Werte über 0.66: Wahrscheinlich reiner gesprochener Inhalt.
                        - 0.33–0.66: Mischung aus Musik und gesprochenen Inhalten.
                        - Unter 0.33: Hauptsächlich Musik.

                        ### Liveness
                        Gibt die Wahrscheinlichkeit an, dass der Track vor einem Live-Publikum aufgeführt wurde.  
                        **Skala:** 0.0 bis 1.0 (höherer Wert = mehr Live-Charakter). Werte über 0.8 deuten auf Live-Aufnahmen hin.

                        ### Instrumentalness
                        Schätzt, wie instrumental ein Track ist. Höhere Werte deuten darauf hin, dass der Track wenig oder keinen Gesang enthält.  
                        **Skala:** 0.0 bis 1.0 (Werte nahe 1.0 deuten auf reine Instrumentalmusik hin).

                        ### Acousticness
                        Gibt an, wie akustisch ein Track ist.  
                        **Skala:** 0.0 bis 1.0 (höherer Wert = stärker akustisch).

                        ### Key
                        Gibt die Tonart des Tracks an.  
                        **Werte:** 
                        - 0 = C
                        - 1 = C#
                        - 2 = D
                        - …
                        - 11 = B
                        - -1: Keine Tonart erkennbar.

                        ### Mode
                        Gibt an, ob ein Track in Dur (1) oder Moll (0) ist.

                        ### Loudness
                        Gibt die durchschnittliche Lautstärke des Tracks in Dezibel (dB) an.  
                        **Einheit:** Dezibel (dB).

                        ### Duration_ms
                        Die Länge des Tracks in Millisekunden.  
                        **Einheit:** Millisekunden (ms).

                        ### Time Signature
                        Gibt die geschätzte Anzahl der Beats pro Takt an.  
                        **Werte:**
                        - 3 = 3/4-Takt (Walzer)
                        - 4 = 4/4-Takt (Standard)
                        """)
                else:
                    # Nachricht anzeigen, wenn keine Treffer vorhanden sind
                    st.warning("Kein Treffer gefunden. Versuchen Sie es mit einer anderen Eingabe.")

        # Filter nach Audio-Features
        query_playlist_filter = """SELECT DISTINCT track_artist, track_name, tempo, valence, energy, danceability FROM user_songs"""
        user_songs_df_filter = pd.read_sql_query(query_playlist_filter, conn_user_db)

        with st.expander("Filter nach Audio-Features", expanded=st.session_state.expander_opened):
            # Tempo-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Langsames Tempo")
            with col2:
                tempo_range = st.slider("Tempo", min_value=0.0, max_value=240.0, value=(0.0, 240.0), step=10.0, label_visibility="collapsed")
            with col3:
             st.write("Schnelles Tempo")

            # Valence-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Traurig")
            with col2:
                valence_range = st.slider("Valence", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
            with col3:
                st.write("Fröhlich")

            # Energy-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Niedrige Energie")
            with col2:
                energy_range = st.slider("Energy", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
            with col3:
                st.write("Hohe Energie")

            # Danceability-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Weniger tanzbar")
            with col2:
                danceability_range = st.slider("Danceability", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
            with col3:
                st.write("Mehr tanzbar")

            # Songs nach den Filtern auswählen
            filtered_songs = user_songs_df_filter[
                (user_songs_df_filter['tempo'] >= tempo_range[0]) & (user_songs_df_filter['tempo'] <= tempo_range[1]) &
                (user_songs_df_filter['valence'] >= valence_range[0]) & (user_songs_df_filter['valence'] <= valence_range[1]) &
                (user_songs_df_filter['energy'] >= energy_range[0]) & (user_songs_df_filter['energy'] <= energy_range[1]) &
                (user_songs_df_filter['danceability'] >= danceability_range[0]) & (user_songs_df_filter['danceability'] <= danceability_range[1])
                ]

            # Gefilterte Songs anzeigen
            st.subheader("Gefilterte Songs")
            if not filtered_songs.empty:
                st.dataframe(filtered_songs, use_container_width=True, height=400)

                # Legenden-Schalter
                if st.button("Erklärung der Audio Features", key="audio_features_duplicate"):
                    st.session_state.show_legend = not st.session_state.show_legend

                # Beschreibungen anzeigen, wenn "Legende" aktiviert ist
                if st.session_state.show_legend:
                    st.markdown("""
                    ### Tempo
                    Das geschätzte Tempo des Tracks in Schlägen pro Minute (BPM).  
                    **Einheit:** Beats pro Minute (BPM).
                        
                    ### Valence
                    Gibt die musikalische Positivität eines Tracks an. Tracks mit hoher Valence klingen fröhlich, glücklich und euphorisch.  
                    **Skala:** 0.0 bis 1.0 (höherer Wert = positiver).
                        
                    ### Danceability
                    Gibt an, wie geeignet ein Track für das Tanzen ist. Basierend auf einer Kombination von Elementen wie Tempo, Rhythmus-Stabilität, Beat-Stärke und Gesamtrhythmus.  
                    **Skala:** 0.0 bis 1.0 (höherer Wert = tanzbarer).

                    ### Energy
                    Gibt das Maß an Intensität und Aktivität eines Tracks an. Tracks mit hoher Energie haben ein schnelles Tempo, einen starken Beat und laute Instrumente.  
                    **Skala:** 0.0 bis 1.0 (höherer Wert = energischer).

                    ### Danceability
                    Wie tanzbar der Track ist. Höherer Wert = besser für Tanz geeignet.
                """)

            else:
                st.warning("Keine Songs entsprechen den Filterkriterien.")

        # CSS zur Anpassung des Designs
        st.markdown("""
            <style>
            .song-list {
                font-size: 14px !important;
                line-height: 1.6 !important;
                display: flex;
                justify-content: space-between;
            }
            .remove-button {
                font-size: 10px !important;
                padding: 1px 3px !important;
                color: red !important;
                background: none !important;
                border: none !important;
                cursor: pointer !important;
            }
            .song-count {
                font-size: 16px !important;
                font-weight: bold !important;
                margin-bottom: 10px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.expander("Mix Up", expanded=st.session_state.expander_opened):
            # Dynamische Suchoption hinzufügen
            search_column_2 = st.selectbox("Suche nach:", ["track_artist", "track_name"], key="search_column_2")
            search_query_2 = st.text_input(f"Geben Sie den {search_column_2} ein:", key="search_query_2")

            # Warenkorb in der Session speichern
            if "cart" not in st.session_state:
                st.session_state.cart = []

            # Anzahl der Songs im Warenkorb anzeigen
            if st.session_state.cart:
                st.markdown(f"<div class='song-count'>Ausgewählte Songs: {len(st.session_state.cart)}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='song-count'>Ihr Warenkorb ist leer.</div>", unsafe_allow_html=True)

            # Suchergebnisse anzeigen
            if search_query_2:
                # Abfrage von Tracks nach Suchbegriff
                query_playlist_search_2 = f"""
                SELECT DISTINCT track_artist, track_name, danceability, energy, key, loudness, mode, speechiness, acousticness, 
                instrumentalness, liveness, valence, tempo, duration_ms 
                FROM user_songs WHERE {search_column_2} LIKE ?
                """
                user_songs_df_search_2 = pd.read_sql_query(query_playlist_search_2, conn_user_db, params=(f"%{search_query_2}%",))

                if not user_songs_df_search_2.empty:
                    st.write("Wählen Sie Songs aus, um sie in den Warenkorb zu legen:")
                    
                    for i, row in user_songs_df_search_2.iterrows():
                        # Eindeutigen Schlüssel für die Checkbox generieren
                        checkbox_key = f"checkbox_{i}_{row['track_name']}_{row['track_artist']}"
                        is_checked = row.to_dict() in st.session_state.cart
                        checked = st.checkbox(
                            f"{row['track_name']} von {row['track_artist']}", 
                            value=is_checked, 
                            key=checkbox_key
                        )
                        if checked and not is_checked:
                            # Hinzufügen zum Warenkorb
                            st.session_state.cart.append(row.to_dict())
                        elif not checked and is_checked:
                            # Entfernen aus dem Warenkorb
                            st.session_state.cart.remove(row.to_dict())
                else:
                    # Meldung anzeigen, wenn keine Treffer gefunden werden
                    st.warning("Kein Treffer gefunden. Versuchen Sie es mit einer anderen Eingabe.")

            # Warenkorb anzeigen (immer sichtbar)
            if st.session_state.cart:
                st.write("Ihr Warenkorb:")
                for index, track in enumerate(st.session_state.cart):
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"<div class='song-list'><b>{track['track_name']}</b> - <i>{track['track_artist']}</i></div>", unsafe_allow_html=True)
                    with col2:
                        if st.button(f"❌", key=f"remove_cart_{index}", help="Löschen"):
                            st.session_state.cart.pop(index)
                            st.experimental_rerun()  # Seite neu laden, um Änderungen zu reflektieren

            # Button nur anzeigen, wenn 20 Songs im Warenkorb sind
            if len(st.session_state.cart) >= 20:
                if st.button("Ähnliche Songs finden"):
                    # DataFrame aus dem Warenkorb erstellen
                    selected_tracks_df = pd.DataFrame(st.session_state.cart)

                    # Machine-Learning-Modell verwenden, um ähnliche Songs zu finden
                    from sklearn.neighbors import NearestNeighbors
                    import numpy as np

                    # Daten für ML vorbereiten
                    feature_columns = [
                        "danceability", "energy", "key", "loudness", "mode",
                        "speechiness", "acousticness", "instrumentalness", "liveness",
                        "valence", "tempo", "duration_ms"
                    ]

                    # Fit-Modell auf allen Songs
                    query_playlist_all = """
                    SELECT * FROM user_songs
                    """
                    user_songs_df_all= pd.read_sql_query(query_playlist_all, conn_user_db)
                    knn = NearestNeighbors(n_neighbors=300, metric="euclidean")
                    knn.fit(user_songs_df_all[feature_columns])

                    # Suche nach ähnlichen Songs basierend auf den ausgewählten Tracks
                    selected_features = selected_tracks_df[feature_columns].values
                    distances, indices = knn.kneighbors(selected_features)

                    # Ergebnisse sammeln
                    user_songs_df_similar = user_songs_df_all.iloc[np.unique(indices.flatten())]

                    # Playlist-Metadaten hinzufügen
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    user_songs_df_similar["playlist_name"] = f"Mix Up {timestamp}"
                    user_songs_df_similar["playlist_genre"] = f"Mix Up {timestamp}"
                    user_songs_df_similar["playlist_subgenre"] = f"Mix Up {timestamp}"
                    user_songs_df_similar["playlist_id"] = timestamp

                    # Ergebnisse anzeigen
                    st.subheader("Ähnliche Songs")
                    st.dataframe(user_songs_df_similar, use_container_width=True, height=400)

                    if st.button("Passt diese Playlist?"):
                        try:
                            # Playlist an all_songs_df anhängen
                            query_playlist_all = pd.concat([query_playlist_all, user_songs_df_similar], ignore_index=True)
                            
                            # Überschreibe die Datenbank mit all_songs_df
                            query_playlist_all.to_sql("user_songs", conn_user_db, if_exists="replace", index=False)

                            # Datenbankänderungen speichern
                            conn_user_db.commit()

                            # Erfolgreiche Speicherung bestätigen
                            st.success("Die Playlist wurde erfolgreich gespeichert.")
                        except Exception as e:
                            st.error(f"Fehler beim Speichern der Playlist: {e}")
                        finally:
                            # Verbindung schließen
                            conn_user_db.close()

        conn_user_db.close()

if __name__ == "__main__":
    main()