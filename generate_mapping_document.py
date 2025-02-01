import os 
import json
from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
import argparse

# Initialize the LangChain LLM
llm = ChatOpenAI(
    model="gpt-4o",  # Use GPT-4 or another supported model
    temperature=0.0,
    max_tokens=10000
)

def extract_nursing_fields(table_schema_file_path, mapping_schema_file_path, domain_name):
    """
    Extract nursing-related fields from a JSON file using OpenAI's GPT API.

    Args:
        table_schema_file_path (str): Path to the JSON file containing the table schema.
        mapping_schema_file_path (str): Path to save the generated mapping schema JSON file.
        domain_name (str): The domain name for future use.

    Returns:
        None
    """
    # Load the JSON file
    with open(table_schema_file_path, 'r') as f:
        data = json.load(f)

    # Prepare the JSON schema as a string for the prompt
    json_content = json.dumps(data, indent=2)

    # Define the prompt
    prompt_template = PromptTemplate(
        input_variables=["schema"],
        template="""
    You are an expert in healthcare data analysis. I have a JSON file that contains healthcare encounter data.

    Your task is to extract a list of fields that are specifically nursing-related. Examples of nursing-related fields include patient locations (e.g., room, unit, bed), emergency department triage information, admission and discharge details, and patient conditions.

    When processing fields that contain sub-fields (e.g., `patient_location`), break down the sub-fields into separate entries. For example, if a field like `patient_location` contains attributes such as `location_id`, `mnemonic`, and `physical_type`, each attribute should be listed as an individual field with its full JSON path.

    You should:
    1. Categorize the fields into one of the following groups: **Patient Information**, **Nursing Assessment**, **Nursing Interventions**, **Nursing Outcomes**, and **Other Nursing-Related Fields**.
    2. Return a dictionary where each group name is a key, and the value is a list of fields within that group.
    3. For each field, provide:
    - The full JSON path as the key.
    - A dictionary containing:
        - `type`: The data type of the field.
        - `reference`: Provide the reference to the FHIR resource that this field is referencing, or 'N/A' otherwise.
        - `PII/PHI`: Answer 'True' if this field is considered PII or PHI. Answer 'False' otherwise.
        - `HIPAA`: Answer 'True' if this field is considered HIPAA. Answer 'False' otherwise.
        - `examples`: A list of example values extracted from the JSON data.
        - `description`: A brief description of the field.

    If the field value in the encounter data is `null`, replace it with relevant examples from FHIR resources or other healthcare standards. Ensure no example is left as `null`.

    Here is the JSON encounter data:
    {json_content}

    Return only the dictionary with the groups and fields, no other information. Do not add backticks around the JSON.
    Do not include the word "json" at the beginning of the JSON content.
    """
    )

    prompt = prompt_template.format(json_content=data)

    # Setup our chain
    response = llm.invoke(prompt)

    # Save the generated mapping schema to the specified file path
    with open(mapping_schema_file_path, "w") as output_file:
        output_file.write(response.content)

    print(f"Nursing-related fields have been saved to {mapping_schema_file_path}.")

# Example usage
if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract nursing-related fields from a JSON schema.")
    parser.add_argument("--table_schema_file_path", type=str, required=True, help="Path to the JSON file containing the table schema.")
    parser.add_argument("--mapping_schema_file_path", type=str, required=True, help="Path to save the generated mapping schema JSON file.")
    parser.add_argument("--domain_name", type=str, required=True, help="The domain name for future use.")

    # Parse arguments
    args = parser.parse_args()

    # Extract nursing-related fields
    extract_nursing_fields(args.table_schema_file_path, args.mapping_schema_file_path, args.domain_name)
