import streamlit as st
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, suggestion TEXT)''')
conn.commit()

st.markdown("# Landing page 🎈")
st.sidebar.markdown("# Landing page 🎈")

st.write("Sign up for demo of [placeholder]")
st.write("We are working on a new product that will help you with [placeholder].")
name = st.text_input("Name")
email = st.text_input("Email")
st.write("Please put in at least one suggestion/feature proposal for the app that you would like to see.")
suggestion = st.text_area("Suggestion")
if(st.button("Submit")):
    if name and email and suggestion:
        c.execute("INSERT INTO users (name, email, suggestion) VALUES (?, ?, ?)", (name, email, suggestion))
        conn.commit()
        st.success("Thank you for your feedback!")
    else:
        st.error("Please fill in all fields.")

def authenticate():
    if("authenticate" in st.session_state and st.session_state["authenticate"] == True):
        st.button("Logout", key="logout")
        if(st.session_state["logout"]):
            st.session_state["authenticate"] = False
            st.session_state["username"] = None
            st.session_state["password"] = None
            st.rerun()
        return True
    else:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        if st.button("Login"):
            # Dummy authentication logic
            if st.session_state["username"] == "admin" and st.session_state["password"] == "password":
                st.session_state["authenticate"] = True
                # st.session_state["username"] = st.session_state["username"]
                st.rerun()
                return True
            else:
                st.error("Invalid credentials")
    return False
    
with st.sidebar:
    st.markdown("# Login 🔑")
    authed = authenticate()
    if(authed):
        st.success("Logged in successfully")
