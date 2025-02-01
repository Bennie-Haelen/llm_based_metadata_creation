import os
import json
import sqlfluff
import argparse

def generate_sql_from_mapping(table_name, mapping_file, schema_file):
    """
    Generate SQL dynamically from a mapping file and a BigQuery table schema.

    Args:
        table_name (str): Name of the BigQuery table to query.
        mapping_file (str): Path to the JSON file defining nursing-related fields.
        schema_file (str): Path to the JSON file defining the BigQuery table schema.

    Returns:
        str: Generated SQL query as a string.
    """
    # Load the mapping file
    print(f"Loading mapping file: {mapping_file}")
    with open(mapping_file, 'r') as mf:
        nursing_fields = json.load(mf)

    # Load the BigQuery table schema
    print(f"Loading schema file: {schema_file}")
    with open(schema_file, 'r') as sf:
        schema = json.load(sf)

    # Function to check if a field is an array (repeated field)
    def is_repeated_field(field_name, schema):
        # Iterate over schema to find the matching field
        for field in schema:
            # Check if the base field matches
            if field['name'] == field_name.split('.')[0]:
                # If it's a nested field, check its subfields
                if 'fields' in field and '.' in field_name:
                    nested_fields = field['fields']
                    for nested_field in nested_fields:
                        if nested_field['name'] == field_name.split('.')[1] and nested_field['mode'] == 'REPEATED':
                            return True
                # Otherwise, check if the field itself is repeated
                return field.get('mode') == 'REPEATED'
        return False

    # Initialize SQL parts
    select_clauses = []
    from_clauses = [f"`{table_name}` AS t"]

    # Counter to generate unique aliases for UNNEST
    unnested_alias_counter = 0

    # Iterate over the nursing fields to create SELECT and FROM clauses
    for category, fields in nursing_fields.items():
        for field, details in fields.items():
            description = details.get("description", "")

            # Check if the field is an array
            if is_repeated_field(field, schema):
                base_field = field.split('.')[0]  # Extract base field name
                alias = f"unnested_{unnested_alias_counter}"  # Create unique alias
                unnested_alias_counter += 1

                # Add UNNEST clause to FROM
                from_clauses.append(f"UNNEST(t.{base_field}) AS {alias}")

                # Handle nested fields in the array
                nested_field = field.split('.')[1] if '.' in field else None
                if nested_field:
                    clause = f"{alias}.{nested_field} AS {field.replace('.', '_')}"
                else:
                    clause = f"{alias} AS {field}"
            else:
                # Handle non-array fields
                if '.' in field:
                    clause = f"{field} AS {field.replace('.', '_')}"
                else:
                    clause = f"t.{field} AS {field}"

            # Add clause to SELECT
            select_clauses.append(f"    {clause}")

    # Combine SELECT and FROM clauses into a complete SQL query
    sql_query = (
        "SELECT\n" +
        ",\n".join(select_clauses) +
        "\nFROM\n" +
        "    " + ",\n    ".join(from_clauses) +
        ";"
    )

    return sql_query

def format_sql(sql_query):
    """
    Format SQL query using SQLFluff.

    Args:
        sql_query (str): Raw SQL query.

    Returns:
        str: Formatted SQL query.
    """
    # Use SQLFluff to fix and format the query
    return sqlfluff.fix(sql_query, dialect="ansi")

if __name__ == "__main__":
    # Set up argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Generate SQL dynamically from a mapping file and schema.")
    parser.add_argument("--table_name", required=True, help="BigQuery table name to query.")
    parser.add_argument("--mapping_file", required=True, help="Path to the nursing-related fields mapping JSON file.")
    parser.add_argument("--schema_file", required=True, help="Path to the BigQuery table schema JSON file.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Generate the raw SQL query from the mapping and schema files
    raw_sql_query = generate_sql_from_mapping(args.table_name, args.mapping_file, args.schema_file)

    # Format the SQL query using SQLFluff
    formatted_sql_query = format_sql(raw_sql_query)

    # Output the formatted SQL query
    print(formatted_sql_query)
