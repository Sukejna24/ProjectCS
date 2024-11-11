import streamlit as st


def main():

    
    st.title("Spotify Melody Match")
    st.write("Willkommen bei - Melody Match! Finde die Playlist für dich und deine Freunde")

    # Musikpräferenzen
    st.header("Finde deinen Match!")

    # Auswahlmöglichkeiten für Genres
    playlists = ['Pop', 'Rock', "Music", 'Hip-Hop', 'Jazz', 'Classical']
    selected_playlists = st.multiselect("Wähle deine Playlists:", playlists)

     # Liste der Künstler
    artists = ["Taylor Swift", "Drake", "Beyoncé", "Adele", "The Weeknd", "Billie Eilish", "Ed Sheeran"]

    # Variable für ausgewählte Künstler
    selected_artists = []

    # Hinweis auf die maximale Auswahl
    st.write("Wähle bis zu 2 Lieblingskünstler:")

    # Schleife durch die Künstlerliste und Checkboxen erstellen
    for artist in artists:
        if st.checkbox(artist, key=artist):
            selected_artists.append(artist)

    # Falls die maximale Anzahl erreicht ist, keine weiteren Checkboxen zulassen
        if len(selected_artists) >= 2:
         st.warning("Maximal 2 Künstler auswählbar.")
         break

    st.write("Ausgewählte Künstler:", selected_artists)

    # Button für den Mix mit Machine Learning
    if st.button("Mix Up"):
        # Hier kommt die Logik für das Zusammenmischen der Songs
        st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik

        # Beispielausgabe, die du später anpassen kannst
        st.write("Empfohlene Songs für dich könnten sein: ...")

    st.slider("tempo", min_value = 0.0, max_value=1.0, value = 0.5, step = 0.1)
    Lieblingssong = st.text_input("Dein Song:")

if __name__ == "__main__":
    main()
    