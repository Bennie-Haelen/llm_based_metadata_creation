from pydantic import BaseModel

# Define the expected output schema
class ColumnInfo(BaseModel):
    description: str
    mapped_data_type: str
