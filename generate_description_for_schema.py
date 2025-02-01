import re
import yaml
import json
import argparse
import argparse
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
from logger_setup import logger, log_entry_exit

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import HumanMessage

from modules.create_table_sql import generate_create_table_sql 
from modules.FHIResourceManager import FHIRResourceManager 
from modules.llm_utils import get_llm


# This is the max length of the description that can be stored in BigQuery
# for either a column or a table, we did not make this a YAML parameter
# since it is a constant value
CHARACTER_LIMIT = 1024

 # Load environment variables from our .env file.
 # We store our API keys and other sensitive information in the .env file
load_dotenv()

class LevelOfDetail(Enum):
    CONSISE = "concise"
    DETAILED = "detailed"
    MOST_DETAILED = "most_detailed"
    FOCUS_ON_DATA_GOVERNANCE = "data_governance"


# Function to load the schema from a JSON file
def load_schema(schema_path):
    """Load the schema from a JSON file specified by the schema_path."""

    with open(schema_path, 'r') as f:
        return json.load(f)
    


# Process the response to extract only the initial lines before "### Field Name"
def extract_initial_lines(response_text):
    delimiter = "### Field Name"
    extracted_text = response_text.split(delimiter)[0].strip()
    return extracted_text


# Function to escape descriptions safely for BigQuery SQL
def escape_description(description):
    """Removes newlines and normalizes whitespace in a string."""
    cleaned_text = description.replace('\n', ' ').replace('\r', ' ')  # Replace newlines/CRs with spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Normalize whitespace (multiple spaces to single, remove leading/trailing)
    
    return cleaned_text

@log_entry_exit  
def generate_enriched_schema(json_schema, fhir_type, llm):

    # Create parser
    parser = JsonOutputParser()
    instructions = parser.get_format_instructions()

    prompt_template = PromptTemplate(
        input_variables=["json_schema", "fhir_type"],
        template="""
        You are an advanced FHIR domain expert with deep knowledge of HL7, FHIR resources, and healthcare interoperability standards.

        I have a JSON schema that represents a FHIR  `{fhir_type}` table.

        You need to provide a the FHIR details summary for each field in the schema. THis is called the 'enriched version'. Limit this summary to 1024 characters

        for example, if the field is 'discharge_date', the enriched version could be:
        
                ```The "discharge_date" field in a FHIR Encounter resource represents the date and time when the patient was officially discharged from the encounter.

                    Key Considerations:

                    Data Type: Typically represented as an instant data type in FHIR, which is a date and time with timezone.
                    Clinical Significance:
                    Marks the end of the encounter: Crucial for determining the duration of the encounter and for various clinical and operational purposes.
                    Billing and Reimbursement: Essential for accurate billing and reimbursement calculations.
                    Clinical Documentation: Used to document the patient's discharge time for continuity of care and medical record keeping.
                    Quality Improvement: Can be used to analyze length of stay, identify potential delays, and improve patient flow.
                    Relationship to Encounter Period: The "discharge_date" is closely related to the period element of the Encounter resource, which defines the overall timeframe of the encounter. The period.end should generally align with the discharge_date.
                    Special Considerations:
                    Not always applicable: For some encounter types (e.g., brief outpatient visits), a formal "discharge" may not be applicable.
                    Accuracy: Ensuring accurate discharge dates is critical for data quality and clinical decision-making.
                    In Summary:

                    The "discharge_date" field is a fundamental element of the FHIR Encounter resource, capturing the crucial point in time when the patient's interaction with the healthcare provider concludes. It plays a vital role in various aspects of healthcare delivery, from clinical documentation and billing to operational efficiency and quality improvement```


        **Requirements:**

        * Do not omit any fields, include every field in the FHIR schema listed below, do not skip or omit any fields.
        * Replace the `description` attribute of each field with the enriched version.
        * Output must remain a valid JSON array.
        * Do not add extra text, disclaimers, backticks, or markdown formatting.

        **FHIR Schema:**
        {json_schema}

        **Output:**
        Return only the enriched valid JSON array, ensuring all descriptions follow the above requirements.        
        """
        )
    try:

        # format the prompt
        prompt = prompt_template.format(
            json_schema=json_schema, 
            fhir_type=fhir_type, 
            character_limit=CHARACTER_LIMIT, 
            instructions=instructions)

        # Invoke the model
        response = llm.invoke(prompt).content

        # Use the JSsonOutputParser to extract the JSON array from the response
        parsed_data = parser.parse(response)
        return parsed_data

    except Exception as e:
        logger.error(f"Error generating schema with description for fhir resource: {fhir_type}': {e}")

    return None


@log_entry_exit
def create_sql_from_schema(schema_json, table_description, resource_name, full_table_name, llm, mode):

    if mode == "alter":
        logger.info("Creating ALTER TABLE SQL statements...")
        prompt_template = PromptTemplate(
                input_variables=["schema_json", "resource_name", "full_table_name", "table_description"],
                template="""
                    You are a data engineer who needs to write an ALTER TABLE query for an existing 
                    BigQuery {resource_name} table with name: {full_table_name}.

                    ### **Step 1: Modify the Table Description**
                    First, create an **ALTER TABLE** statement to add the following table description:
                    "{table_description}"

                    ### **Step 2: Modify Column Descriptions**
                    Here is the schema for the FHIR {resource_name} table. Write an **ALTER TABLE DDL** statement 
                    to **add column descriptions** to the encounter table:
                    {schema_json}

                    Do NOT generate an ALTER COLUMN statement for nested fields.

                """)
        
    elif mode == "create":
        logger.info("Creating CREATE TABLE SQL statements...")
        prompt_template = PromptTemplate(
                input_variables=["schema_json", "resource_name", "full_table_name", "table_description"],
                template="""
                    You are a data engineer who needs to write an CREATE OR REPLACE TABLE query for a new 
                    BigQuery {resource_name} table with name: {full_table_name}.

                    The schema of the table is here:
                    {schema_json}.

                    Make sure to create a column-level description based upon the description fields in the schema

                    Make sure to add a table level description with this text: {table_description}.

                    Ensure that the SQL output is 100% valid SQL for BigQuery

                """)
    else:
        logger.error(f"Invalid mode specified: {mode}")
        pass
     
    # Create the prompt        
    prompt = prompt_template.format(
        schema_json=schema_json, 
        full_table_name=full_table_name, 
        table_description=table_description, 
        resource_name=resource_name)

    # Invoke the model
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(input=messages)

    # Return the response
    return response.content


# Function to save the enriched schema to a file
@log_entry_exit
def save_enriched_schema(enriched_schema, output_path):
    """
    If enriched_schema is a string containing JSON, parse it first so we can
    dump a proper JSON array. Otherwise, just dump directly.
    """

    # If the enriched schema is a string, attempt to parse it as JSON
    if isinstance(enriched_schema, str):

        try:
            logger.info("Attempting to parse enriched schema as JSON...")
            enriched_schema = json.loads(enriched_schema)
            logger.info("Enriched schema successfully parsed as JSON.")

        except json.JSONDecodeError:
            logger.error("Warning: Could not parse enriched_schema as JSON.")
            # If it truly isn't valid JSON, handle as needed.

    # Save the enriched schema to the output path
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_schema, f, indent=2)


@log_entry_exit
def save_final_sql(sql_statements, output_path):
    """
        This function saves the final SQL statements to the sepcified output path.

        Args:
            sql_statements (str): The SQL statements to be saved.
            output_path (str): The path where the SQL statements will be saved.
    """

    # Ensure SQL statements contain actual newlines,
    # and save the file with proper formatting
    logger.info("Performing initial saving...")
    formatted_sql = sql_statements.encode().decode('unicode_escape')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted_sql)

    """
    Reads the SQL code from input_file, removes any lines containing triple backticks,
    and writes the cleaned code to output_file.
    """

    # Read the SQL code from the input file and remove lines with 
    # triple backticks and/or sql prefix
    logger.info("Re-reading the file and cleaning the SQL code...")
    with open(output_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    cleaned_lines = []
    for line in lines:
        # Skip lines containing only triple backticks
        # (You can adjust this check if your triple backticks appear differently)
        if line.strip() in ("```sql", "```"):
            continue
        cleaned_lines.append(line)

    # Write the cleaned SQL code to the output file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(cleaned_lines)
    
    logger.info("Final Save completed, cleaned SQL code saved")


@log_entry_exit
def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a Python dictionary.

    :param file_path: The path to the YAML file.
    :return: The contents of the YAML file as a dictionary
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data



#  ---------------------------------------------------------------------------
# This function will parse the YAML data and extract the 
# configuration information
#  ---------------------------------------------------------------------------
@log_entry_exit
def parse_yaml_data(config_data):
    """
    Parses the YAML data and extracts the configuration information.

    :param data: The YAML data to parse.
    :return: The configuration information as a dictionary
    """
    # Access the YAML information
    # Access app settings
    app_name    = config_data['app']['app_name'].strip()
    app_version = config_data['app']['app_version'].strip()

    # Access the file information
    input_schema_location  = config_data['files']['input_schema'].strip()
    output_schema_location = config_data['files']['output_schema'].strip()
    sql_output_location    = config_data['files']['sql_output'].strip()

    # Get the big query info
    project_id  = config_data['bigquery']['project_id'].strip()
    dataset_id  = config_data['bigquery']['dataset_id'].strip()
    table_id    = config_data['bigquery']['table_id'].strip()
    location    = config_data['bigquery']['location'].strip()
    mode        = config_data['bigquery']['mode'].strip()

    # Build the full table name
    full_table_name = f"{project_id}.{dataset_id}.{table_id}"

    # LLM INfo
    llm_model = config_data['llm']['model'].strip()

    # Finally, return the configuration information as a large tuple
    return app_name, app_version, input_schema_location, output_schema_location, sql_output_location, \
           project_id, dataset_id, table_id, full_table_name, location, mode, llm_model



# Initialize logger
# logger = logging.getLogger(__name__)

# Main function to orchestrate the process
def main():
    """
    Parses arguments, reads YAML configuration, and orchestrates the process of
    generating enriched descriptions for FHIR schema fields and generating SQL statements
    to either create a new table, or update an existing table with UPDATE statements.
    """

    # Argument parser for YAML file location
    parser = argparse.ArgumentParser(description="Generate rich descriptions for FHIR schema fields.")
    parser.add_argument('--yaml', type=str, required=True, help='The location of the YAML file')

    # Parse arguments and extract the YAML source path
    args = parser.parse_args()
    yaml_source_path = Path(args.yaml)
    logger.info(f"YAML Source Path: {yaml_source_path}")

    # Read YAML configuration file
    config_data = read_yaml_file(yaml_source_path)

    if not config_data:
        logger.error("Failed to load YAML configuration.")
        return

    # Parse the YAML data
    (
        app_name, app_version, input_schema_location, output_schema_location,
        sql_output_location, project_id, dataset_id, table_id,
        full_table_name, location, mode, llm_model
    ) = parse_yaml_data(config_data)

    # Log the parsed arguments for debugging
    indentation = ' ' * 25
    logger.info(f"Parsed YAML Arguments: \n"
            f"{indentation}input_schema_location..................: '{input_schema_location}',\n"
            f"{indentation}output_schema_location.................: '{output_schema_location}',\n"
            f"{indentation}sql_output_location....................: '{sql_output_location}',\n"
            f"{indentation}project_id.............................: '{project_id}',\n"
            f"{indentation}dateset_id.............................: '{dataset_id}',\n"
            f"{indentation}table_id...............................: '{table_id}',\n"
            f"{indentation}full_table_name........................: '{full_table_name}',\n"
            f"{indentation}location...............................: '{location}',\n"
            f"{indentation}mode...................................: '{mode}',\n"
            f"{indentation}LLM Model..............................: '{llm_model}'")


    # Initialize the Language Model (LLM)
    llm = get_llm(llm_model)

    # Load the input schema, representing the complete schema for the table
    schema = load_schema(input_schema_location)

    # Determine the corresponding FHIR resource name from the table name
    fhir_mgr = FHIRResourceManager(llm)
    fhir_resource = fhir_mgr.get_fhir_resource_name(full_table_name)
    logger.info(f"FHIR Resource Name Identified: {fhir_resource}")


    # Generate a table-level description for the FHIR table
    table_description = fhir_mgr.generate_description(fhir_resource)
    logger.info(f"Table Description Generated...")


    # Create an enriched schema with additional descriptions for each field
    logger.info("Generating enriched schema with descriptions...")
    enriched_schema = generate_enriched_schema(schema, fhir_resource, llm)
    logger.info("Enriched schema generation completed.")


    # Save the enriched schema to the output location
    save_enriched_schema(enriched_schema, output_schema_location)
    logger.info(f"Enriched schema successfully saved to: '{output_schema_location}'")

    # Generate SQL statements (ALTER TABLE / CREATE TABLE) based on the mode
    logger.info("Starting the SQL generation process...")
    generated_sql = create_sql_from_schema(
        enriched_schema, table_description, fhir_resource, full_table_name, llm, mode)
    logger.info("SQL generation completed.")

    # Save the generated SQL file
    save_final_sql(generated_sql, sql_output_location)
    logger.info(f"Generated SQL saved to: '{sql_output_location}'")

    logger.info("Process completed successfully.")
# Execute the script
if __name__ == "__main__":
    main()
