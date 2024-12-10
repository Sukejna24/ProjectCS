import streamlit as st
import sqlite3
import pandas as pd
import bcrypt
import hashlib
from datetime import datetime
import os

def main():
    # Initialisation of Session-States, all important variables are checked if they exist in session_state. If not they are initialised
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    if 'show_legend' not in st.session_state:
        st.session_state.show_legend = False
    if 'expander_opened' not in st.session_state:
        st.session_state.expander_opened = False  # initialisation of expander_opened

    # creats 3 columns, both at the end are for the frame, to centralize the picture
    col1, col2, col3 = st.columns([1, 3, 1])

    # Import spotify logo
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Spotify.png", width=150)
    
    st.title("Track Finder")

    # Definition of the path of the actual script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    songs_dir = os.path.join(script_dir, "songs")

    # Ensure that "songs" directory exists
    if not os.path.exists(songs_dir):
        os.makedirs(songs_dir)
        
    # Reads the csv-file
    file_name_spotify_songs = os.path.join(script_dir, "spotify_songs.csv")
    df = pd.read_csv(file_name_spotify_songs)

    # Creation of the main database of the user 
    file_name_users = os.path.join(script_dir, "users.db")
    conn_users = sqlite3.connect(file_name_users)
    c_users = conn_users.cursor()
    c_users.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT, password TEXT)''')
    conn_users.commit()

    # Hash-function, creation and storing of the password 
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    # function that creates User-ID to new registrated Users
    def generate_user_id(username):
        timestamp = datetime.now().strftime("%H%M%S")  # User ID based on second, minute and hour of first registration
        data = f"{username}{timestamp}"
        user_hash = hashlib.md5(data.encode()).hexdigest()[:5]  # Shortens the hash to 5 characters
        return user_hash

    # Function to create the Users database and to import and apply songs
    def create_user_database(user_id):
        user_db_path = os.path.join(songs_dir, f"{user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)
        df.to_sql('user_songs', conn_user_db, if_exists='replace', index=False)
        cursor = conn_user_db.cursor()
        cursor.execute("DELETE FROM user_songs;")
        conn_user_db.commit()
        conn_user_db.close()

    # creation of the data base and saving a pandas dataframe into an SQL database
    def save_csv_to_database(df):
        songs_db_path = os.path.join(script_dir, "spotify_songs.db") #creates the file path SQL Database
        conn_songs_db = sqlite3.connect(songs_db_path)
        df.to_sql('spotify_songs', conn_songs_db, if_exists='replace', index=False)
        conn_songs_db.commit()
        conn_songs_db.close()

    # Registration for first time users
    def register_user(username, password):
        if user_exists(username):
            st.warning("Username already exists!")
        else:
            user_id = generate_user_id(username)
            hashed_password = hash_password(password)
            c_users.execute("INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", 
                            (user_id, username, hashed_password))
            conn_users.commit()

            # Create a customised user database, next time the User logs in, his username and password are saved
            create_user_database(user_id)

            st.success(f"Registration successful! Your user-ID is: {user_id}. Login now!")

    # Function checks whether user exists
    def user_exists(username):
        c_users.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c_users.fetchone()

    # Check login
    def login_user(username, password):
        c_users.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c_users.fetchone()
        if user and check_password(password, user[2]):
            st.session_state.user_id = user[0]  # user_id is saved in st.session_state
            return user[0]  # Returns the user_id
        return None
    
    # Access to the user's database (Personal Songs)
    def load_user_db():
        user_db_path = os.path.join(songs_dir, f"{st.session_state.user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)

        query_playlist_overview = """
        SELECT DISTINCT 
            playlist_name, 
            playlist_genre, 
            playlist_subgenre, 
            track_artist, 
            track_album_name, 
            track_name 
        FROM user_songs
        """

        user_songs_df_overview = pd.read_sql_query(query_playlist_overview, conn_user_db)
        conn_user_db.close()
        return user_songs_df_overview

    # Streamlit-application
    with st.sidebar:
        st.header("Login & Registration")

    # User chooses to log in or to registrate
    with st.sidebar:
        if not st.session_state.logged_in:
            option = st.selectbox("Choose an action:", ["Login", "Registration"])
    
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if option == "Registration":
                if st.button("Registration"):
                    register_user(username, password)
            elif option == "Login":
                if st.button("Login"):
                    user_id = login_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = user_id
                        st.success(f"Welcome, {username}!")
                    else:
                        st.error("Incorrect user name or password.")
        else:
            st.sidebar.success(f"Logged in as: {st.session_state.username}")
            st.sidebar.write(f"Your user-ID: {st.session_state.user_id}")
            st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": "", "user_id": "", "show_legend": False}))

    # Show user database after successful login (only a small part)
    if st.session_state.logged_in:
        st.header("Your personal songs")

        # # Access to the user's database
        user_db_path = os.path.join(songs_dir, f"{st.session_state.user_id}.db")
        conn_user_db = sqlite3.connect(user_db_path)        

        # Check if user_id is set in session state
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'default_user'  # Replace with your default user logic

        # Initial load
        user_songs_df_overview = load_user_db()

        # Display the data and add a refresh button
        if st.button("Refresh"):
            user_songs_df_overview = load_user_db()
            st.success("Database refreshed!")

        st.dataframe(user_songs_df_overview, use_container_width=True, height=200)

        save_csv_to_database(df)
        songs_db_path = os.path.join(script_dir, "spotify_songs.db")
        conn_songs_db = sqlite3.connect(songs_db_path)

        with st.expander("Search", expanded=st.session_state.expander_opened):

            # Dynamische Suchoption hinzufügen
            search_column_1 = st.selectbox("Search for:", ["track_artist", "track_name", "playlist_name"], key="search_column_1")
            search_query_1 = st.text_input(f"Please insert {search_column_1}:", key="search_query_1")

            # Show results of the search
            if search_query_1:
                query_playlist_search_1 = f"""SELECT DISTINCT playlist_name, track_artist, track_name, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms FROM spotify_songs WHERE {search_column_1} LIKE ?"""
                spotify_songs_df_search_1 = pd.read_sql_query(query_playlist_search_1, conn_songs_db, params=(f"%{search_query_1}%",))
                if not spotify_songs_df_search_1.empty:
                    # Shwo results if songs were found
                    st.dataframe(spotify_songs_df_search_1, use_container_width=True, height=400)

                    # Show legend button after successful search
                    if st.button("Explanation of the Audio Features", key="audio_features"):
                        st.session_state.show_legend = not st.session_state.show_legend

                    # Show description if legend is activated
                    if st.session_state.show_legend:
                        st.markdown("""
                        ### Danceability
                        Indicates how suitable a track is for dancing. It is based on a combination of elements such as tempo, rhythm stability, beat strength and overall rhythm.   
                        **Scale:** 0.0 to 1.0 (higher value = more danceable).

                        ### Energy
                        Indicates the level of intensity and activity of a track. Tracks with high energy have a fast tempo, a strong beat and loud instruments.    
                        **Scale:** 0.0 to 1.0 (higher value = more energetic).

                        ### Valence
                        Indicates the musical positivity of a track. Tracks with a high valence sound cheerful, happy and euphoric.   
                        **Scale:** 0.0 to 1.0 (higher value = more positive).

                        ### Tempo
                        The estimated tempo of the track in beats per minute (BPM).    
                        **Unit:** Beats per minute (BPM).

                        ### Speechiness
                        Indicates the proportion of spoken words in a track. High values indicate more spoken content (e.g. podcasts, audiobooks, rap).  
                        **Scale:** 
                        - Values above 0.66: Probably pure spoken content.
                        - 0.33-0.66: Mixture of music and spoken content.
                        - Below 0.33: Mainly music.

                        ### Liveness
                        Indicates the probability that the track was performed in front of a live audience. 
                        **Scale:** 0.0 to 1.0 (higher value = more live character). Values above 0.8 indicate live recordings.

                        ### Instrumentalness
                        Estimates how instrumental a track is. Higher values indicate that the track contains little or no vocals.
                        **Scale:** 0.0 to 1.0 (values close to 1.0 indicate pure instrumental music).

                        ### Acousticness
                        Indicates how acoustic a track is.   
                        **Scale:** 0.0 to 1.0 (higher value = more acoustic).

                        ### Key
                        Specifies the tonality of the track.  
                        **Values:** 
                        - 0 = C
                        - 1 = C#
                        - 2 = D
                        - …
                        - 11 = B
                        - -1: No tonality recognisable.

                        ### Mode
                        Indicates whether a track is in major (1) or minor (0).

                        ### Loudness
                        Indicates the average volume of the track in decibels (dB). 
                        **Unit:** Decibel (dB).

                        ### Duration_ms
                        The length of the track in milliseconds.   
                        **Unit:** Milliseconds (ms).

                        ### Time Signature
                        Indicates the estimated number of beats per bar.  
                        **Values:**
                        - 3 = 3/4-Takt (Walzer)
                        - 4 = 4/4-Takt (Standard)""")
                else:
                    # Display message if no hits are available
                    st.warning("No match found. Try another entry.")

        # Filter by audio features
        query_playlist_filter = """SELECT DISTINCT track_artist, track_name, tempo, valence, energy, danceability FROM spotify_songs"""
        spotify_songs_df_filter = pd.read_sql_query(query_playlist_filter, conn_songs_db)

        with st.expander("Filter by audio-features", expanded=st.session_state.expander_opened):
            # Tempo-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Slow tempo")
            with col2:
                tempo_range = st.slider("Tempo", min_value=0.0, max_value=240.0, value=(0.0, 240.0), step=10.0, label_visibility="collapsed")
            with col3:
             st.write("fast tempo")

            # Valence-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Sad")
            with col2:
                valence_range = st.slider("Valence", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
            with col3:
                st.write("Happy")

            # Energy-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("Low energy")
            with col2:
                energy_range = st.slider("Energy", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
            with col3:
                st.write("High energie")

            # Danceability-Filter
            col1, col2, col3 = st.columns([2, 6, 2])
            with col1:
                st.write("less danceable")
            with col2:
                danceability_range = st.slider("Danceability", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.1, label_visibility="collapsed")
            with col3:
                st.write("more danceable")

            #  Select songs according to the filters
            filtered_songs = spotify_songs_df_filter[
                (spotify_songs_df_filter['tempo'] >= tempo_range[0]) & (spotify_songs_df_filter['tempo'] <= tempo_range[1]) &
                (spotify_songs_df_filter['valence'] >= valence_range[0]) & (spotify_songs_df_filter['valence'] <= valence_range[1]) &
                (spotify_songs_df_filter['energy'] >= energy_range[0]) & (spotify_songs_df_filter['energy'] <= energy_range[1]) &
                (spotify_songs_df_filter['danceability'] >= danceability_range[0]) & (spotify_songs_df_filter['danceability'] <= danceability_range[1])
                ]

            # Show filtered songs
            st.subheader("Filtered songs")
            if not filtered_songs.empty:
                st.dataframe(filtered_songs, use_container_width=True, height=400)

                # Show legend 
                if st.button("Description of audio features", key="audio_features_duplicate"):
                    st.session_state.show_legend = not st.session_state.show_legend

                # Show descriptions when "Legend" is activated
                if st.session_state.show_legend:
                    st.markdown("""
                    ### Tempo
                    The estimated tempo of the track in beats per minute (BPM).    
                    **Unit:** Beats per minute (BPM).
                        
                    ### Valence
                    Indicates the musical positivity of a track. Tracks with a high valence sound cheerful, happy and euphoric.  
                    **Scale:** 0.0 to 1.0 (higher value = more positive).
                        
                    ### Danceability
                    Indicates how suitable a track is for dancing. Based on a combination of elements such as tempo, rhythm stability, beat strength and overall rhythm.   
                    **Scale:** 0.0 to 1.0 (higher value = more danceable).

                    ### Energy
                    Indicates the level of intensity and activity of a track. Tracks with high energy have a fast tempo, a strong beat and loud instruments.  
                    **Scale:** 0.0 to 1.0 (higher value = more energetic).

                    ### Danceability
                    How danceable the track is. Higher value = more suitable for dancing.
                """)

            else:
                st.warning("No songs match the filter criteria.")

        # CSS for customising the design
        st.markdown("""
            <style>
            .song-list {
                font-size: 14px !important;
                line-height: 1.6 !important;
                display: flex;
                justify-content: space-between;
            }
            .remove-button {
                font-size: 10px !important;
                padding: 1px 3px !important;
                color: red !important;
                background: none !important;
                border: none !important;
                cursor: pointer !important;
            }
            .song-count {
                font-size: 16px !important;
                font-weight: bold !important;
                margin-bottom: 10px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.expander("Mix Up", expanded=st.session_state.expander_opened):
            # Add dynamic search option
            search_column_2 = st.selectbox("Search for:", ["track_artist", "track_name"], key="search_column_2")
            search_query_2 = st.text_input(f"Please insert {search_column_2}:", key="search_query_2")

            # Save basket in the session
            if "cart" not in st.session_state:
                st.session_state.cart = []

            # Display the number of songs in the basket
            if st.session_state.cart:
                st.markdown(f"<div class='song-count'>Choosen songs: {len(st.session_state.cart)}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='song-count'>Your basket is empty.</div>", unsafe_allow_html=True)

            # Show search results
            if search_query_2:
                # Query tracks by search term
                query_playlist_search_2 = f"""
                SELECT DISTINCT track_artist, track_name, danceability, energy, key, loudness, mode, speechiness, acousticness, 
                instrumentalness, liveness, valence, tempo, duration_ms 
                FROM spotify_songs WHERE {search_column_2} LIKE ?
                """
                spotify_songs_df_search_2 = pd.read_sql_query(query_playlist_search_2, conn_songs_db, params=(f"%{search_query_2}%",))

                if not spotify_songs_df_search_2.empty:
                    st.write("Select songs to add them to the basket:")
                    
                    for i, row in spotify_songs_df_search_2.iterrows():
                        # Generate a unique key for the checkbox
                        checkbox_key = f"checkbox_{i}_{row['track_name']}_{row['track_artist']}"
                        is_checked = row.to_dict() in st.session_state.cart
                        checked = st.checkbox(
                            f"{row['track_name']} von {row['track_artist']}", 
                            value=is_checked, 
                            key=checkbox_key
                        )
                        if checked and not is_checked:
                            # Add to basket
                            st.session_state.cart.append(row.to_dict())
                        elif not checked and is_checked:
                            # Delete from basket
                            st.session_state.cart.remove(row.to_dict())
                else:
                    # Display message if no hits are found
                    st.warning("No match found. Try another entry.")

            # Show basket (always visible)
            if st.session_state.cart:
                st.write("Your basket:")
                for index, track in enumerate(st.session_state.cart):
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"<div class='song-list'><b>{track['track_name']}</b> - <i>{track['track_artist']}</i></div>", unsafe_allow_html=True)
                    with col2:
                        if st.button(f"❌", key=f"remove_cart_{index}", help="Löschen"):
                            st.session_state.cart.pop(index)
                            st.experimental_rerun()  # Reload page to reflect changes

            # Initialize session_state
            if "similar_songs_generated" not in st.session_state:
                st.session_state.similar_songs_generated = False

            if "save_playlist_clicked" not in st.session_state:
                st.session_state.save_playlist_clicked = False

            # Initialize empty dataframe
            if "user_songs_df_similar" not in st.session_state:
                st.session_state.user_songs_df_similar = pd.DataFrame()  # Fallback for later access

            # Show button only if there are 20 songs in the basket
            if len(st.session_state.cart) >= 5:
                if st.button("Find similar songs"):
                    # Create DataFrame from the basket
                    selected_tracks_df = pd.DataFrame(st.session_state.cart)

                    # Use machine learning model to find similar songs
                    from sklearn.neighbors import NearestNeighbors
                    import numpy as np

                    # Prepare data for Machine Learning
                    feature_columns = [
                        "danceability", "energy", "key", "loudness", "mode",
                        "speechiness", "acousticness", "instrumentalness", "liveness",
                        "valence", "tempo", "duration_ms"
                    ]

                    # Fit model on all songs
                    query_playlist_all = """
                    SELECT * FROM spotify_songs
                    """
                    spotify_songs_df_all = pd.read_sql_query(query_playlist_all, conn_songs_db)
                    knn = NearestNeighbors(n_neighbors=300, metric="euclidean")
                    knn.fit(spotify_songs_df_all[feature_columns])

                    # Search for similar songs based on the selected tracks
                    selected_features = selected_tracks_df[feature_columns].values
                    distances, indices = knn.kneighbors(selected_features)

                    # Collect results
                    user_songs_df_similar = spotify_songs_df_all.iloc[np.unique(indices.flatten())]

                    # Save into st.session_state
                    st.session_state.user_songs_df_similar = user_songs_df_similar

                    # Add playlist metadata
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    user_songs_df_similar["playlist_name"] = f"Mix Up {timestamp}"
                    user_songs_df_similar["playlist_genre"] = f"Mix Up {timestamp}"
                    user_songs_df_similar["playlist_subgenre"] = f"Mix Up {timestamp}"
                    user_songs_df_similar["playlist_id"] = timestamp

                    # Show results
                    st.subheader("Similar songs")
                    st.dataframe(user_songs_df_similar, use_container_width=True, height=400)

                    # refresh state
                    st.session_state.similar_songs_generated = True
                    st.session_state.save_playlist_clicked = False

            # Save button is shown if songs have been generated 
            if st.session_state.similar_songs_generated and not st.session_state.save_playlist_clicked:
                st.write("Do you like the songs? Save now!")
                if st.button("Save Playlist"):
                    # Assure that the datafram is not empty
                    if not st.session_state.user_songs_df_similar.empty:
                        try:
                            user_db_path = os.path.join(songs_dir, f"{st.session_state.user_id}.db")
                            conn_user_db = sqlite3.connect(user_db_path)
                            st.session_state.user_songs_df_similar.to_sql(
                                'user_songs', conn_user_db, if_exists='append', index=False
                            )
                            conn_user_db.commit()
                            conn_user_db.close()

                            st.success("The Playlist has been saved successfully!")
                            st.session_state.similar_songs_generated = False
                        except Exception as e:
                            st.error(f"Error when saving the playlist: {e}")
                    else:
                        st.error("No songs to save available!")

        conn_songs_db.close() #close connection

if __name__ == "__main__":
    main()