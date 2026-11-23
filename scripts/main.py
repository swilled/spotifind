import streamlit as st
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

conn = st.connection("my_db", type="sql", url="sqlite:///my_database.db")

with conn.session as s:
    s.execute(text("""
        CREATE TABLE IF NOT EXISTS songs (
            username TEXT NOT NULL,
            Artist TEXT,
            Track TEXT,
            UNIQUE (username, Artist, Track)
        )
    """))
    s.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """))
    s.commit()

if "username" not in st.session_state:
    tab_login, tab_signup = st.tabs(["Log in", "Sign up"])
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Name ", placeholder="Type your name...", key="login_user")
            password = st.text_input("Password ", placeholder="Type your password...", key="login_pass",type="password")
            login = st.form_submit_button("Log in")
            if login:
                name = username.strip().lower()
                result = conn.query("SELECT password_hash FROM users WHERE username = :u", params={"u": name}, ttl=0)
                if result.empty or not check_password_hash(result["password_hash"][0], password):
                    st.error("Wrong username or password")
                else:
                    st.session_state["username"] = name
                    st.rerun()
    with tab_signup:
        with st.form("signup_form"):
            new_username = st.text_input("Name ", placeholder="Type your name...", key="signup_user")
            password = st.text_input("Password ", placeholder="Type your password...", key="signup_pass", type="password")
            enter = st.form_submit_button("Enter")
            if enter and (not new_username.strip() or not password.strip()):
                if not new_username.strip():
                    st.warning("⚠️ Please type in a name!!")
                if not password.strip():
                    st.warning("⚠️ Please type in a password!!")
            elif enter and new_username.strip() and password.strip():
                name = new_username.strip().lower()
                existing = conn.query(f"SELECT username FROM users WHERE username = :u", params={"u": name}, ttl=0)
                if not existing.empty:
                    st.error("That name is already taken.")
                else:
                    hash_password = generate_password_hash(password, salt_length=8, method='pbkdf2:sha256')
                    with conn.session as s:
                        s.execute(
                            text("INSERT OR IGNORE INTO users (username, password_hash) VALUES (:u, :p)"),
                            {"u": name, "p": hash_password},
                        )
                        s.commit()
                    st.session_state["username"] = name
                    st.rerun()
            st.stop()

st.sidebar.button("Logout", on_click=st.session_state.clear)
home = st.Page("similar_songs_app.py", title="Recommender", icon="🎧")
about = st.Page("about.py", title="About", icon="🤔")
saved_songs = st.Page("saved_songs.py", title="Saved Songs", icon="✅")
user_likes = st.Page("user_likes.py", title="User Likes", icon="📈")

pg = st.navigation([home, saved_songs, about, user_likes])
pg.run()