import mysql.connector
from typing import List
import json

# Define a custom Python type for the global_data_concept table
class GlobalDataConcept:
    def __init__(
        self,
        global_concept_id,
        concept_name,
        data_product_id,
        context,
        business_definition,
        data_type_id,
        data_type_name,
        contains_pii,
        hippa_compliant,
        classification_id,
        user_data_level_1_authorization,
        user_data_level_2_authorization,
        user_data_level_3_authorization,
        user_data_level_4_authorization,
        notes,
        data_class,
    ):
        self.global_concept_id = global_concept_id
        self.concept_name = concept_name
        self.data_product_id = data_product_id
        self.context = context
        self.business_definition = business_definition
        self.data_type_id = data_type_id
        self.data_type_name = data_type_name
        self.contains_pii = bool(contains_pii)
        self.hippa_compliant = bool(hippa_compliant)
        self.classification_id = classification_id
        self.user_data_level_1_authorization = user_data_level_1_authorization
        self.user_data_level_2_authorization = user_data_level_2_authorization
        self.user_data_level_3_authorization = user_data_level_3_authorization
        self.user_data_level_4_authorization = user_data_level_4_authorization
        self.notes = notes
        self.data_class = data_class

    def __repr__(self):
        return (
            f"GlobalDataConcept("
            f"global_concept_id={self.global_concept_id}, "
            f"concept_name='{self.concept_name}', "
            f"data_product_id={self.data_product_id}, "
            f"context='{self.context}', "
            f"business_definition='{self.business_definition}', "
            f"data_type_id={self.data_type_id}, "
            f"data_type_name='{self.data_type_name}', "
            f"contains_pii={self.contains_pii}, "
            f"hippa_compliant={self.hippa_compliant}, "
            f"classification_id={self.classification_id}, "
            f"user_data_level_1_authorization='{self.user_data_level_1_authorization}', "
            f"user_data_level_2_authorization='{self.user_data_level_2_authorization}', "
            f"user_data_level_3_authorization='{self.user_data_level_3_authorization}', "
            f"user_data_level_4_authorization='{self.user_data_level_4_authorization}', "
            f"notes='{self.notes}', "
            f"data_class='{self.data_class}'"
            f")"
        )

    def to_json(self):
        """Convert the object to a JSON-compatible dictionary."""
        return {
            "global_concept_id": self.global_concept_id,
            "concept_name": self.concept_name,
            "data_product_id": self.data_product_id,
            "context": self.context,
            "business_definition": self.business_definition,
            "data_type_id": self.data_type_id,
            "data_type_name": self.data_type_name,
            "contains_pii": self.contains_pii,
            "hippa_compliant": self.hippa_compliant,
            "classification_id": self.classification_id,
            "user_data_level_1_authorization": self.user_data_level_1_authorization,
            "user_data_level_2_authorization": self.user_data_level_2_authorization,
            "user_data_level_3_authorization": self.user_data_level_3_authorization,
            "user_data_level_4_authorization": self.user_data_level_4_authorization,
            "notes": self.notes,
            "data_class": self.data_class,
        }

def fetch_global_data_concepts(db_config) -> List[GlobalDataConcept]:
    connection = None
    cursor = None
    global_data_concepts = []
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute queries
        cursor = connection.cursor()

        # Define the query to read the global_data_concept table
        query = """
        SELECT 
            global_concept_id,
            concept_name,
            version,
            context,
            business_definition,
            B.data_type_id as data_type_id,
            B.data_type_name as data_type_name,
            contains_pii,
            hippa_compliant,
            classification_id,
            user_data_level_1_authorization,
            user_data_level_2_authorization,
            user_data_level_3_authorization,
            user_data_level_4_authorization,
            notes,
            data_class
        FROM 
            hca_metadata.global_data_concept A
        INNER JOIN
            hca_metadata.data_type B
            ON A.data_type_id = B.data_type_id;
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows into custom Python objects
        for row in rows:
            global_data_concept = GlobalDataConcept(*row)
            global_data_concepts.append(global_data_concept)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return global_data_concepts

def global_data_concepts_to_json(global_data_concepts: List[GlobalDataConcept]) -> str:
    """Convert a list of GlobalDataConcept objects into a JSON array string."""
    return json.dumps([concept.to_json() for concept in global_data_concepts], indent=4)
