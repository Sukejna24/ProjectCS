import streamlit as st

def main():
    st.title("Melody Match")
    st.write("Willkommen bei - Melody Match! Wähle deine Musikpräferenzen.")

    # Musikpräferenzen
    st.header("Wähle deine Musikpräferenzen")

    # Auswahlmöglichkeiten für Genres
    genres = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical']
    selected_genres = st.multiselect("Wähle deine Lieblingsgenres:", genres)

    # Auswahlmöglichkeiten für Künstler
    artists = ['Taylor Swift', 'The Weeknd', 'Ed Sheeran', 'Beyoncé', 'Adele']
    selected_artists = st.multiselect("Wähle deine Lieblingskünstler:", artists)

    # Button für den Mix mit Machine Learning
    if st.button("Mix Up"):
        # Hier kommt die Logik für das Zusammenmischen der Songs
        st.write("Mixing up your preferences...")  # Placeholder für Machine Learning Logik

        # Beispielausgabe, die du später anpassen kannst
        st.write("Empfohlene Songs für dich könnten sein: ...")

if __name__ == "__main__":
    main()