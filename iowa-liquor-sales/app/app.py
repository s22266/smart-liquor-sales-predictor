import streamlit as st
import requests
import pandas as pd
from functions import make_prediction
import yaml
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from dataDownloader import DataLoader

base_url = "https://data.iowa.gov/resource/m3tr-qhgy.json"
# start_date = "2023-01-01T00:00:00"
# end_date = "2023-01-02T00:00:00"
output_dir = "./data/01_raw"

# Wskazanie ścieżki do katalogu głównego projektu Kedro
# Zakładając, że uruchamiasz Streamlit z tego samego katalogu
project_path = Path.cwd()

# Bootstrap projektu Kedro
bootstrap_project(project_path)

# Funkcja do uruchomienia Kedro pipeline
def run_kedro_pipeline(pipeline_name):
    with KedroSession.create(project_path=project_path) as session:
        return session.run(pipeline_name=pipeline_name)

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

    tabs = ["Informacje ogólne", "Algorytm Prophet", "Algorytm przewidywania sprzedaży"]
    choice = st.sidebar.selectbox("Wybierz stronę", tabs)

    if choice == "Informacje ogólne":
        informacjeOgolne()
    elif choice == "Algorytm Prophet":
        facebookAlgorithm()
    elif choice == "Algorytm przewidywania sprzedaży":
        algorytmPrzewidywaniaSprzedaży()

    start_date_to_download = str(st.sidebar.date_input("Wybierz datę początkową", value=pd.to_datetime("2016-12-01"))) + "T00:00:00"
    end_date_to_download = str(st.sidebar.date_input("Wybierz datę końcową", value=pd.to_datetime("2023-12-02"))) + "T00:00:00"

    if st.sidebar.button("Pobierz rekordy"):
        data_loader = DataLoader(base_url, start_date_to_download, end_date_to_download, output_dir)
        is_succes = data_loader.load_data()
        if is_succes:
            st.sidebar.write("Dane zapisane lokalnie w lokalizacji data/01_raw/imported_data_iowa_liquer.csv")
        elif is_succes == False:
            st.sidebar.write("Dane nie zostały zapisane")


    if st.sidebar.button("Retrain model"):
        run_kedro_pipeline("create_model")

def algorytmPrzewidywaniaSprzedaży():
    st.header("Algorytm przewidywania sprzedaży")

    # Wczytanie danych z pliku CSV do DataFrame
    countydf = pd.read_csv('./app/distinct_county.csv')
    selected_county = st.selectbox("Wybierz Chrabstwo", countydf['county'])

    alcoholTypes = ['Rum', 'Vodka', 'Tequila', 'Whiskies', 'Schnapps']
    selected_liquor = st.selectbox("Wybierz Alkohol", alcoholTypes)

    # Wybór daty początkowej i końcowej
    start_date = st.date_input("Wybierz datę początkową", value=pd.to_datetime("2023-12-01"))
    end_date = st.date_input("Wybierz datę końcową", value=pd.to_datetime("2024-12-31"))

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
        result= run_kedro_pipeline("model_prediction")

        result_df = result['predicted_data']

        st.dataframe(result_df)

        historic_df = result['historic_data']

        # Tworzenie daty na podstawie kolumn "Year" i "Month" dla wyników przewidywań
        result_df['Date'] = pd.to_datetime(result_df['Year'].astype(str) + '-' + result_df['Month'].astype(str))

        # Tworzenie daty na podstawie kolumn "Year" i "Month" dla danych historycznych
        historic_df['Date'] = pd.to_datetime(historic_df['Year'].astype(str) + '-' + historic_df['Month'].astype(str))

        fig, ax = plt.subplots()
        sns.lineplot(x=result_df['Date'], y=result_df['predicted'], ax=ax, label='Przewidywana sprzedaż')  
        sns.lineplot(x=historic_df['Date'], y=historic_df['Sale (Dollars)'], ax=ax, label='Rzeczywista sprzedaż')  # Dodanie danych historycznych
        plt.title("Przewidywania sprzedaży vs. Rzeczywista sprzedaż")
        plt.xlabel("Data")
        plt.ylabel("Sprzedaż w dolarach")
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(fig)
    
            

def facebookAlgorithm():
    st.header("Facebook algorithm")
    
    unique_data = pd.read_csv("./app/Iowa_Unique.csv")

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

    number_of_months = st.slider("Wybierz liczbę miesięcy do predykcji", min_value=1, max_value=69, value=1)

    if st.button("Prediction"):
        st.pyplot(make_prediction(selected_column,selected_value,predicted_column,number_of_months))
    

def informacjeOgolne():
    st.header("Informacje ogólne")
    
    # Dodanie obrazka
    st.image("./app/iowa_citizen.png", caption="Mieszkaniec stanu Iowa", use_column_width=True)

    # Dodanie artykułu
    st.write("""
    ## Iowa Liquor Sales Dataset
    
    Zbiór danych *Iowa Liquor Sales* zawiera informacje o sprzedaży napojów alkoholowych w stanie Iowa. Jest to cenne źródło danych dla analizy konsumpcji alkoholu oraz trendów w sprzedaży i dystrybucji napojów alkoholowych.
    
    ### Struktura danych
    
    Zbiór danych składa się z kilku kolumn, w tym:
    
    - **Invoice/Item Number:** Unikalny identyfikator zestawu zamówienia i numeru linii związanej z zamówieniem alkoholu w sklepie.
    - **Date:** Data zamówienia.
    - **Store Number:** Unikalny numer przypisany do sklepu, który zamówił alkohol.
    - **Store Name:** Nazwa sklepu, który zamówił alkohol.
    - **Address:** Adres sklepu, który zamówił alkohol.
    - **City:** Miasto, w którym znajduje się sklep zamawiający alkohol.
    - **Zip Code:** Kod pocztowy miejsca, w którym znajduje się sklep zamawiający alkohol.
    - **Store Location:** Lokalizacja sklepu, zamawiającego alkohol.
    - **County Number:** Numer hrabstwa w stanie Iowa, w którym znajduje się sklep zamawiający alkohol.
    - **County:** Hrabstwo, w którym znajduje się sklep zamawiający alkohol.
    - **Category:** Kod kategorii związany z zamówionym alkoholem.
    - **Category Name:** Kategoria zamówionego alkoholu.
    - **Vendor Number:** Numer dostawcy dla marki zamówionego alkoholu.
    - **Vendor Name:** Nazwa dostawcy dla marki zamówionego alkoholu.
    - **Item Number:** Numer identyfikacyjny produktu alkoholowego.
    - **Item Description:** Opis zamówionego produktu alkoholowego.
    - **Pack:** Liczba butelek w kartonie dla zamówionego alkoholu.
    - **Bottle Volume (ml):** Objętość każdej butelki alkoholu w mililitrach.
    - **State Bottle Cost:** Kwota, którą Alcoholic Beverages Division zapłaciła za każdą butelkę alkoholu w zamówieniu.
    - **State Bottle Retail:** Kwota, którą sklep zapłacił za każdą butelkę alkoholu w zamówieniu.
    - **Bottles Sold:** Ilość butelek alkoholu zamówionych przez sklep.
    - **Sale (Dollars):** Całkowity koszt zamówienia alkoholu.
    - **Volume Sold (Liters):** Całkowita objętość zamówionego alkoholu w litrach.
    - **Volume Sold (Gallons):** Całkowita objętość zamówionego alkoholu w galonach.
    
    """)

if __name__ == "__main__":
    main()
