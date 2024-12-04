import streamlit as st

def main():

        st.markdown("""
    <style>
        /* Hintergrundfarbe der gesamten App */
        .stApp { background-color: #121212; }

        /* Sidebar */
        .sidebar .sidebar-content { background-color: #121212; color: black; }
        .sidebar .sidebar-header h1, 
        .sidebar .sidebar-header h2, 
        .sidebar .sidebar-header h3, 
        .sidebar .stMarkdown { color: black !important; }

        /* Schriftfarbe der Hauptinhalte */
        .stMarkdown, 
        .stTitle, 
        .stHeader, 
        .stSubheader, 
        .stText, 
        .stTextinput, 
        .stTextarea, 
        .stCheckbox, 
        .stRadio, 
        .stButton, 
        .stSelectbox, 
        .stMultiselect, 
        .stSlider, 
        .stCode { color: white !important; }

        /* Buttons */
        .stButton > button {
            background-color: #1db954; 
            color: white; 
            font-size: 16px; 
            padding: 10px; 
            border-radius: 5px; 
            border: none;
        }
        .stButton > button:hover { 
            background-color: #1ed760;
        }

        /* Slider Anpassungen */
        .stSlider > div { color: white !important; }

        /* Multiselect und Dropdown */
        .stSelectbox select, 
        .stMultiselect select, 
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #1ed760; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            padding: 8px;
        }

        /* Ladebalken */
        .stProgress > div > div { background-color: #1ed760 !important; }
    </style>
""", unsafe_allow_html=True)
        
    st.title("Melody Match")
    st.write("Willkommen bei Melody Match! Wähle deine Musikpräferenzen.")

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
