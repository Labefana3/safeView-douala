import streamlit as st
from PIL import Image

st.set_page_config(page_title="SafeView Douala", layout="wide")
st.title("SafeView - Surveillance Boutique Douala")

st.sidebar.title("Menu SafeView")
menu = st.sidebar.selectbox("Choisir une page", ["Camera Live", "Detection", "A Propos"])

if menu == "Camera Live":
    st.subheader("Vue Camera")
    st.info("Ici tu verras ta camera en direct")
    file = st.file_uploader("Teste avec une photo de ta boutique", type=["jpg","png","jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, use_column_width=True)

elif menu == "Detection":
    st.subheader("Detection de mouvement")
    st.success("Systeme pret")

else:
    st.subheader("A Propos")
    st.write("SafeView Douala v1.0 - Cree par Labefana3 pour Akwa")
    st.write("Version solide qui ne meurt jamais.")

st.sidebar.success("Statut: En ligne")
