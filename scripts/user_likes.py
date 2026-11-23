import streamlit as st
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

conn = st.connection("my_db", type="sql", url="sqlite:///my_database.db")
st.markdown("# User Likes 📈", anchors=False)
features = [
    "Danceability",
    "Energy",
    "Acousticness",
    "Valence",
    "Tempo",
    "Loudness",
    "Speechiness",
    "Instrumentalness",
    "Liveness"
]

df = pd.read_csv("../cleaned_dataset.csv")
songs = df.dropna(subset=features + ["Artist", "Track"]).reset_index(drop=True)

mask = pd.Series(False, index=songs.index)

recs = st.session_state.get("recommendations")

saved_df = conn.query("SELECT Artist, Track FROM songs WHERE username = :u",params={"u": st.session_state["username"]}, ttl=0)
saved = list(saved_df.itertuples(index=False, name=None))

for artist, track in saved:
    mask |= (songs["Artist"].str.lower() == artist.lower()) & (songs["Track"].str.lower() == track.lower())

saved_songs_info = songs[mask][["Artist","Track"] + features]

st.subheader("Saved Songs")
st.dataframe(saved_songs_info)

if len(saved_songs_info) < 6:
    st.info("Not enough songs to compare. Add more!")
    st.stop()

x_train_table, x_test_table = train_test_split(saved_songs_info, test_size=0.2, random_state=42)

scaler = StandardScaler().fit(songs[features])

svm_results = []
random_results = []

for seed in range(20):
    x_train_table, x_test_table = train_test_split(saved_songs_info, test_size=0.2, random_state=seed)
    X_saved = scaler.transform(x_train_table[features])

    model = OneClassSVM(kernel="rbf", nu=0.1).fit(X_saved)

    candidates = songs.drop(index=x_train_table.index)
    candidates["score"] = model.decision_function(scaler.transform(candidates[features]))
    candidates["rank"] = candidates["score"].rank(ascending=False)
    if seed == 0:
        candidates.loc[x_test_table.index, ["Artist", "Track", "rank"]]
    percentiles = (1-(candidates["rank"]/len(candidates))).where(candidates.index.isin(x_test_table.index)).dropna()
    svm_results.append(percentiles.mean())

    candidates["random_score"] = np.random.default_rng(seed).random(len(candidates))
    candidates_rank = candidates["random_score"].rank(ascending=False)
    random_percentiles = (1-(candidates_rank / len(candidates))).where(candidates.index.isin(x_test_table.index)).dropna()
    random_results.append(random_percentiles.mean())

results = pd.DataFrame({"model": ["SVM", "Random"], "percentile": [np.mean(svm_results), np.mean(random_results)], "Standard Deviation": [np.std(svm_results), np.std(random_results)]})
st.dataframe(results)




