import streamlit as st


def main():


    # Seitenleiste mit Text und anderen Elementen
    st.sidebar.write("Dies ist die Seitenleiste")
    st.sidebar.write("Hier kannst du zusätzliche Informationen anzeigen oder Filter auswählen.")

    # Beispiel für einen Slider in der Seitenleiste
    value = st.sidebar.slider("Wähle eine Zahl", 0, 100, 50)

    # Beispiel für eine Auswahlbox in der Seitenleiste
    option = st.sidebar.selectbox("Wähle eine Option", ["Option 1", "Option 2", "Option 3"])

    #Hauptbereich
    st.title("Spotify Melody Match")
    st.write("Welcome to Melody Match! Find the perfect playlist for you and your friends.")

    # Musikpräferenzen
    st.header("Find your Match!")

    # Auswahl zwischen multiselect oder checkbox
    playlists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5"]
    selected_playlists = st.multiselect("Choose 2 playlists:", playlists)

     # Liste der Künstler
    artists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5"]

    # Variable für ausgewählte Künstler
    selected_artists = []

    # Hinweis auf die maximale Auswahl
    st.write("Choose 2 playlists:")

    # Schleife durch die Künstlerliste und Checkboxen erstellen
    for artist in artists:
        if st.checkbox(artist, key=artist):
            selected_artists.append(artist)

    # Falls die maximale Anzahl erreicht ist, keine weiteren Checkboxen zulassen
        if len(selected_artists) >= 2:
         st.warning("A maximum of 2 artists can be selected.")
         break

    # Button für den Mix mit Machine Learning
    if st.button("Mix Up"):
        # Hier kommt die Logik für das Zusammenmischen der Songs
        st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik

        # Beispielausgabe, die du später anpassen kannst
        st.write("Recommended songs for you could be: ...")

    #Falls kein möglicher Match
    st.write("No potential match found.")
    st.write("Choose the attributes of your desired Playlist")
    st.slider("tempo", min_value = 0.0, max_value=1.0, value = 0.5, step = 0.1)
    st.slider("Valence", min_value = 0.0, max_value=1.0, value = 0.5, step = 0.1)
    st.slider("Energy", min_value = 0.0, max_value=1.0, value = 0.5, step = 0.1)
    st.slider("Danceability", min_value = 0.0, max_value=1.0, value = 0.5, step = 0.1)
    if st.button("Search Playlists"):
        Lieblingssong = st.text_input("Dein Song:")

if __name__ == "__main__":
    main()
    