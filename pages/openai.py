# openai.py
import streamlit as st
from IPython.display import Image
import requests

# Generate image from text
import openai

# Définissez votre clé API OpenAI
openai.api_key = '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'

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

    # Télécharger l'image au clic d'un bouton
    if st.button("Télécharger l'image"):
        download_image(image_url, 'img.png')
        st.success("Image téléchargée avec succès!")

def download_image(url_img, img_name):
    img = requests.get(url_img).content
    with open(img_name, 'wb') as handler:
        handler.write(img)

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

if __name__ == "__main__":
    main()
