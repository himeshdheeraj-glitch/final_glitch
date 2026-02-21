import streamlit as st

@st.dialog("Modal")
def open_modal():
    with open("test_other.py", "w") as f:
        f.write('import streamlit as st\nst.write("Hello inside modal")\nif st.button("Click me inside modal"): st.write("Clicked!")')
    with open("test_other.py") as f:
        exec(f.read())

if st.button("Open Modal"):
    open_modal()
