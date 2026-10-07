import streamlit as st

home = st.Page("similar_songs_app.py", title="Recommender")
about = st.Page("about.py", title="About")
saved_songs = st.Page("saved_songs.py", title="Saved Songs")

if "saved" not in st.session_state:
    st.session_state["saved"] = []

pg = st.navigation([home, saved_songs, about])
pg.run()