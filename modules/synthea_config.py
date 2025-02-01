import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'user': 'bennie.haelen@insight.com',
    'password': os.getenv("DB_PASSWORD"),
    'host': '34.30.224.53',
    'database': 'synthea',
    'port': 3306,
}
