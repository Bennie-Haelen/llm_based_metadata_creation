import sqlite3

PROMPT_DB = "db/prompts.db"

def get_prompt_by_name(name: str):
    """Retrieve a prompt's template by its name."""
    conn = sqlite3.connect(PROMPT_DB)
    c = conn.cursor()

    c.execute("SELECT template FROM prompts WHERE name = ?", (name,))
    row = c.fetchone()
    
    conn.close()
    
    if row:
        return row[0]  # Return the template text
    else:
        return None  # Return None if no prompt is found

