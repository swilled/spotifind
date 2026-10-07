import streamlit as st
import pandas as pd

st.markdown("# Saved Songs", anchors=False)

saved = st.session_state.get("saved", [])

if not saved:
    st.page_link("similar_songs_app.py", label="Add New Songs :)")
else:
    table = pd.DataFrame(saved, columns=["Artist", "Track"])

    st.dataframe(table)

if st.button("Find Similar Songs"):
    st.switch_page("similar_songs_app.py")


