import mysql.connector

def fetch_metadata_from_information_schema(db_config):
    """
    Fetch metadata from the MySQL information schema for tables and columns.
    """
    metadata = {}
    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            db_name = db_config['database']
            print(f"Connected to database: {db_name}")
            cursor = connection.cursor()

            # Query to fetch tables
            cursor.execute(f"""
                SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = '{db_name}';
            """)
            tables = cursor.fetchall()

            for (table_name,) in tables:

                # Query to fetch columns
                cursor.execute(f"""
                  SELECT 
                    c.COLUMN_NAME,
                    c.DATA_TYPE,
                    c.COLUMN_KEY,
                    kcu.REFERENCED_TABLE_NAME AS referenced_table,
                    kcu.REFERENCED_COLUMN_NAME AS referenced_column
                FROM 
                    INFORMATION_SCHEMA.COLUMNS AS c
                LEFT JOIN 
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu
                    ON c.TABLE_SCHEMA = kcu.TABLE_SCHEMA
                    AND c.TABLE_NAME = kcu.TABLE_NAME
                    AND c.COLUMN_NAME = kcu.COLUMN_NAME
                WHERE 
                    c.TABLE_SCHEMA = '{db_name}'
                    AND c.TABLE_NAME = '{table_name}';
                """)
                columns = cursor.fetchall()
                
                metadata[table_name] = columns

        return metadata

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")