import streamlit as st


def main():

    #Design anpassen
    st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:", layout="wide", initial_sidebar_state="expanded")

    # Seitenleiste mit Text und anderen Elementen
    st.sidebar.header("Dies ist die Seitenleiste")
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

    # Hinweis auf die maximale Auswahl
    st.write("Choose 2 playlists:")

    #Liste der Playlists
    artists = ["Playlist 1", "Playlist 2", "Playlist 3", "Playlist 4", "Playlist 5"]

    # Multiselect mit einer maximalen Auswahl von 2 Playlists
    selected_artists = st.multiselect("Select artists", artists, max_selections=2)  # Maximale Anzahl von auswählbaren Künstlern

    # Wenn mehr als 2 Künstler ausgewählt werden, zeige eine Warnung
    if len(selected_artists) > 2:
        st.warning("A maximum of 2 artists can be selected.")

    # Zeige die ausgewählten Künstler
    if selected_artists:
        st.write(f"You selected: {', '.join(selected_artists)}")

    # Button für den Mix mit Machine Learning
    if st.button("Mix Up"):
        # Hier kommt die Logik für das Zusammenmischen der Songs
        st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik
         # Beispielausgabe, die du später anpassen kannst
        st.write("Recommended songs for you could be: ...")

    # Bild von der lokalen Festplatte einfügen
    st.image("C:\Users\jessy\OneDrive\Fotos\Documentos\Uni HSG\Bachelor\6. Semester\CS\CS Projekt\Bild Spotify.jpeg", caption="Dies ist ein Bild", use_column_width=True)

    #Falls kein möglicher Match
    st.write("No potential match found.")
    st.write("Choose the attributes of your desired Playlist")
    st.slider("tempo", min_value = 0.0, max_value=1.0, value = 0.4, step = 0.2)
    st.slider("Valence", min_value = 0.0, max_value=1.0, value = 0.4, step = 0.2)
    st.slider("Energy", min_value = 0.0, max_value=1.0, value = 0.4, step = 0.2)
    st.slider("Danceability", min_value = 0.0, max_value=1.0, value = 0.4, step = 0.2)
    if st.button("Search Playlists"):
        Lieblingssong = st.text_input("Dein Song:")

if __name__ == "__main__":
    main()
    