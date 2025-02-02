import os, csv, string, random
from collections import deque
from datetime import datetime
from sqlalchemy.engine.row import Row
import bcrypt

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


def json_serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO format string
    elif isinstance(obj, (tuple, set)):
        return list(obj)  # Convert tuple/set to list
    elif isinstance(obj, dict):
        return {key: json_serializable(value) for key, value in obj.items()}  # Process dict recursively
    elif isinstance(obj, list):
        return [json_serializable(item) for item in obj]  # Process list recursively
    elif isinstance(obj, Row):  # Handle SQLAlchemy Row
        return {key: json_serializable(value) for key, value in obj._mapping.items()}  # Use ._mapping for dictionary-like access
    elif hasattr(obj, "__dict__"):
        return {key: json_serializable(value) for key, value in vars(obj).items()}  # Handle custom objects
    return obj  # Fallback for unsupported types

def generate_random_string(length):  
    """  
    Generate a random string of specified length composed of letters and digits.  
  
    Parameters:  
    length (int): The length of the random string to generate.  
  
    Returns:  
    str: A random string containing uppercase letters, lowercase letters, and digits.  
    """  
    if length < 0:  
        raise ValueError("Length must be a non-negative integer.")  
      
    # Define the character set: uppercase, lowercase, and digits  
    characters = string.ascii_letters + string.digits  
      
    # Generate a random string  
    random_string = ''.join(random.choice(characters) for _ in range(length))  
      
    return random_string 

def generate_hashed_password(plain_password: str) -> str:
    """
    Generate a hashed password using bcrypt.

    Args:
        plain_password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to check against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))