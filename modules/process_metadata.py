from sentence_transformers import SentenceTransformer, util


from modules.DataType import fetch_data_types
from modules.GlobalDataConcept import fetch_global_data_concepts
from modules.hca_metadata_config import DB_CONFIG as HCA_METADATA_DB_CONFIG
from modules.llm_utils import generate_table_description, generate_column_description

def find_best_match(model, column_name: str, concept_embeddings, global_concepts: list):
    """
    Find the best matching global concept for a given column name using embeddings.
    """
    column_embedding = model.encode(column_name)
    scores = util.cos_sim(column_embedding, concept_embeddings)
    best_match_idx = scores.argmax()
    best_match_score = scores[0, best_match_idx].item()
    return global_concepts[best_match_idx] if best_match_score > 0.7 else None


def process_metadata(metadata):
    """
    Process metadata to generate descriptions for tables and columns using LangChain.
    """
    # Load pre-trained model for embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Fetch data types and global data concepts
    existing_data_types = fetch_data_types(HCA_METADATA_DB_CONFIG)
    global_data_concepts = fetch_global_data_concepts(HCA_METADATA_DB_CONFIG)

    print(f"global_data_concepts: {global_data_concepts}")

    concept_embeddings = model.encode([concept.concept_name for concept in global_data_concepts])

    schema_descriptions = {}

    for table_name, columns in metadata.items():
        print(f"Processing table: {table_name}")
        table_description = generate_table_description(table_name)
        schema_descriptions[table_name] = {"description": table_description, "columns": {}}

        for column_name, data_type, column_key,  referenced_table, referenced_column in columns:

            is_primary_key = column_key == "PRI"
            contains_pii = False
            hipadd_compliant = False
            is_foreign_key = referenced_table is not None
            best_match = find_best_match(model, column_name, concept_embeddings, global_data_concepts)

            if best_match:
                schema_descriptions[table_name]["columns"][column_name] = {
                    "is_primary_key": is_primary_key,
                    "description": best_match.business_definition,
                    "mapped_data_type": best_match.data_type_name,
                    "used_global_concept": True,
                    "contains_pii": best_match.contains_pii,
                    "hippa_compliant": best_match.hippa_compliant,
                    "is_foreign_key": is_foreign_key,
                    "referenced_table": referenced_table,
                    "referenced_column": referenced_column
                }
            else:
                column_info = generate_column_description(
                    table_name, column_name, data_type, [dt.data_type_name for dt in existing_data_types]
                )
                schema_descriptions[table_name]["columns"][column_name] = {
                    "is_primary_key": is_primary_key,
                    "description": column_info.description,
                    "mapped_data_type": column_info.mapped_data_type,
                    "used_global_concept": False,
                    "contains_pii": contains_pii,
                    "hippa_compliant": hipadd_compliant,
                    "is_foreign_key": is_foreign_key,
                    "referenced_table": referenced_table,
                    "referenced_column": referenced_column
                }

        # Uncomment the following line to process all tables
        #break

    return schema_descriptions
