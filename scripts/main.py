import streamlit as st

home = st.Page("similar_songs_app.py", title="Recommender")
about = st.Page("about.py", title="About")

pg = st.navigation([home, about])
pg.run()