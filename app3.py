import streamlit as st


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
    selected_artists = st.multiselect(artists, max_selections=2)  # Maximale Anzahl von auswählbaren Künstlern

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
    st.image("https://assets.turbologo.com/blog/en/2021/07/20045641/Spotify_logo_symbol.png", width=90)

    #Falls kein möglicher Match
    st.write("No potential match found.")

    # CSS für den Container erstellen
    st.markdown("""
        <style>
            .custom-container {
                border: 2px solid #4CAF50;  /* Grüner Rahmen */
                padding: 20px;
                margin: 20px;
                border-radius: 10px;
                background-color: #f0f0f0;  /* Helles Grau als Hintergrund */
            }
        </style>
    """, unsafe_allow_html=True)

    # Den Container mit CSS-Klasse stylen, ohne HTML-Tags in Streamlit zu mischen
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    
    # Widgets innerhalb des Containers anzeigen
    st.header("Choose the attributes of your desired Playlist")
    st.slider("Tempo", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
    st.slider("Valence", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
    st.slider("Energy", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
    st.slider("Danceability", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
    
    # Den Container schließen (damit der Rahmen endet)
    st.markdown('</div>', unsafe_allow_html=True)


    if st.button("Search Playlists"):
        Lieblingssong = st.text_input("Dein Song:")

if __name__ == "__main__":
    main()