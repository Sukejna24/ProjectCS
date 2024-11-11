import streamlit as st


def main():

    
    st.title("Spotify Melody Match")
    st.write("Willkommen bei - Melody Match! Wähle zwei Playlists aus.")

    # Musikpräferenzen
    st.header("Wähle 2 deiner Lieblingsplaylists in Spotify")

    # Auswahlmöglichkeiten für Genres
    playlists = ['Pop', 'Rock', "Music", 'Hip-Hop', 'Jazz', 'Classical']
    selected_playlists = st.multiselect("Wähle deine Playlists:", playlists)

    # Auswahlmöglichkeiten für Künstler
    artists = ['Taylor Swift', 'The Weeknd', 'Ed Sheeran', 'Beyoncé', 'Adele']
    selected_artists = st.multiselect("Wähle deine Lieblingskünstler:", artists)

    # Button für den Mix mit Machine Learning
    if st.button("Mix Up"):
        # Hier kommt die Logik für das Zusammenmischen der Songs
        st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik

        # Beispielausgabe, die du später anpassen kannst
        st.write("Empfohlene Songs für dich könnten sein: ...")

    st.slider("tempo", min_value = 0.0, max_value=1.0, value = 0.5, step = 0.1)
    Lieblingssong = st.text_input("Dein Song:")


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

if __name__ == "__main__":
    main()
    