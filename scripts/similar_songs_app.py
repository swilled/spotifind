import streamlit as st
from similar_songs_demo import recommend_songs, songs
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text
import random

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

conn = st.connection("my_db", type="sql", url="sqlite:///my_database.db")

count_df = conn.query(
    "SELECT COUNT(*) AS n FROM songs WHERE username = :u",
    params={"u": st.session_state["username"]},
    ttl=0,
)
random_greetings = ["What's up, ", "Welcome, ", "Glad you're back, ", "Ready to jam, ", "Find your next favorite, "]
count = count_df["n"][0]

random_greet = random.choice(random_greetings)
st.write(f"# {random_greet}{st.session_state['username']}!!")


st.image("../static/spotifind_logo_neutral.png")

artists = sorted(songs["Artist"].drop_duplicates())
st.markdown("### Artist", anchors=False)
artist_name = st.selectbox("Artist", label_visibility="collapsed", options=artists, index=None, placeholder="select an artist")

if artist_name:
    artist_songs = songs[songs["Artist"] == artist_name]
    tracks = sorted(artist_songs["Track"].drop_duplicates())
    st.markdown("### Song", anchors=False)
    track_name = st.selectbox("Song", label_visibility="collapsed", options=tracks, index=None, placeholder="select a song")

    if track_name:
        song_slider = st.slider("Number of similar songs", min_value=1, max_value=10, value=5)
        st.markdown("### Recommendations", anchors=False)

        recommendations = recommend_songs(artist_name, track_name, number=song_slider)
        st.session_state["recommendations"] = recommendations

        # recommendations + their audio features (same order as recommendations)
        shown = recommendations[["Artist", "Track", "match_percentage"]].merge(
            songs[["Artist", "Track"] + features].drop_duplicates(["Artist", "Track"]),
            on=["Artist", "Track"], how="left",
        )

        # saved songs -> their features
        saved_df = conn.query(
            "SELECT Artist, Track FROM songs WHERE username = :u",
            params={"u": st.session_state["username"]},
            ttl=0,
        )
        saved_info = songs.merge(saved_df, on=["Artist", "Track"])[features]

        if saved_info.empty:
            shown["score"] = None
        else:
            scaler = StandardScaler().fit(songs[features])
            model = OneClassSVM(kernel="rbf", nu=0.1).fit(scaler.transform(saved_info))
            shown["score"] = model.decision_function(scaler.transform(shown[features]))

        user_data = st.dataframe(
            shown[["Artist", "Track", "match_percentage", "score"]],
            hide_index=True, on_select="rerun", selection_mode="multi-row",
        )
        rows = user_data.selection.rows

        if st.button("Save selected"):
            with conn.session as s:
                for num in rows:
                    song = shown.iloc[num]
                    s.execute(
                        text("INSERT OR IGNORE INTO songs (username, Artist, Track) VALUES (:u, :artist, :track)"),
                        {"u": st.session_state["username"], "artist": song["Artist"], "track": song["Track"]},
                    )
                s.commit()
            st.switch_page("saved_songs.py")

