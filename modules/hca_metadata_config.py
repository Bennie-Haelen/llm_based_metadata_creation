import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'user': 'bennie.haelen@insight.com',
    'password': os.getenv("DB_PASSWORD"),
    'host': '34.66.23.188',
    'database': 'hca_metadata',
    'port': 3306,
}
