import os, csv
from collections import deque

def environment_transform(environment=None):
    if environment is None:
        environment = os.getenv('APP_ENVIRONMENT', 'production')
    environment_dict = {
        "production":  "prod",
        "staging": "stg",
        "development": "dev",
        "prod": "prod",
        "stg": "stg",
        "dev": "dev",
        "local": "loc",
        "loc": "loc",
        "prd": "prod",
        "test": "test", 
        "testing": "test"
    }
    return environment_dict[environment]

def offset(limit, page): 
        if page <= 1:
                return 0
        return ((page - 1) * limit)

async def read_last_row_from_csv(file_path):
    # Buat antrian dengan kapasitas satu
    last_row_queue = deque(maxlen=1)

    # Buka file CSV
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Tambahkan setiap baris ke dalam antrian
        for row in csv_reader:
            last_row_queue.append(row)

    # Jika tidak ada baris yang terbaca, kembalikan None
    if not last_row_queue:
        return None

    # Kembalikan baris terakhir dari antrian
    return last_row_queue

async def read_csv(file_path):
    row_queue = []
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            row_queue.append(row)
    return row_queue