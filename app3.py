import streamlit as st


def main():

    # Seitenleiste mit Text und anderen Elementen
    st.sidebar.write("Dies ist die Seitenleiste")
    st.sidebar.write("Hier kannst du zusätzliche Informationen anzeigen oder Filter auswählen.")

    # Beispiel für einen Slider in der Seitenleiste
    value = st.sidebar.slider("Wähle eine Zahl", 0, 100, 50)

    # Beispiel für eine Auswahlbox in der Seitenleiste
    option = st.sidebar.selectbox("Wähle eine Option", ["Option 1", "Option 2", "Option 3"])

    # Hauptbereich
    st.write("Hauptbereich")
    st.write(f"Ausgewählte Zahl: {value}")
    st.write(f"Ausgewählte Option: {option}")

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
    st.write("Wähle zwei Playlists aus:")

    # Schleife durch die Künstlerliste und Checkboxen erstellen
    for artist in artists:
        if st.checkbox(artist, key=artist):
            selected_artists.append(artist)

    # Falls die maximale Anzahl erreicht ist, keine weiteren Checkboxen zulassen
        if len(selected_artists) >= 2:
         st.warning("Maximal 2 Künstler auswählbar.")
         break

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
    