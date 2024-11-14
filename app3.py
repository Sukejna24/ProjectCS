import streamlit as st
import time


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
        st.image("https://assets.turbologo.com/blog/en/2021/07/20045641/Spotify_logo_symbol.png", width=120)
    
    st.title("Spotify Melody Match")

    # Musikpräferenzen
    st.write("Welcome to Melody Match! Find the perfect playlist for you and your friends.")
    st.header("Find your Match!")

    # Hinweis auf die maximale Auswahl
    st.write("Choose 2 playlists:")

    #Liste der Playlists
    artists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5"]

    # Multiselect mit einer maximalen Auswahl von 2 Playlists
    selected_artists = st.multiselect("", artists, max_selections=2)  # Maximale Anzahl von auswählbaren Künstlern

    # Wenn mehr als 2 Künstler ausgewählt werden, zeige eine Warnung
    if len(selected_artists) > 2:
        st.warning("A maximum of 2 artists can be selected.")

    # Zeige die ausgewählten Künstler
    if selected_artists:
        st.write(f"You selected: {', '.join(selected_artists)}")
        
    # Button für den Mix mit Machine Learning
    if st.button("Mix Up"):
        st.write("Mixing up your preferences...") # Placeholder für Machine Learning Logik
        # Ladebalken mit st.progress erstellen
        progress_bar = st.progress(0)

        # Beispielhafte Ladeaktion, die 100 Schritte dauert
        for percent_complete in range(100):
            time.sleep(0.05)  # Wartezeit simuliert das Laden
            progress_bar.progress(percent_complete + 1)  # Ladebalken erhöhen

        st.success("Loading complete!")  # Erfolgsmeldung nach Abschluss

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
