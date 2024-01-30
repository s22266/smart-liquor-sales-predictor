
# Przewidywanie Sprzedaży alkoholu w stanie IOWA

## Ważne 

Należy wrzucić odpowiedni plik credentials.json do folderu conf/local pod nazwą credGoogleCloud.json w clu połączenia z usługą google Big Query

W celu poprawnego działaniu części wykorzystującej autogluon należy kliknąć w przycisk "Pobierz rekordy" na stronie głównej aplikacji stremalit lub pobrać dataset Iowa-Liquor-Sales z strony https://data.iowa.gov/Sales-Distribution/Iowa-Liquor-Sales/m3tr-qhgy/data_preview w foramcie ".csv" i umieścić go w folderze "data/01_raw/" pod nazwą imported_data_iowa_liquer.csv

## Opis funkcjonalności 

Główne funkcjonalności aplikacji do prognozowania sprzedaży obejmują: 

### Algorytm WeightedEnsemble_L2: 

Umożliwia przewidywanie ogólnej sprzedaży alkoholu w oparciu o wybraną kategorię alkoholu i hrabstwo. Użytkownik ma możliwość wyboru z listy rozwijanej interesującego go hrabstwa oraz kategorii produktu, a system generuje prognozę sprzedaży dla tej kombinacji. 

### Algorytm Prophet: 

Drugi algorytm oferuje bardziej szczegółowe prognozy sprzedaży, biorąc pod uwagę dodatkowe kolumny grupujące takie jak: miasto (City), hrabstwo (County), nazwa kategorii (Category Name), nazwa dostawcy (Vendor Name), opis przedmiotu (Item Description). 

Algorytm przewiduje wartości takie jak liczba sprzedanych butelek (Bottles Sold), sprzedaż w dolarach (Sale in Dollars), oraz objętość sprzedanego alkoholu zarówno w litrach (Volume Sold in Liters) jak i w galonach (Volume Sold in Gallons). 

Aplikacja pozwala użytkownikom na dokładną analizę trendów sprzedażowych i prognozowanie przyszłych wyników sprzedaży. 

## 1. Stawianie obrazu dockerowego 

Założnie: Aplikacja Docker jest zainstalowana 

#### 1) Postawienie lokalnie kontenera
docker build -t "nazwa kontenera" .

#### 2) Uruchomienie kontenera
docker run -p 8080:8080 "nazwa kontenera"

## 2. Local

#### 1) Pobranie wymaganych zależności 

pip install -r src/requirements.txt

#### 2) uruchomienia aplikacji webowej lokalnie

streamlit run app/app.py








