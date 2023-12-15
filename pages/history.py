import streamlit as st
import pandas as pd
from fonction import DataBase, db 

def show_history():
    st.title('Historique des Scrapings')

    # Initialize the database
    database = DataBase(name_database='MaBaseDeDonnees')

    # Define the table structure
    table_structure = {
        'id': db.Integer,
        'title': db.String,
        'date': db.String,
        'link': db.String,
        'image': db.String,
        'categorie': db.String
    }

    # Create the table (if not exists)
    database.create_table('Tableau1', **table_structure)

    # Read the data from the database
    historical_data = database.select_table('Tableau1')

    # Display historical data in a DataFrame
    df_historical = pd.DataFrame(historical_data)
    st.write(df_historical)


st.sidebar.title("LHERBIER Clément")
st.sidebar.markdown("""
    Le site <a href="https://noveldeglace.com/nouvelles/" style="color: yellow; text-decoration: none;">noveldeglace.com</a> est un site qui regroupe des traductions benevole de romans japonais en français.
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
                    <a href="https://m-afton-scraptp-home-h4nsrx.streamlit.app/openai" style="color: yellow; text-decoration: none;">lien vers le site deployer</a>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_history()
