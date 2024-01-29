import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import logging
from google.api_core.exceptions import BadRequest
from google.cloud import bigquery

def make_prediction(column,item,predicted_column,number_of_months):
    
    column = zmien_nazwe_kolumny(column)
    predicted_column = zmien_nazwe_kolumny(predicted_column)

    df = get_dataFrame(column,item,predicted_column)

    df = df.dropna()    

    # Próbujemy przekształcić kolumnę 'date' do typu daty
    df['date'] = pd.to_datetime(df['date'])

    # Grupowanie po 'Store Name' i zliczanie unikalnych dat, a następnie sortowanie wyników
    store_counts = df.groupby(column)['date'].nunique().reset_index()
    store_counts_sorted = store_counts.sort_values(by='date', ascending=False)  

    # Wybierz sklep, którego dane chcesz pozostawić
    wybrana_wartosc = item

    # Utwórz nowy DataFrame zawierający tylko dane z wybranego sklepu
    df_sklep = df[df[column] == wybrana_wartosc]

    # Agregacja danych tygodniowo i sumowanie sprzedaży dla każdego tygodnia
    df = df.resample('M', on='date')[predicted_column].sum().reset_index()

    # Zastosowanie funkcji do DataFrame
    df = replace_outliers_with_max(df, predicted_column)

    # Przekształć zestaw treningowy do formatu ds i y dla modelu Prophet
    df_train_prophet = df.rename(columns={'date': 'ds', predicted_column: 'y'})

    # Inicjalizacja modelu Prophet
    model = Prophet()

    # Trenowanie modelu na danych
    model.fit(df_train_prophet)

    # Tworzymy przyszłość z danymi godzinowymi na rok naprzód
    future = model.make_future_dataframe(periods=number_of_months, freq='M', include_history=False)
    forecast = model.predict(future)

    # Ograniczamy zakres dat na wykresie
    fig, ax = plt.subplots(figsize=(15, 8))  # Ustaw większy rozmiar figury
    ax.plot(forecast['ds'], forecast['yhat'], 'r-', label='Prognoza sprzedaży', linewidth=2)
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='pink', alpha=0.5, label='Przedział ufności (95%)')

    # Dodajmy także historyczne wartości
    ax.plot(df['date'], df[predicted_column], 'b-', label='Historia sprzedaży', linewidth=2)

    ax.set_title('Historia i prognoza sprzedaży')
    ax.set_xlabel('Data')
    ax.set_ylabel(predicted_column)
    plt.legend()
    plt.grid(True)
    # plt.show()
    return fig


def replace_outliers_with_max(df, column):
    # Obliczanie IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Definiowanie górnej granicy
    upper_bound = Q3 + 1.5 * IQR

    # Zastępowanie wartości odstających maksymalną wartością nieodstającą
    df[column] = df[column].apply(lambda x: min(x, upper_bound) if x >= 0 else x)

    # Opcjonalnie: zastąp wartości ujemne minimalną wartością nieujemną
    min_non_negative = df[df[column] >= 0][column].min()
    df[column] = df[column].apply(lambda x: max(x, min_non_negative))

    return df

def get_dataFrame(groupingColumn,item,predicted_column, project_id='caramel-park-411816'):
    # Delete all items from yesterday import
    bq = bigquery.Client(project=project_id)
    try:
        results = bq.query(f"SELECT {groupingColumn}, date, {predicted_column} FROM `ASI.sales` where {groupingColumn} = '{item}' AND {groupingColumn} IS NOT NULL AND date IS NOT NULL AND {predicted_column} IS NOT NULL")
        df = results.to_dataframe()
        print("📝 Successfully executed query")
    except BadRequest as e:
        print("⛔️ Unsuccessful query execution: %s", e)
        return str(e)
    else:
        return df
        

def zmien_nazwe_kolumny(stara_nazwa):
    # Utwórz słownik z mapowaniem starych nazw kolumn na nowe nazwy
    column_mapping = {
        'Store Name': 'store_name',
        'City': 'city',
        'Zip Code': 'zip_code',
        'County': 'county',
        'Category Name': 'category_name',
        'Vendor Name': 'vendor_name',
        'Item Description': 'item_description',
        'Bottles Sold': 'bottles_sold',
        'Sale (Dollars)': 'sale_dollars',
        'Volume Sold (Liters)': 'volume_sold_liters',
        'Volume Sold (Gallons)': 'volume_sold_gallons'
    }

    # Sprawdź, czy wybrana nazwa jest w słowniku
    if stara_nazwa in column_mapping:
        # Pobierz nową nazwę zgodnie z mapowaniem
        nowa_nazwa = column_mapping[stara_nazwa]
    else:
        nowa_nazwa = None

    return nowa_nazwa