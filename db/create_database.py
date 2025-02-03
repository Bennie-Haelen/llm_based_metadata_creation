import sqlite3

PROMPT_DB = "db/prompts.db"

def create_database(db_path: str = PROMPT_DB):

    # Connect to the SQLite database (it will be created if it doesn't exist)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create the prompts table with the desired schema.
    create_table_query = """
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        template TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'prompts' created or already exists.")
    
    # Optionally, insert some initial prompt templates.
    initial_prompts = [
        ('greeting_prompt', 'Hello, {name}! How can I help you today?'),
        ('support_prompt', 'Dear {customer_name}, please describe your issue in detail.')
    ]
    
    insert_query = "INSERT OR IGNORE INTO prompts (name, template) VALUES (?, ?)"
    cursor.executemany(insert_query, initial_prompts)
    connection.commit()
    print("Initial prompts inserted (if they did not exist).")
    
    # Close the cursor and connection.
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_database()
