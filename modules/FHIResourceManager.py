from langchain.schema import HumanMessage
from langchain_core.prompts import PromptTemplate

from modules.llm_utils import get_llm
from logger_setup import logger, log_entry_exit

class FHIRResourceManager:

    def __init__(self, llm):  # llm_model is optional
        self.llm_model = llm


    @log_entry_exit
    def get_fhir_resource_name(self, full_table_name):
        """
        Extracts and converts a BigQuery table name into a FHIR resource name.

        This function takes a fully qualified BigQuery table name (which may include multiple 
        hierarchical levels separated by periods) and extracts the last segment. If the extracted 
        table name starts with "fhir_", that prefix is removed to return a clean FHIR resource name.

        Parameters:
        - full_table_name (str): The fully qualified BigQuery table name in the format 
        "project.dataset.table_name".

        Returns:
        - str: The cleaned FHIR resource name.
        
        Example Usage:
        >>> get_fhir_resource_name("my_project.my_dataset.fhir_Patient")
        'Patient'

        >>> get_fhir_resource_name("bigquery.fhir_Observation")
        'Observation'

        >>> get_fhir_resource_name("bigquery.some_other_table")
        'some_other_table'
        """
        logger.info(f"Extracting FHIR resource name from table name: {full_table_name}")

        # Extract the last part of the table name after the last period
        table_name = full_table_name.split(".")[-1].replace("fhir_", "")
        logger.info(f"Extracted FHIR resource name: {table_name}")

        return table_name



    @log_entry_exit
    def generate_description(self, fhir_resource_name):
        """ 
            Generates a description for a fhir resource name using an LLM (if available).
            
            args:  fhir_resource_name (str): The name of the FHIR resource.
            returns: str: The generated description for the FHIR resource.
        """

        if not self.llm_model:
            "No description available."  # Fallback

        prompt_template = PromptTemplate(
            input_variables=["table_name"],
            template="""
            Generate a complete description for a BigQuery table that stores FHIR (Fast Healthcare Interoperability Resources) data.  
            The table name (which corresponds to a FHIR resource type) is: {table_name}.
            
            The description should be suitable for use in a BigQuery table schema's OPTIONS(description="...").  
            Therefore, it **MUST NOT** contain newline characters (\\n) or carriage return characters (\\r). Replace any newlines with spaces.

            Output the description ONLY. Do not include any other text or commentary
            """
        )

        try:

            # Format the Prompt template and create our message array
            prompt = prompt_template.format(table_name=fhir_resource_name) 
            messages = [HumanMessage(content=prompt)]

            # Invoke the model
            description = self.llm_model.invoke(input=messages).content

            return description

        except Exception as e:
            logger.error(f"Error generating description for fhir resource: '{fhir_resource_name}, error: {e}")


