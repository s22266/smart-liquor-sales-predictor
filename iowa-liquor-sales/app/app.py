import streamlit as st
import requests
import pandas as pd
from functions import groupBy
import yaml
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Wskazanie ścieżki do katalogu głównego projektu Kedro
# Zakładając, że uruchamiasz Streamlit z tego samego katalogu
project_path = Path.cwd()

# Bootstrap projektu Kedro
bootstrap_project(project_path)

# Funkcja do uruchomienia Kedro pipeline
def run_kedro_pipeline():
    with KedroSession.create(project_path=project_path) as session:
        return session.run(pipeline_name="model_prediction")  # Uruchamia domyślny pipeline

page_bg_img = """
<style>
[data-testid="stAppViewContainer"],
[data-testid="stSidebarContent"]{
    background-image: linear-gradient(rgba(255,255,240,0), rgba(255,228,196,1));
}
</style>
"""

def main():
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("Sprzedaż alkholu wysokoprocentowego w stanie Iowa")

    tabs = ["Informacje ogólne", "Algorytm Facebooka", "Algorytm przewidywania sprzedaży"]
    choice = st.sidebar.selectbox("Wybierz stronę", tabs)

    if choice == "Informacje ogólne":
        informacjeOgolne()
    elif choice == "Algorytm Facebooka":
        facebookAlgorithm()
    elif choice == "Algorytm przewidywania sprzedaży":
        algorytmPrzewidywaniaSprzedaży()

def algorytmPrzewidywaniaSprzedaży():
    st.header("Algorytm przewidywania sprzedaży")

    # Wczytanie danych z pliku CSV do DataFrame
    countydf = pd.read_csv('./app/distinct_county.csv')
    selected_county = st.selectbox("Wybierz Chrabstwo", countydf['county'])

    alcoholTypes = ['Rum', 'Vodka', 'Tequila', 'Whiskies', 'schnapps']
    selected_liquor = st.selectbox("Wybierz Alkohol", alcoholTypes)

    # Wybór daty początkowej i końcowej
    start_date = st.date_input("Wybierz datę początkową", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Wybierz datę końcową", value=pd.to_datetime("2023-12-31"))

    if st.button("Predict"):
        with open('./conf/base/parameters_model_prediction.yml', 'w') as file:
            yaml.dump({
                'county_name': selected_county,
                'category_name': selected_liquor,
                'start_month': start_date.month,
                'start_year': start_date.year,
                'end_year': end_date.year,
                'end_month': end_date.month,
            }, file)
        # Uruchamianie modelu i generowanie wykresu
        result_df = run_kedro_pipeline()

        result_df = result_df['predicted_data']

        fig, ax = plt.subplots()
        sns.lineplot(x=result_df.index, y=result_df['predicted'], ax=ax)  # Zakładam, że index DataFrame to data
        plt.title("Przewidywania sprzedaży")
        plt.xlabel("Data")
        plt.ylabel("Przewidywana sprzedaż")
        st.pyplot(fig)
    
            

def facebookAlgorithm():
    st.header("Facebook algorithm")
    
    unique_data = pd.read_csv("Iowa_Unique.csv")

    # Utwórz listę z nazwami kolumn
    column_names = unique_data.columns.tolist()

    # Wybierz kolumnę za pomocą widżetu selectbox
    selected_column = st.selectbox("Wybierz kolumnę grupującą", column_names)

    # Wybierz unikalne wartości z wybranej kolumny
    unique_values = unique_data[selected_column].dropna().unique()

    # Wybierz wartość z unikalnych wartości za pomocą drugiego selectbox
    selected_value = st.selectbox(f"Wybierz wartość z {selected_column}", unique_values)

    predicted_column_names = ['Bottles Sold', 'Sale (Dollars)',
                     'Volume Sold (Liters)', 'Volume Sold (Gallons)']

    # Wybierz predykowane pole (kolejną kolumnę) za pomocą trzeciego selectbox
    predicted_column = st.selectbox("Wybierz predykowane pole", predicted_column_names)

    if st.button("Predict"):
        st.pyplot(groupBy(selected_column,selected_value,predicted_column))
    

def informacjeOgolne():
    st.header("Informacje ogólne")
    
    # Dodanie obrazka
    st.image("iowa_citizen.png", caption="Mieszkaniec stanu Iowa", use_column_width=True)

    # Dodanie artykułu
    st.write("""
    ## Iowa Liquor Sales Dataset

    Zbiór danych *Iowa Liquor Sales* zawiera informacje o sprzedaży napojów alkoholowych w stanie Iowa. Jest to cenne źródło danych dla analizy konsumpcji alkoholu oraz trendów w sprzedaży i dystrybucji napojów alkoholowych.

    ### Struktura danych

    Zbiór danych składa się z kilku kolumn, w tym:

    - **Date:** Data transakcji.
    - **Store Number:** Numer sklepu, w którym dokonano sprzedaży.
    - **City:** Miasto, w którym znajduje się sklep.
    - **Zip Code:** Kod pocztowy sklepu.
    - **County:** Powiat, w którym znajduje się sklep.
    - **Category:** Kategoria napoju alkoholowego.
    - **Vendor Number:** Numer dostawcy napoju.
    - **Item Number:** Numer przedmiotu (napoju).
    - **Item Description:** Opis napoju.
    - **Bottle Volume (ml):** Objętość butelki w mililitrach.
    - **State Bottle Retail:** Cena detaliczna butelki w danym stanie.
    - **Volume Sold (Liters):** Objętość sprzedanego napoju w litrach.
    - **Sale (Dollars):** Całkowita wartość sprzedaży w dolarach.

    ### Analiza danych

    Zbiór danych można wykorzystać do różnych analiz, takich jak:

    - Analiza sprzedaży w poszczególnych miastach czy powiatach.
    - Średnie wartości sprzedaży w zależności od kategorii napojów.
    - Analiza trendów czasowych w konsumpcji alkoholu.

    ### Korzystanie z danych

    Przed przystąpieniem do analizy warto dokładnie zbadać i oczyścić dane, aby uzyskać precyzyjne wyniki. Pamiętaj również o przestrzeganiu przepisów dotyczących prywatności i zabezpieczenia danych.

    Zapraszam do eksploracji danych i odkrywania fascynujących trendów w zestawie danych Iowa Liquor Sales!
    """)

if __name__ == "__main__":
    main()
