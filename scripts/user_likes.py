import streamlit as st
from sklearn.linear_model import LogisticRegression
import pandas as pd

features = [
    "Danceability",
    "Energy",
    "Acousticness",
    "Valence",
    "Tempo",
    "Loudness",
]

df = pd.read_csv("../cleaned_dataset.csv")
songs = df.dropna(subset=features + ["Artist", "Track"]).reset_index(drop=True)
scaled_features = (songs[features] - songs[features].min()) / (
    songs[features].max() - songs[features].min()
)

mask = pd.Series(False, index=songs.index)

recs = st.session_state.get("recommendations")
saved = st.session_state.get("saved", [])

for artist, track in saved:
    mask |= (songs["Artist"].str.lower() == artist.lower()) & (songs["Track"].str.lower() == track.lower())

saved_songs_info = songs[mask][["Track"] + features]
st.dataframe(saved_songs_info)
if recs is None:
    st.info("Search for a song on the Recommender page first.")
else:
    recs_info = recs[["Artist", "Track"]].merge(songs, on=["Artist", "Track"])
    st.dataframe(recs_info)





