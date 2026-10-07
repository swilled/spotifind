
import streamlit as st

from similar_songs_demo import recommend_songs, songs

st.image("../static/spotifind_logo.png")
artists = sorted(songs["Artist"].drop_duplicates())
st.markdown("### Artist", anchors=False)
artist_name = st.selectbox("Artist", label_visibility="collapsed", options=artists, index=None, placeholder="select an artist")

if artist_name:
    artist_songs = songs[songs["Artist"] == artist_name]
    tracks = sorted(artist_songs["Track"].drop_duplicates())
    st.markdown("### Song", anchors=False)
    track_name = st.selectbox("Song",label_visibility="collapsed", options=tracks, index=None, placeholder="select a song")

    if track_name:
        song_slider = st.slider("Number of similar songs", min_value=1, max_value=10, value=5)
        st.markdown("### Recommendations", anchors=False)

        if song_slider:
            recommendations = recommend_songs(artist_name, track_name, number= song_slider)
            user_data = st.dataframe(recommendations[["Artist", "Track", "match_percentage"]], hide_index=True, on_select="rerun", selection_mode="multi-row")
            # st.write(user_data)
            rows = user_data.selection.rows
            shown = recommendations[["Artist", "Track", "match_percentage"]]
            if st.button("Save selected"):
                for num in rows:
                    song = shown.iloc[num]
                    pair = (song['Artist'], song['Track'])
                    if pair not in st.session_state['saved']:
                        st.session_state['saved'].append((song['Artist'], song['Track']))