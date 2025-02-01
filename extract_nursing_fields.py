import os
from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the LangChain LLM
llm = ChatOpenAI(
    model="gpt-4o",  # Use GPT-4 or another supported model
    temperature=0.0,
    max_tokens=1000
)

def extract_nursing_fields(input_file: str, output_file: str):
    """
    Extract nursing-related fields from the given schema using OpenAI and LangChain.

    Parameters:
        input_file (str): Path to the input file containing the schema.
        output_file (str): Path to the output file to save extracted fields.
    """
    # Load schema from the input file
    with open(input_file, 'r') as file:
        schema = file.read()

    # Define the prompt
    prompt_template = PromptTemplate(
        input_variables=["schema"],
        template="""
You are an expert in healthcare data and FHIR standards. Based on the provided source schema, generate a valid FHIR Encounter resource in JSON format, but **include only nursing-related fields**. Follow these guidelines:

1. Identify nursing-related fields based on keywords like: `nursing`, `assessment`, `observation`, `priority`, `triage`, `intervention`, `disposition`, `emergency`, `location`, and `arrival`.
2. Map the identified fields to appropriate FHIR Encounter fields, following the FHIR standard for field names, nesting, and structures.
3. If no direct mapping exists for a field, add it as a FHIR extension.
4. Include sample or placeholder values for required fields.

#### Source Schema:
{schema}

#### Output Format:
Generate the FHIR Encounter resource in JSON format with fields structured as follows:
- `resourceType`: Always set to `"Encounter"`.
- `id`: Map to the unique identifier for the encounter.
- `status`: Use `"in-progress"`, `"finished"`, or appropriate status.
- `class`: Use FHIR coding for the encounter class (e.g., `"INPATIENT"`, `"OUTPATIENT"`).
- `type`: Use SNOMED CT or other coding systems for nursing-specific encounter types (e.g., `"Nursing Assessment"`).
- `participant`: Include nursing participants (e.g., `Practitioner`) with their roles and references.
- `period`: Map nursing-relevant admission and discharge dates to `start` and `end` fields.
- `serviceType`: Use appropriate coding to describe the service type (e.g., `"Wound Care"`).
- `reasonCode`: Include reasons relevant to nursing interventions.
- `location`: Include nursing-relevant location details with references (e.g., `treatment room`, `ward`).
- `extension`: Add custom nursing-specific fields that do not have a direct mapping.

Ensure the JSON is valid, well-structured, and uses proper FHIR coding where required. 

Output only the JSON, no other fields, no backticks, and no comments.
        """
    )

    prompt = prompt_template.format(schema=schema)

    # Setup our chain
    response = llm.invoke(prompt)


    # Extract and save the output
    extracted_fields = response.content
    with open(output_file, 'w') as file:
        file.write(extracted_fields)

    print(f"Extracted nursing-related fields have been saved to {output_file}.")

# Example usage
# Make sure to set your OpenAI API key in the environment variable `OPENAI_API_KEY` before running this program
if __name__ == "__main__":
    input_file_path = os.path.join("fhir files", "encounters_table_schema.json")
    output_file_path = os.path.join("fhir files", "__encounters_nursing_fields.json")

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

    extract_nursing_fields(input_file_path, output_file_path)
