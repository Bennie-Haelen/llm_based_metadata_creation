import os
import json

credentials_path = "credentials_new.json"
if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
else:
    print("Credentials file found")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

from modules.BigQuerySchemaManager import BigQuerySchemaManager 

def extract_json_schema_from_table(project_id, dataset_id, table_id):

    # Initialize BigQuerySchemaManager
    bq_schema_manager = BigQuerySchemaManager(project_id, dataset_id)

    # Get the schema in JSON format
    schema_json = bq_schema_manager.get_table_schema(table_id, format="json")
    return schema_json

def main():

    dll = extract_json_schema_from_table("hca-sandbox", "hca_metadata_pot", "fhir_encounter")    
    print(dll)


if __name__ == "__main__":
    main()