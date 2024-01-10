import streamlit as st
import pandas as pd

# Wczytanie danych
data = pd.read_csv("iowa_dataset.csv")  # Podmień na odpowiednią nazwę pliku CSV

# Unikalne sklepy dostępne w danych
available_stores = data['name'].unique()

# Unikalne marki dostępne w danych
available_brands = data['vendor_name'].unique()

# Interfejs użytkownika
st.title("Przewidywanie Sprzedaży Alkoholu")

# Wybór opcji
selected_option = st.radio("Wybierz opcję:", ["Ogólna sprzedaż alkoholu dla danego sklepu", "Sprzedaż konkretnej marki alkoholu dla danego sklepu"])

if selected_option == "Ogólna sprzedaż alkoholu dla danego sklepu":
    # Wybór sklepu
    selected_store = st.selectbox("Wybierz sklep:", available_stores)

    # Przygotowanie danych tylko dla wybranego sklepu
    store_data = data[data['name'] == selected_store]

elif selected_option == "Sprzedaż konkretnej marki alkoholu dla danego sklepu":
    # Wybór sklepu
    selected_store = st.selectbox("Wybierz sklep:", available_stores)

    # Wybór marki
    selected_brand = st.selectbox("Wybierz markę alkoholu:", available_brands)

# Dodatkowe pola do wprowadzania danych użytkownika (opcjonalne)
st.sidebar.header("Dodatkowe opcje:")
item_no = st.sidebar.text_input("Numer produktu:")
pack = st.sidebar.text_input("Ilość opakowań:")
bottle_volume_ml = st.sidebar.text_input("Pojemność butelki (ml):")
state_bottle_cost = st.sidebar.text_input("Koszt butelki:")
state_bottle_retail = st.sidebar.text_input("Cena detaliczna butelki:")
sale_bottles = st.sidebar.text_input("Liczba sprzedanych butelek:")
sale_dollars = st.sidebar.text_input("Kwota sprzedaży:")

# Funkcja pomocnicza do bezpiecznej konwersji na liczbę całkowitą
def safe_cast(value, default):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Przygotowanie dodatkowych danych wejściowych (opcjonalne)
additional_input_data = pd.DataFrame({
    'store': [selected_store],
    'itemno': [safe_cast(item_no, 0)],
    'pack': [safe_cast(pack, 0)],
    'bottle_volume_ml': [safe_cast(bottle_volume_ml, 0)],
    'state_bottle_cost': [safe_cast(state_bottle_cost, 0.0)],
    'state_bottle_retail': [safe_cast(state_bottle_retail, 0.0)],
    'sale_bottles': [safe_cast(sale_bottles, 0)],
    'sale_dollars': [safe_cast(sale_dollars, 0.0)]
})
# Przewidywanie na podstawie dodatkowych danych (opcjonalne)
# if selected_option == "Ogólna sprzedaż alkoholu dla danego sklepu" and st.sidebar.button("Przewiduj na podstawie dodatkowych danych"):
#     additional_predictions = model.predict(additional_input_data[['store', 'itemno', 'pack', 'bottle_volume_ml', 'state_bottle_cost',
#                                                                  'state_bottle_retail', 'sale_bottles', 'sale_dollars']])
#     st.sidebar.header("Wyniki Dodatkowego Przewidywania")
#     st.sidebar.write("Przewidywana sprzedaż alkoholu w następnym miesiącu:", additional_predictions[0])

# elif selected_option == "Sprzedaż konkretnej marki alkoholu" and st.sidebar.button("Przewiduj na podstawie dodatkowych danych"):
#     additional_predictions = model.predict(additional_input_data[['store', 'itemno', 'pack', 'bottle_volume_ml', 'state_bottle_cost',
#                                                                  'state_bottle_retail', 'sale_bottles', 'sale_dollars']])
#     st.sidebar.header("Wyniki Dodatkowego Przewidywania")
#     st.sidebar.write("Przewidywana sprzedaż alkoholu w następnym miesiącu:", additional_predictions[0])

