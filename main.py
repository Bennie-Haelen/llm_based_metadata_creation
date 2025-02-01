# Step 1: Fetch metadata from the information schema
import json

from modules.process_metadata import process_metadata
from modules.synthea_config import DB_CONFIG as SYNTHEA_DB_CONFIG
from modules.Information_schema_retrieval import fetch_metadata_from_information_schema

metadata = fetch_metadata_from_information_schema(SYNTHEA_DB_CONFIG)

# Step 2: Process the fetched metadata
if metadata:
    descriptions = process_metadata(metadata)

    # Step 3: Save the descriptions to a file
    with open("database_descriptions.json", "w") as f:
        json.dump(descriptions, f, indent=4)