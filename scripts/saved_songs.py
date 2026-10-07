import streamlit as st
import pandas as pd

st.markdown("# Saved Songs", anchors=False)

saved = st.session_state.get("saved", [])

table = pd.DataFrame(saved, columns=["Artist", "Track"])

st.dataframe(table)


