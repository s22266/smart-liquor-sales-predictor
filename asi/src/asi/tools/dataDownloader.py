import pandas as pd
import os
from urllib.parse import quote_plus
import time

class DataLoader:
    def __init__(self, base_url, start_date, end_date, output_dir, limit=1000):
        self.base_url = base_url
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir
        self.limit = limit

    def build_query(self, offset):
        where_clause = f"date between '{self.start_date}' and '{self.end_date}'"
        encoded_where_clause = quote_plus(where_clause)
        query_parameters = f"?$where={encoded_where_clause}&$limit={self.limit}&$offset={offset}&$order=:id"
        return self.base_url + query_parameters

    def load_data(self):
        data_frames = []
        offset = 0

        while True:
            full_url = self.build_query(offset)
            print(f"URL : {full_url}")

            try:
                data = pd.read_json(full_url)

                if data.empty:
                    print("Data is empty")
                    break

                data_frames.append(data)
                offset += self.limit

                time.sleep(2) #Page overload when sleep < 2

            except Exception as e:
                print(f"Error while downloading URL: {full_url}, error: {e}")
                break

        all_data = pd.concat(data_frames, ignore_index=True)

        self.save_data(all_data)

    def save_data(self, data):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        output_path = os.path.join(self.output_dir, 'downloaded_data.csv')
        data.to_csv(output_path, index=False)
        print(f"Dane zapisane do {output_path}")

# Ustawienia
base_url = "https://data.iowa.gov/resource/m3tr-qhgy.json"
start_date = "2020-01-01T00:00:00"
end_date = "2023-01-01T00:00:00"
output_dir = "../../../data/01_raw"

# Użycie klasy DataLoader
data_loader = DataLoader(base_url, start_date, end_date, output_dir)
data_loader.load_data()
