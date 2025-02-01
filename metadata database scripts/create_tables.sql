-- Create the schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS hca_metadata;

-- Drop the tables first
DROP TABLE IF EXISTS hca_metadata.data_column;
DROP TABLE IF EXISTS hca_metadata.data_table;
DROP TABLE IF EXISTS hca_metadata.global_data_concept;
DROP TABLE IF EXISTS hca_metadata.data_product;
DROP TABLE IF EXISTS hca_metadata.sub_domain; 
DROP TABLE IF EXISTS hca_metadata.domain;
DROP TABLE IF EXISTS hca_metadata.data_type;
DROP TABLE IF EXISTS hca_metadata.data_classification;

-- domain table
CREATE TABLE hca_metadata.domain(
    domain_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    domain_name VARCHAR(255) NOT NULL UNIQUE,
    domain_description VARCHAR(1024) NOT NULL
);

-- sub-domain table
CREATE TABLE hca_metadata.sub_domain(
    sub_domain_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sub_domain_name VARCHAR(255) NOT NULL UNIQUE,
    sub_domain_description TEXT,
    domain_id INT NOT NULL,
    CONSTRAINT fk_domain FOREIGN KEY (domain_id) 
        REFERENCES hca_metadata.domain(domain_id)
);

-- data_classification table
CREATE TABLE hca_metadata.data_classification(
    classification_id TINYINT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
    classification_name VARCHAR(255) NOT NULL UNIQUE,
    classification_description VARCHAR(1024) NOT NULL
);

-- data_type table
CREATE TABLE hca_metadata.data_type(
    data_type_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data_type_name VARCHAR(255) NOT NULL UNIQUE,
    category ENUM('Primitive', 'Complex', 'Temporal', 'Geospatial') NOT NULL,
    supports_null BOOLEAN DEFAULT FALSE NOT NULL,
    example_values TEXT 
);

-- data_product table
CREATE TABLE hca_metadata.data_product (
    data_product_id INT AUTO_INCREMENT PRIMARY KEY,
    sub_domain_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_description TEXT,
    version INT NOT NULL,
    is_latest BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (sub_domain_id, product_name, version),
    FOREIGN KEY (sub_domain_id) REFERENCES hca_metadata.sub_domain(sub_domain_id)
);

-- global_data_concept table
CREATE TABLE hca_metadata.global_data_concept(
    global_concept_id INT AUTO_INCREMENT PRIMARY KEY,
    concept_name VARCHAR(255) NOT NULL,
    version INT NOT NULL,
    UNIQUE(concept_name, version),
    context VARCHAR(255) NOT NULL,
    business_definition VARCHAR(1024) NOT NULL,
    data_type_id TINYINT UNSIGNED NOT NULL,
    contains_pii BOOLEAN NOT NULL,
    hippa_compliant BOOLEAN NOT NULL,
    classification_id TINYINT UNSIGNED NOT NULL,
    user_data_level_1_authorization VARCHAR(255),
    user_data_level_2_authorization VARCHAR(255),
    user_data_level_3_authorization VARCHAR(255),
    user_data_level_4_authorization VARCHAR(255),
    notes VARCHAR(2048),
    data_class VARCHAR(255) NULL,
    CONSTRAINT fk_data_classification FOREIGN KEY (classification_id) 
        REFERENCES hca_metadata.data_classification(classification_id),
    CONSTRAINT fk_data_type FOREIGN KEY (data_type_id) 
        REFERENCES hca_metadata.data_type(data_type_id)
);

-- data_table
CREATE TABLE hca_metadata.data_table(
    table_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data_product_id INT NOT NULL,
    table_name VARCHAR(255) NOT NULL UNIQUE,
    business_description TEXT,
    data_governor VARCHAR(255) NOT NULL,
    business_owner VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_data_product_table FOREIGN KEY (data_product_id) 
        REFERENCES hca_metadata.data_product(data_product_id)
);

-- data_column
CREATE TABLE hca_metadata.data_column(
    column_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    column_name VARCHAR(255) NOT NULL,
    business_definition VARCHAR(1024) NOT NULL,
    data_type_id TINYINT UNSIGNED NOT NULL,
    contains_pii BOOLEAN NOT NULL,
    hippa_compliant BOOLEAN NOT NULL,
    classification_id TINYINT UNSIGNED NOT NULL,
    is_primary_key BOOLEAN NOT NULL DEFAULT FALSE,
    is_foreign_key BOOLEAN NOT NULL DEFAULT FALSE,
    referenced_table_id INT NULL,
    reference_columns_id INT NULL,
    notes VARCHAR(2048),
    data_class VARCHAR(255) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_table_column FOREIGN KEY (table_id) 
        REFERENCES hca_metadata.data_table(table_id),
    CONSTRAINT fk_data_type_column FOREIGN KEY (data_type_id) 
        REFERENCES hca_metadata.data_type(data_type_id),
    CONSTRAINT fk_data_classification_data_col FOREIGN KEY (classification_id) 
        REFERENCES hca_metadata.data_classification(classification_id),
    CONSTRAINT fk_referenced_table FOREIGN KEY (referenced_table_id)
        REFERENCES hca_metadata.data_table(table_id),
    CONSTRAINT fk_reference_columns FOREIGN KEY (reference_columns_id)
        REFERENCES hca_metadata.data_column(column_id)
);



-- - ----------------------------------------------------------------------------
--  I N S E R T   S T A T E M E N T S
-- -----------------------------------------------------------------------------
-- Insert BigQuery data types into the data_type table
INSERT INTO hca_metadata.data_type (
    data_type_name, 
    category, 
    supports_null, 
    example_values
)
VALUES
('STRING', 'Primitive', TRUE, 'Example: "Hello, World!"'),
('BYTES', 'Primitive', TRUE, 'Example: B\'1234567890abcdef\''),
('INTEGER', 'Primitive', TRUE, 'Example: 123'),
('FLOAT', 'Primitive', TRUE, 'Example: 123.45'),
('NUMERIC', 'Primitive', TRUE, 'Example: 123456789.123456789'),
('BIGNUMERIC', 'Primitive', TRUE, 'Example: 123456789123456789.123456789123456789'),
('BOOLEAN', 'Primitive', TRUE, 'Example: TRUE or FALSE'),
('DATE', 'Temporal', TRUE, 'Example: 2025-01-01'),
('DATETIME', 'Temporal', TRUE, 'Example: 2025-01-01T12:34:56'),
('TIME', 'Temporal', TRUE, 'Example: 12:34:56'),
('TIMESTAMP', 'Temporal', TRUE, 'Example: 2025-01-01 12:34:56 UTC'),
('GEOGRAPHY', 'Geospatial', TRUE, 'Example: POINT(-122.084, 37.421)'),
('ARRAY', 'Complex', TRUE, 'Example: [1, 2, 3]'),
('STRUCT', 'Complex', TRUE, 'Example: STRUCT("John", 30, TRUE)'),
('JSON', 'Complex', TRUE, 'Example: {"key": "value"}');



-- Insert classifications into the data_classification table
INSERT INTO hca_metadata.data_classification (
    classification_name, 
    classification_description
)
VALUES
('Internal', 'Data intended for internal use only, restricted to authorized personnel.'),
('Public', 'Data that is open and accessible to the public without restrictions.');


--
-- Insert Data in the domain table
--
INSERT INTO hca_metadata.domain (
    domain_name,
    domain_description
)
VALUES
(
    'Global', -- domain_name
    'This domain contains global concepts.' -- domain_description
);


--
-- Insert data in the sub-domain table
--
INSERT INTO hca_metadata.sub_domain (
    sub_domain_name,
    sub_domain_description,
    domain_id
)
VALUES
(
    'Data Concepts', -- sub_domain_name
    'This sub-domain contains information about global data concepts', -- sub_domain_description
    1 -- domain_id (assumes the domain with ID 1 exists in hca_metadata.domain)
);

--
-- Insert data in the data_product table
--
INSERT INTO hca_metadata.data_product (
    sub_domain_id,
    product_name,
    product_description,
    version,
    is_latest
)
VALUES
(
    1, -- sub_domain_id (assumes sub_domain with ID 1 exists in hca_metadata.sub_domain)
    'Global Data Concepts', -- product_name
    'This data product contains global data concepts used throughout areas', -- product_description
    1, -- version (initial version of the data product)
    TRUE -- is_latest (indicates this is the latest version of the product)
);


--
-- Insert data in the global_data_concept table
--
-- Insert into global_data_concept
INSERT INTO hca_metadata.global_data_concept (
    concept_name,
    version,
    context,
    business_definition,
    data_type_id,
    contains_pii,
    hippa_compliant,
    classification_id,
    user_data_level_1_authorization,
    user_data_level_2_authorization,
    user_data_level_3_authorization,
    user_data_level_4_authorization,
    notes,
    data_class
)
VALUES (
    'Patient Identifier', -- concept_name
    1, -- version
    'Patient Identifier', -- context
    'The unique identifier of the patient.', -- business_definition
    1, -- data_type_id (e.g., INT64 from your data_type table)
    TRUE, -- contains_pii (Yes, it contains personally identifiable information)
    TRUE, -- hippa_compliant (Yes, it adheres to HIPAA regulations)
    1, -- classification_id (Sensitive classification)
    'Level 1 Authorization Required', -- user_data_level_1_authorization
    NULL, -- user_data_level_2_authorization
    NULL, -- user_data_level_3_authorization
    NULL, -- user_data_level_4_authorization
    'Ensure this field is properly masked in public reports.', -- notes
    'Demographics' -- data_class
);
