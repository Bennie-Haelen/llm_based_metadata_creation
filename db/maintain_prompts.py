import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Set the page layout to wide mode
st.set_page_config(page_title="Prompt Manager", layout="wide")

PROMPT_DB = "db/prompts.db"
# ----------------------------
# Database Utility Functions
# ----------------------------

def init_db():
    """Initialize the database and create the prompts table if it does not exist."""
    conn = sqlite3.connect(PROMPT_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            template TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_prompts():
    """Retrieve all prompt templates from the database as a pandas DataFrame."""
    conn = sqlite3.connect(PROMPT_DB)
    df = pd.read_sql_query("SELECT id, name, template FROM prompts", conn)
    conn.close()
    return df

def add_prompt(name: str, template: str):
    """Add a new prompt template to the database."""
    conn = sqlite3.connect(PROMPT_DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO prompts (name, template) VALUES (?, ?)", (name, template))
        conn.commit()
        st.success("✅ Prompt added successfully!")
        st.rerun()
    except sqlite3.IntegrityError as e:
        st.error(f"⚠️ Error adding prompt: {e}")
    finally:
        conn.close()

def update_prompt(prompt_id: int, new_name: str, new_template: str):
    """Update an existing prompt template."""
    conn = sqlite3.connect(PROMPT_DB)
    c = conn.cursor()
    try:
        c.execute("UPDATE prompts SET name = ?, template = ? WHERE id = ?", (new_name, new_template, prompt_id))
        conn.commit()
        st.success("✅ Prompt updated successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"⚠️ Error updating prompt: {e}")
    finally:
        conn.close()

def delete_prompt(prompt_id: int):
    """Delete a prompt template from the database."""
    conn = sqlite3.connect(PROMPT_DB)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
        conn.commit()
        st.success("✅ Prompt deleted successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"⚠️ Error deleting prompt: {e}")
    finally:
        conn.close()

# ----------------------------
# Initialize Database
# ----------------------------
init_db()

# ----------------------------
# Streamlit App Layout
# ----------------------------
st.title("📝 Prompt Template Manager")

st.markdown("## 📋 Existing Prompts")

# Read prompts from the database
df_prompts = get_prompts()

# Display Grid at the top
if not df_prompts.empty:
    # Build AgGrid grid options
    gb = GridOptionsBuilder.from_dataframe(df_prompts)
    gb.configure_selection("single", use_checkbox=True)  # Enable single row selection
    grid_options = gb.build()

    # Display the grid
    grid_response = AgGrid(
        df_prompts,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=400,  # Increase height for better visibility
        fit_columns_on_grid_load=True,
    )

    # Get selected rows safely
    selected_rows = grid_response.get("selected_rows", [])

    if isinstance(selected_rows, list) and len(selected_rows) > 0:
        selected_prompt = selected_rows[0]
    elif isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
        selected_prompt = selected_rows.iloc[0].to_dict()
    else:
        selected_prompt = None
else:
    st.info("No prompts available.")
    selected_prompt = None

# ----------------------------
# Editing & Adding Sections Below
# ----------------------------

st.markdown("---")

# Editing Section
st.markdown("## ✏️ Edit Selected Prompt")
if selected_prompt:
    new_name = st.text_input("Prompt Name", value=selected_prompt["name"])
    new_template = st.text_area("Prompt Template", value=selected_prompt["template"], height=250)  # Increased height

    col_upd, col_del = st.columns([1, 1])
    with col_upd:
        if st.button("✅ Update Prompt"):
            if new_name.strip() and new_template.strip():
                update_prompt(selected_prompt["id"], new_name.strip(), new_template.strip())
            else:
                st.error("⚠️ Both the prompt name and template must be provided.")
    with col_del:
        if st.button("🗑️ Delete Prompt"):
            delete_prompt(selected_prompt["id"])

st.markdown("---")

# New Prompt Section
st.markdown("## ➕ Add a New Prompt")

with st.form("add_prompt_form"):
    new_prompt_name = st.text_input("New Prompt Name")
    new_prompt_template = st.text_area("New Prompt Template", height=250)  # Increased height

    submitted = st.form_submit_button("➕ Add Prompt")
    if submitted:
        if new_prompt_name.strip() and new_prompt_template.strip():
            add_prompt(new_prompt_name.strip(), new_prompt_template.strip())
        else:
            st.error("⚠️ Please provide both a prompt name and template.")
