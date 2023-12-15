import streamlit as st
import pandas as pd
from fonction import scraping_and_store
import base64

st.set_page_config(
    page_title="Streamlit App",
    page_icon="🧊",
    layout="wide",
)

st.title('LN scraper')
st.markdown("""
Cette application scrape les données du site [noveldeglace.com](https://noveldeglace.com/nouvelles/) et les stocke dans une base de données SQLite.
* **Librairies Python:** pandas, streamlit, BeautifulSoup, requests, sqlalchemy
* **j'ai choisi d'utiliser beautifulsoup car c'est la librairie simple d'utilisation et dans mon scraping je n'ai pas besoin d'intéragir avec le site web.**
""")

st.sidebar.title("LHERBIER Clément")

pages = st.slider('Nombre de pages', 1, 201 , 1)#il ya 1197 pages mais je ne peux pas toutes les scraper car cela prendrait trop de temps et en 201 pages on a deja 2000 lignes

if st.button('Lancer le Scraping'):
    with st.spinner('Chargement en cours...'):

        results = scraping_and_store(pages)  # Passer le nombre de pages sélectionné

        df = pd.DataFrame(results)

        st.write(df)

        file_name = 'result.csv'
        st.success('Scraping terminé !')
        st.download_button(
            label="Télécharger les données",
            data=df.to_csv().encode('utf-8'),
            file_name=file_name,
            mime='text/csv'
        )

    st.snow()
    
    st.toast('Scraping terminé !', icon='📖')