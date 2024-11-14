import streamlit as st
from PIL import Image
import requests
from io import BytesIO


def main():


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
    
    # Bild-URL
    image_url = "https://assets.turbologo.com/blog/en/2021/07/20045641/Spotify_logo_symbol.png"

    # Bild von der URL laden
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Zeige das Bild und mache es "klickbar" über eine Auswahl
    selection = st.selectbox("Wähle eine Option", ("", "Klick auf das Bild"))

    # Wenn der Benutzer die Option wählt, wird eine Aktion ausgeführt
    if selection == "Klick auf das Bild":
        st.image(image, caption="Bild wurde angeklickt!", use_column_width=True)
        st.write("Das Bild wurde geklickt!")

    # Bild-URL
    image_url = "https://assets.turbologo.com/blog/en/2021/07/20045641/Spotify_logo_symbol.png"

    # HTML und CSS, um das Bild als Button darzustellen
    html_code = f"""
        <a href="#" onclick="window.parent.postMessage({{'type': 'image_click'}}, '*')">
         <img src="{image_url}" width="300"/>
        </a>
    """

    # Zeige das Bild als interaktiven Button
    st.markdown(html_code, unsafe_allow_html=True)

    # Wenn das Bild geklickt wird, wird eine Aktion ausgeführt
    # Dies funktioniert durch eine benutzerdefinierte Funktionalität in Streamlit (nach Bedarf angepasst)
    if st.session_state.get('image_click', False):
        st.write("Das Bild wurde geklickt!")

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