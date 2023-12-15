# openai.py
import streamlit as st
from IPython.display import Image
import requests
import base64  # Importez la bibliothèque base64

# Generate image from text
import openai

# Définissez votre clé API OpenAI
openai.api_key = st.secrets["API_KEY"]

def generate_and_display_image(prompt):
    # Generate image from text
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']

    # Afficher l'image
    st.image(image_url, caption="Generated Image", use_column_width=True)

def main():
    st.title("Génération d'image avec OpenAI")

    # Input pour saisir le prompt
    prompt = st.text_input("Entrez le prompt pour générer l'image")

    # Bouton pour générer et afficher l'image
    if st.button("Générer et Afficher l'image"):
        if not prompt:
            st.warning("Veuillez saisir un prompt.")
        else:
            generate_and_display_image(prompt)


st.sidebar.title("LHERBIER Clément")
st.sidebar.markdown("""
    Le site <a href="https://noveldeglace.com/nouvelles/" style="color: white; text-decoration: none;">noveldeglace.com</a> est un site qui regroupe des traductions benevole de romans japonais en français.
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
                    <a href="https://m-afton-scraptp-home-h4nsrx.streamlit.app/openai" style="color: white; text-decoration: none;">lien vers le site deployer</a>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
