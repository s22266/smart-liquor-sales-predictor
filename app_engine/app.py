import streamlit as st
import pandas as pd
from functions import make_prediction


base_url = "https://data.iowa.gov/resource/m3tr-qhgy.json"
output_dir = "./data/01_raw"

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
