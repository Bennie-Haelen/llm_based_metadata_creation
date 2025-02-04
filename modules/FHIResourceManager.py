import json
from langchain.schema import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


from logger_setup import logger, log_entry_exit
from db.get_prompt_by_name import get_prompt_by_name

# This is the max length of the description that can be stored in BigQuery
# for either a column or a table, we did not make this a YAML parameter
# since it is a constant value
CHARACTER_LIMIT = 1024

class FHIRResourceManager:
    """
    This class encapsulates the functionality to manage FHIR resources in the context of BigQuery tables.
    """

    @log_entry_exit
    def __init__(self, llm, full_table_name):
        """
        Initializes the FHIRResourceManager instance.

        Parameters:
        - llm: The language model instance. Used for LLM processing in the class.
        - full_table_name (str): The fully qualified BigQuery table name in the format 
          "project.dataset.table_name".

        Attributes:
        - self.llm_model: Stores the provided language model instance.
        - self._fhir_resource_name: Extracts and stores the FHIR resource name derived 
                                    from the provided BigQuery table name.
        - self._full_table_name: Stores the provided full table name.
        """

        # Store the provided language model instance
        self.llm_model = llm  

        # Store the provided full table name
        self._full_table_name = full_table_name

        # Extract and store the FHIR resource name
        self._fhir_resource_name = self._extract_fhir_resource_name(full_table_name) 



    @property
    def fhir_resource_name(self):
        """
        Read-only property to access the FHIR resource name.

        This property provides access to the extracted FHIR resource name without allowing 
        direct modification. The value is set during object initialization and retrieved when accessed.

        Returns:
        - str: The extracted FHIR resource name.
        """

        # Return the stored FHIR resource name
        return self._fhir_resource_name  



    @property
    def full_table_name(self):
        """     
        Read-only property to access the full table name.

        This property provides access to the full table name without allowing direct modification.
        The value is set during object initialization and retrieved when accessed.

        Returns:
        - str: The full table name in the format "project.dataset.table_name".
        """
        return self._full_table_name
    

    @log_entry_exit  
    def _extract_fhir_resource_name(self, full_table_name: str) -> str:
        """
        Extracts and converts a BigQuery table name into a FHIR resource name.

        This method ensures the input follows the correct format for a fully qualified BigQuery table 
        name (i.e., it contains at least two periods). If the format is invalid, an exception is raised.

        Steps:
        1. Validate that the input contains at least two periods (e.g., "project.dataset.table_name").
        2. Extract the last segment of the table name after the final period.
        3. If the extracted name starts with "fhir_", remove the prefix.
        4. Log the extracted resource name and return it.

        Parameters:
        - full_table_name (str): The fully qualified BigQuery table name in the format 
        "project.dataset.table_name".

        Returns:
        - str: The cleaned FHIR resource name (i.e., table name without "fhir_" prefix).

        Raises:
        - ValueError: If the input does not contain at least two periods, indicating an invalid format.
        """

        logger.info(f"Extracting FHIR resource name from table name: {full_table_name}")

        # Validate input format: Ensure it contains at least two periods
        if full_table_name.count(".") < 2:
            error_message = "Invalid table name format. Expected 'project.dataset.table_name'."
            logger.error(error_message)
            raise ValueError(error_message)

        # Extract the last part of the table name and clean it by removing "fhir_" prefix if present
        resource_name = full_table_name.split(".")[-1].replace("fhir_", "")
        
        logger.info(f"Extracted FHIR resource name: {resource_name}")

        return resource_name



    @log_entry_exit  # Decorator for logging function entry and exit
    def generate_table_description(self):
        """ 
        Generates a description for a FHIR resource name using an LLM. 
        This description is at the resource (or table) level, so it
        describes the resource as a whole.

        This method constructs a prompt dynamically using a stored prompt template and 
        then invokes the LLM model to generate a description of the given FHIR resource.

        Steps:
        1. Ensure the LLM model is initialized; otherwise, return a fallback message.
        2. Retrieve the appropriate prompt template from the database using its name.
        3. Set up a `PromptTemplate` to format the retrieved prompt.
        4. Inject the `fhir_resource_name` into the prompt and construct a message array.
        5. Invoke the LLM model to generate a description.
        6. Log the successful generation and return the description.
        7. Handle any errors gracefully and log them.

        Returns:
        - str: The generated description for the FHIR resource.
        If the LLM model is not available, returns `"No description available."`
        If an error occurs, logs the error and returns `None`.
        """

        # Ensure the LLM model is initialized; otherwise, return a fallback message
        if not self.llm_model:
            return "No description available."  # Fallback

        try:
            # Retrieve the prompt template from the database
            prompt_name = "get_table_description"
            prompt_template_str = get_prompt_by_name(prompt_name)

            # Set up the prompt template with the expected input variable
            prompt_template = PromptTemplate(
                input_variables=["table_name"],
                template=prompt_template_str
            )

            # Format the prompt by injecting the FHIR resource name
            prompt = prompt_template.format(table_name=self.fhir_resource_name) 

            # Create a message array containing the formatted prompt
            messages = [HumanMessage(content=prompt)]

            # Invoke the LLM model to generate a description
            description = self.llm_model.invoke(input=messages).content

            # Log successful retrieval of the description
            logger.info(f"Generated description for FHIR resource '{self._fhir_resource_name}' successfully retrieved.")

            return description

        except Exception as e:
            # Log the error and return None in case of failure
            logger.error(f"Error generating description for FHIR resource '{self._fhir_resource_name}': {e}")
            return None


    

    @log_entry_exit  
    def generate_enriched_schema(self, json_schema):
        """
        This methoid generates an enriched schema by adding column-level 
        descriptionss for a given FHIR resource.

        Args:
        - json_schema (dict): The JSON schema for the FHIR resource.

        Returns:
        - list: The enriched schema with the column descriptions.
        """

        # We use the JSON Output Parser to extract the JSON array from the response
        # Using this parser, we get very predictable results, and we do not have
        # to worry about the structure of the response and extra "bits" emitted
        # by the LLM model
        parser = JsonOutputParser()
        instructions = parser.get_format_instructions()

        logger.info(f"Generating enriched schema for fhir resource: {self._fhir_resource_name}")

        try:
            # Define chunk size (e.g., process 10 fields at a time)
            # Because of the potentially large size of the models, we decided to 
            # use chunking here. This is a common practice when working with large
            # models and large amounts of data. We can adjust the chunk size as needed, 
            # but 10 is a good starting point.
            chunk_size = 10
            logger.info(f"Splitting schema into chunks of {chunk_size} fields...")
            schema_chunks = [json_schema[i:i + chunk_size] for i in range(0, len(json_schema), chunk_size)]
    

            # Retrieve the appropriate prompt template from our prompt database
            prompt_name = "generate_resource_schema_with_descriptions"
            prompt_template_str = get_prompt_by_name(prompt_name)

            # Set up the prompt template with the expected input variables                  
            prompt_template = PromptTemplate(
                input_variables=["input_json_schema", "fhir_resource"],
                template=prompt_template_str)

            # Process each chunk
            enriched_schema = []
            for idx, chunk in enumerate(schema_chunks):
                logger.info(f"Processing chunk {idx + 1}/{len(schema_chunks)}...")

                # Format the prompt with the chunk
                prompt = prompt_template.format(fhir_resource=self.fhir_resource_name, input_json_schema=json.dumps(chunk, indent=2))

                # Create a message array containing the formatted prompt
                messages = [HumanMessage(content=prompt)]
                
                # Send request to LLM
                response = self.llm_model.invoke(input=messages).content

                # Parse response and extend enriched schema
                try:
                    # Use the JSsonOutputParser to extract the JSON array from the response,
                    # and add it to the enriched schema
                    enriched_chunk = parser.parse(response)
                    enriched_schema.extend(enriched_chunk)

                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON for chunk {idx + 1}. error:{e}")

            logger.info("Creation of enriched schema completed successfully...")
            return enriched_schema
            
        except Exception as e:
            logger.error(f"Error generating schema with description for fhir resource: {self._fhir_resource_name}': {e}")




    @log_entry_exit
    def create_sql_from_schema(self, schema_json, table_description, mode):

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

                        Output multiple column statements, do not write multiple ALTER TABLE STATEMENTS, all column alters should be in one statement.

                        Do NOT generate an ALTER COLUMN statement for nested fields.
                        Only output the SQL by itself, no prefix or postfix of any kind.

                    """)
            
        elif mode == "create":
            logger.info("Creating CREATE TABLE SQL statements...")
            prompt_template = PromptTemplate(
                    input_variables=["schema_json", "resource_name", "full_table_name", "table_description"],
                    template="""
                        You are a data engineer who needs to write an CREATE OR REPLACE TABLE query for a new 
                        BigQuery {resource_name} table with name: {full_table_name}. Include descriptions as well.

                        The schema of the table is here:
                        {schema_json}.

                        In the CREATE TABLE statement, include the following table description:
                        "{table_description}"
                        
                        Only output the SQL by itself, no prefix or postfix of any kind.
                        Make sure to handle embedded fields correctly, the generated SQL should be 100 percent in line with the BigQuery syntax
                    """)
        else:
            logger.error(f"Invalid mode specified: {mode}")
            pass
        
        # Create the prompt        
        prompt = prompt_template.format(
            schema_json=schema_json, 
            full_table_name=self.full_table_name, 
            table_description=table_description, 
            resource_name=self.fhir_resource_name)

        # Invoke the model
        messages = [HumanMessage(content=prompt)]
        response = self.llm_model.invoke(input=messages)

        # Return the response
        return response.content