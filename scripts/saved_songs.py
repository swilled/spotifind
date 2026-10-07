import streamlit as st
import pandas as pd

st.markdown("# Saved Songs", anchors=False)

saved = st.session_state.get("saved", [])

if not saved:
    st.subheader("No Songs 😔", anchor=False)
    st.subheader("Add some!", anchor=False)
else:
    st.subheader(f"You have {len(saved)} songs saved. Add more?", anchor=False)

    table = pd.DataFrame(saved, columns=["Artist", "Track"])

    st.dataframe(table)

if st.button("Find Similar Songs"):
    st.switch_page("similar_songs_app.py")


