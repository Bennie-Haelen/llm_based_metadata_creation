import os
import json
import pandas as pd


# Define the path to the INPUT JSON file
input_file_path = os.path.join("fhir files", "big_query_encounter.json")

# Load the JSON data from a file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Load the mapping spreadsheet (replace with the actual file path)
spreadsheet_path = os.path.join("fhir files", "Nursing_Info_Mapping_Document.xlsx")
mapping_df = pd.read_excel(spreadsheet_path, sheet_name=None)

# Combine all sheet data into one DataFrame
mapping_combined = pd.concat(mapping_df.values(), ignore_index=True)

# Extract the field names from the mapping
field_names = mapping_combined["Field Name"].tolist()

# Extract relevant nursing-related fields dynamically
nursing_data = []
for record in data:
    nursing_record = {}
    for field in field_names:
        # Handle nested fields (e.g., departure_info.departure_disposition_text)
        keys = field.split(".")
        value = record
        for key in keys:
            value = value.get(key, "N/A") if isinstance(value, dict) else "N/A"
        nursing_record[field] = value
    nursing_data.append(nursing_record)

# Convert to a DataFrame
nursing_df = pd.DataFrame(nursing_data)

# Export to JSON
output_path = os.path.join("fhir files", "nursing_transformed_data.json")
nursing_df.to_json(output_path, orient="records", indent=4)

print(f"Transformed nursing data has been saved to {output_path}.")
