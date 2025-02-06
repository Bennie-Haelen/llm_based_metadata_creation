import json
import sqlfluff

def get_field_sql(field):
    """
    Recursively generates the SQL definition for a single field.
    
    Parameters:
        field (dict): A dictionary representing the field metadata.
        
    Returns:
        str: A SQL snippet for the field.
    """
    # Extract basic properties; treat an empty mode as NULLABLE
    name = field["name"]
    field_type = field["type"].upper()
    mode = field.get("mode") or "NULLABLE"
    description = field.get("description", "")

    # If the field is a RECORD or has nested fields, process them recursively.
    # (BigQuery uses STRUCT for nested types.)
    if field_type == "RECORD" or (field.get("fields") and len(field["fields"]) > 0):
        nested_fields = field["fields"]
        # Generate SQL definitions for each nested field
        nested_sql_parts = [get_field_sql(subfield) for subfield in nested_fields]
        nested_sql = ", ".join(nested_sql_parts)
        base_type = f"STRUCT<{nested_sql}>"
    else:
        base_type = field_type

    # If the mode is REPEATED, wrap the type in an ARRAY<>
    if mode.upper() == "REPEATED":
        base_type = f"ARRAY<{base_type}>"


    return f"{name} {base_type} OPTIONS(description=\"{description}\")" if description else f"{name} {base_type}"



def generate_create_table_statement(table_name, schema):
    """
    Generates a CREATE TABLE statement based on the provided schema.
    
    Parameters:
        table_name (str): The name of the table to create.
        schema (list): A list of field dictionaries representing the schema.
        
    Returns:
        str: The complete CREATE TABLE statement.
    """
    # Generate the SQL for each field and join them with commas and newlines.
    fields_sql = ",\n  ".join(get_field_sql(field) for field in schema)
    create_table_sql = f"CREATE OR REPLACE TABLE {table_name} (\n  {fields_sql}\n);"
    return create_table_sql


if __name__ == "__main__":
    # Example: Load your JSON schema from a file or define it directly.
    # Here, we're defining the schema directly using the provided JSON.
    # Load the schema JSON (it can also come from a file or other source)

    path  = "fhir files/schema_with_descriptions.json"
    
    with open(path, "r") as file:
        schema = json.load(file)

    # Generate and print the CREATE TABLE statement
    create_table_statement = generate_create_table_statement('hca-sandbox.hca_metadata_pot.bennie2', schema)
    final_create_table_statement = sqlfluff.fix(create_table_statement, dialect="bigquery")
    print(final_create_table_statement)