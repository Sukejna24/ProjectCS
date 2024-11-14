import streamlit as st


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

    # Beispiel für einen Slider in der Seitenleiste
    value = st.sidebar.slider("Rate this app", min_value=1, max_value=5, value=3, step=1)

    # Beispiel für eine Auswahlbox in der Seitenleiste
    option = st.sidebar.selectbox("Wähle eine Option", ["Option 1", "Option 2", "Option 3"])
   
    # Erstelle zwei gleich breite Spalten
    col1, col2 = st.columns(2)

    #Hauptbereich
    with col1:
        st.title("Spotify Melody Match")

    with col2:
        # Bild-URL
        st.image("https://assets.turbologo.com/blog/en/2021/07/20045641/Spotify_logo_symbol.png", width=120)
    
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
        # Hier kommt die Logik für das Zusammenmischen der Songs
        st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik
         # Beispielausgabe, die du später anpassen kannst

    #Falls kein möglicher Match
    st.write("If there was no potential match found, click below.")


    # Widgets innerhalb des Containers anzeigen
    with st.expander("Choose the attributes of your desired Playlist"):
        st.header("Choose the attributes of your desired Playlist")
        st.slider("Tempo", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
        st.slider("Valence", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
        st.slider("Energy", min_value=0.0, max_value=1.0, value=0.4, step=0.2)
        st.slider("Danceability", min_value=0.0, max_value=1.0, value=0.4, step=0.2)

    if st.button("Search Playlists"):
        st.write("Recommended songs for you could be: ...")
if __name__ == "__main__":
    main()