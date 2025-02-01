import json
import os
import mysql.connector


def read_fhir_bundle(file_path):
    """Read and parse a FHIR bundle JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def extract_patient_data(bundle):
    """Extract relevant patient information and other resources from FHIR bundle."""
    patient_data = {
        'resources': {
            'Patient': [],
            'Encounter': [],
            'Condition': [],
            'MedicationRequest': [],
            'Procedure': [],
        }
    }
    
    for entry in bundle.get('entry', []):
        resource = entry.get('resource', {})
        resource_type = resource.get('resourceType')
        
        if resource_type in patient_data['resources']:
            patient_data['resources'][resource_type].append(resource)
    
    return patient_data


def create_tables(cursor):
    """Create necessary tables in MySQL database."""
    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id VARCHAR(255) PRIMARY KEY,
            birth_date DATE,
            gender VARCHAR(50),
            first_name VARCHAR(255),
            last_name VARCHAR(255)
        )
    """)
    
    # Encounters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encounters (
            id VARCHAR(255) PRIMARY KEY,
            patient_id VARCHAR(255),
            encounter_date DATE,
            encounter_type VARCHAR(255),
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    
    # Conditions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conditions (
            id VARCHAR(255) PRIMARY KEY,
            patient_id VARCHAR(255),
            encounter_id VARCHAR(255),
            code VARCHAR(50),
            description TEXT,
            onset_date DATE,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (encounter_id) REFERENCES encounters(id)
        )
    """)

    # Medications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id VARCHAR(255) PRIMARY KEY,
            patient_id VARCHAR(255),
            medication_code VARCHAR(50),
            medication_description TEXT,
            status VARCHAR(50),
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    # Procedures table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS procedures (
            id VARCHAR(255) PRIMARY KEY,
            patient_id VARCHAR(255),
            procedure_code VARCHAR(50),
            procedure_description TEXT,
            performed_date DATE,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)


def insert_patient(cursor, patient):
    """Insert patient data into MySQL."""
    try:
        sql = """
            INSERT INTO patients (id, birth_date, gender, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        name = patient.get('name', [{}])[0]
        values = (
            patient.get('id'),
            patient.get('birthDate'),
            patient.get('gender'),
            name.get('given', [''])[0],
            name.get('family', '')
        )
        print(f"Inserting patient with id: {patient.get('id')}")
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"Error inserting patient: {err}")


def insert_encounter(cursor, encounter):
    """Insert encounter data into MySQL."""
    try:
        patient_id = encounter.get('subject', {}).get('reference', '').split('/')[-1]
        patient_id = patient_id.replace("urn:uuid:", "")
        
        sql = """
            INSERT INTO encounters (id, patient_id, encounter_date, encounter_type)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            encounter.get('id'),
            patient_id,
            encounter.get('period', {}).get('start'),
            encounter.get('type', [{}])[0].get('text', '')
        )
        print(f"Inserting encounter with patient_id: {patient_id}")
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"Error inserting encounter: {err}")


def insert_condition(cursor, condition):
    """Insert condition data into MySQL."""
    try:
        patient_id = condition.get('subject', {}).get('reference', '').split('/')[-1]
        patient_id = patient_id.replace("urn:uuid:", "")
        encounter_id = condition.get('encounter', {}).get('reference', '').split('/')[-1]
        encounter_id = encounter_id.replace("urn:uuid:", "")
        
        sql = """
            INSERT INTO conditions (id, patient_id, encounter_id, code, description, onset_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            condition.get('id'),
            patient_id,
            encounter_id,
            condition.get('code', {}).get('coding', [{}])[0].get('code'),
            condition.get('code', {}).get('coding', [{}])[0].get('display'),
            condition.get('onsetDateTime')
        )
        print(f"Inserting condition with patient_id: {patient_id} and encounter_id: {encounter_id}")
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"Error inserting condition: {err}")


def insert_medication(cursor, medication):
    """Insert medication data into MySQL."""
    try:
        patient_id = medication.get('subject', {}).get('reference', '').split('/')[-1]
        patient_id = patient_id.replace("urn:uuid:", "")
        
        sql = """
            INSERT INTO medications (id, patient_id, medication_code, medication_description, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            medication.get('id'),
            patient_id,
            medication.get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('code'),
            medication.get('medicationCodeableConcept', {}).get('coding', [{}])[0].get('display'),
            medication.get('status')
        )
        print(f"Inserting medication with patient_id: {patient_id}")
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"Error inserting medication: {err}")


def insert_procedure(cursor, procedure):
    """Insert procedure data into MySQL."""
    try:
        patient_id = procedure.get('subject', {}).get('reference', '').split('/')[-1]
        patient_id = patient_id.replace("urn:uuid:", "")
        
        sql = """
            INSERT INTO procedures (id, patient_id, procedure_code, procedure_description, performed_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            procedure.get('id'),
            patient_id,
            procedure.get('code', {}).get('coding', [{}])[0].get('code'),
            procedure.get('code', {}).get('coding', [{}])[0].get('display'),
            procedure.get('performedDateTime')
        )
        print(f"Inserting procedure with patient_id: {patient_id}")
        cursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"Error inserting procedure: {err}")


def main():
    # Configure MySQL connection
    db_config = {
        'host': '34.30.224.53',
        'user': 'root',
        'password': 'de08NT22244',
        'database': 'synthea'
    }
    
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Process FHIR files
    fhir_directory = '../synthea/output/fhir'
    for filename in os.listdir(fhir_directory):
        if filename.endswith('.json') and not filename.startswith('hospital') and not filename.startswith('practitioner'):
            file_path = os.path.join(fhir_directory, filename)
            bundle = read_fhir_bundle(file_path)
            patient_data = extract_patient_data(bundle)
            
            for patient in patient_data['resources']['Patient']:
                insert_patient(cursor, patient)
            conn.commit()
            
            for encounter in patient_data['resources']['Encounter']:
                insert_encounter(cursor, encounter)
            
            for condition in patient_data['resources']['Condition']:
                insert_condition(cursor, condition)

            for medication in patient_data['resources']['MedicationRequest']:
                insert_medication(cursor, medication)

            for procedure in patient_data['resources']['Procedure']:
                insert_procedure(cursor, procedure)
            
            conn.commit()
    
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
