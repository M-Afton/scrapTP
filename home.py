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
st.divider()
st.sidebar.markdown("""
                    Le site <a href="https://noveldeglace.com/nouvelles/" style="color: yellow; text-decoration: none;">noveldeglace.com</a> est un site qui regroupe des traductions benevole de romans japonais en français.
                    """, unsafe_allow_html=True)
st.sidebar.markdown("""
                    <a href="https://m-afton-scraptp-home-h4nsrx.streamlit.app/openai" style="color: yellow; text-decoration: none;">lien vers le site deployer</a>
                    """, unsafe_allow_html=True)

pages = st.slider('Nombre de pages', 1, 201 , 1)#il ya 1197 pages mais je ne peux pas toutes les scraper car cela prendrait trop de temps et en 201 pages on a deja 2000 lignes

if st.button('Lancer le Scraping'):
    with st.spinner('Chargement en cours...'):

        progress_bar = st.progress(0)

        results = scraping_and_store(pages, progress_bar)  # Passer le nombre de pages sélectionné

        df = pd.DataFrame(results)

        st.write(df)

        for result in results:
            # Display each result in a list format with images
            st.image(result['image'], caption=result['title'], use_column_width=True)
            st.write(f"**Chapitre:** {result['date']}")
            st.write(f"**Lien:** [{result['title']}]({result['link']})")
            st.write(f"**message:** {result['categorie']}")
            st.write("----------------------------")


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
