import streamlit as st
from sqlalchemy import text

conn = st.connection("my_db", type="sql", url="sqlite:///my_database.db")

df = conn.query(
    "SELECT Artist, Track FROM songs WHERE username = :u",
    params={"u": st.session_state["username"]},
    ttl=0,
)
st.markdown("# Saved Songs✅", anchors=False)

if df.empty:
    st.subheader("No Songs 😔", anchor=False)
else:
    st.subheader(f"You have {len(df)} songs saved.", anchor=False)
    user_select = st.dataframe(df, hide_index=True,on_select="rerun", selection_mode="multi-row")
    rows = user_select.selection.rows
    if st.button("Remove Selected Songs"):
        with conn.session as s:
            for num in rows:
                song = df.iloc[num]
                s.execute(
                    text("DELETE FROM songs WHERE Artist = :artist AND Track = :track AND username= :u"),
                    {"artist": song["Artist"], "track": song["Track"], "u": st.session_state["username"]}
                )
            s.commit()
        st.rerun()

if st.button("Find Similar Songs"):
    st.switch_page("similar_songs_app.py")


