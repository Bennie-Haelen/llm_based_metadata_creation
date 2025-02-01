import mysql.connector
from typing import List

# Define a custom Python type for the data_type table
class DataType:
    def __init__(self, data_type_id, data_type_name, category, supports_null, example_values):
        self.data_type_id = data_type_id
        self.data_type_name = data_type_name
        self.category = category
        self.supports_null = supports_null
        self.example_values = example_values

    def __repr__(self):
        return (
            f"DataType("
            f"data_type_id={self.data_type_id}, "
            f"data_type_name='{self.data_type_name}', "
            f"category='{self.category}', "
            f"supports_null={self.supports_null}, "
            f"example_values='{self.example_values}')"
        )
    
def fetch_data_types(db_config) -> List[DataType]:
    connection = None
    cursor = None
    data_types = []
    try:

        # Connect to the database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute queries
        cursor = connection.cursor()

        # Define the query to read the data_type table
        query = """
        SELECT 
            data_type_id,
            data_type_name,
            category,
            supports_null,
            example_values
        FROM 
            hca_metadata.data_type;
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows into custom Python objects
        for row in rows:
            data_type = DataType(*row)
            data_types.append(data_type)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return data_types    