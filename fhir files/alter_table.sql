ALTER TABLE `hca-sandbox.hca_metadata_pot.xxx`
  SET OPTIONS(description="This BigQuery table stores FHIR (Fast Healthcare Interoperability Resources) data for the resource type 'xxx'. It is designed to facilitate the exchange of healthcare information electronically, ensuring interoperability between different healthcare systems. The table includes structured data fields that align with the FHIR standard, allowing for efficient querying and analysis of healthcare data. Each record in the table represents a specific instance of the 'xxx' resource type, capturing relevant attributes and relationships as defined by the FHIR specification. This enables healthcare providers, researchers, and analysts to access and utilize comprehensive healthcare data for improved decision-making and patient care.");
ALTER TABLE `hca-sandbox.hca_metadata_pot.xxx`
  ALTER COLUMN encounter_id SET OPTIONS (description="The \"encounter_id\" field uniquely identifies an encounter within a healthcare system. It is crucial for linking related data across different systems and ensuring continuity of care. This identifier is typically assigned by the healthcare provider's system and is used to track the patient's interactions with healthcare services. It is essential for data integration, reporting, and analytics, allowing for accurate retrieval and analysis of encounter-related information."),
  ALTER COLUMN lastupdated SET OPTIONS (description="The \"lastupdated\" field indicates the most recent date and time when the encounter record was modified. This timestamp is vital for data synchronization and ensuring that the most current information is available across systems. It helps in maintaining data integrity and is often used in auditing processes to track changes over time. Accurate last updated timestamps are crucial for effective data management and interoperability."),
  ALTER COLUMN hl7_message_date_time SET OPTIONS (description="The \"hl7_message_date_time\" field represents the date and time when the HL7 message related to the encounter was generated. This field is important for understanding the sequence of events and ensuring timely communication between systems. It helps in tracking the flow of information and is essential for troubleshooting and auditing purposes. Accurate timestamps are critical for maintaining the integrity of the data exchange process."),
  ALTER COLUMN hl7_message_date_time_UTC SET OPTIONS (description="The \"hl7_message_date_time_UTC\" field provides the date and time of the HL7 message in Coordinated Universal Time (UTC). This standardization is crucial for ensuring consistent interpretation of timestamps across different time zones. It facilitates global interoperability and accurate data exchange, allowing systems to synchronize and process information without time zone discrepancies. This field is essential for maintaining data consistency in international healthcare settings."),
  ALTER COLUMN hl7_message_control_id SET OPTIONS (description="The \"hl7_message_control_id\" field is a unique identifier for an HL7 message, used to track and manage message exchanges between systems. It ensures that each message can be uniquely identified, preventing duplication and aiding in error handling. This control ID is crucial for maintaining the integrity of message transactions and is often used in logging and auditing processes to trace the flow of information."),
  ALTER COLUMN meta_latest_source_date_time SET OPTIONS (description="The \"meta_latest_source_date_time\" field indicates the most recent date and time when the source data for the encounter was updated. This field is important for understanding the currency of the data and ensuring that the most up-to-date information is being used. It plays a critical role in data validation and quality assurance processes, helping to maintain the accuracy and reliability of healthcare data."),
  ALTER COLUMN intermediate_snapshot_creation_date_time SET OPTIONS (description="The \"intermediate_snapshot_creation_date_time\" field represents the date and time when an intermediate snapshot of the encounter data was created. This snapshot is often used for data backup, recovery, and auditing purposes. It provides a point-in-time view of the data, which is essential for tracking changes and ensuring data integrity throughout the data processing lifecycle."),
  ALTER COLUMN final_fhir_write_date_time SET OPTIONS (description="The \"final_fhir_write_date_time\" field indicates the date and time when the encounter data was last written to the FHIR server. This timestamp is crucial for ensuring that the most recent data is available for clinical and operational use. It helps in maintaining data consistency and is often used in auditing processes to verify the timeliness and accuracy of data updates."),
  ALTER COLUMN final_fhir_commit_date_time SET OPTIONS (description="The \"final_fhir_commit_date_time\" field represents the date and time when the encounter data was committed to the FHIR server. This timestamp is essential for ensuring data integrity and consistency, as it marks the point at which the data becomes part of the official record. It is used in auditing and data reconciliation processes to verify that data has been accurately and completely recorded."),
  ALTER COLUMN encounter_version_id SET OPTIONS (description="The \"encounter_version_id\" field is a unique identifier for a specific version of an encounter record. It is used to track changes and manage different versions of the data over time. This versioning is crucial for maintaining a complete history of the encounter, supporting auditing, and ensuring that the correct version of the data is used in clinical and operational decision-making."),
  ALTER COLUMN version_id_fingerprint SET OPTIONS (description="The \"version_id_fingerprint\" field is a unique identifier used to track the version of the FHIR resource. It ensures data integrity and consistency by allowing systems to detect changes or updates to the resource. This field is crucial for maintaining accurate and up-to-date patient records, supporting version control, and facilitating data synchronization across different systems. It is typically generated using a hashing algorithm to create a unique fingerprint of the resource's content."),
  ALTER COLUMN consent_coid SET OPTIONS (description="The \"consent_coid\" field represents the unique identifier for a patient's consent document within the FHIR framework. It is essential for managing patient privacy and ensuring compliance with legal and regulatory requirements. This identifier links the encounter to the specific consent provided by the patient, allowing healthcare providers to access and share information in accordance with the patient's preferences and legal obligations."),
  ALTER COLUMN meta_action_code SET OPTIONS (description="The \"meta_action_code\" field indicates the type of action performed on the FHIR resource, such as creation, update, or deletion. It is a critical component for auditing and tracking changes within healthcare systems. This field helps ensure data accuracy and accountability by providing a clear record of modifications made to the resource, supporting both operational workflows and compliance with data governance policies."),
  ALTER COLUMN hl7_v2_source_interface SET OPTIONS (description="The \"hl7_v2_source_interface\" field identifies the source interface from which the HL7 v2 message originated. It is vital for tracing data flow and ensuring interoperability between different healthcare systems. This field helps in understanding the context and origin of the data, facilitating troubleshooting, and ensuring that information is accurately integrated and processed across various platforms and applications."),
  ALTER COLUMN patient_account_num SET OPTIONS (description="The \"patient_account_num\" field is a unique identifier assigned to a patient's account within a healthcare facility. It is used for billing, administrative, and financial purposes, linking the encounter to the patient's financial records. This field is crucial for managing patient accounts, ensuring accurate billing and reimbursement, and facilitating communication between clinical and financial systems."),
  ALTER COLUMN patient_primary_id SET OPTIONS (description="The \"patient_primary_id\" field represents the primary identifier for a patient within the FHIR system. It is essential for uniquely identifying a patient across different encounters and healthcare settings. This field ensures accurate patient matching and data retrieval, supporting continuity of care, reducing the risk of errors, and enhancing the overall quality of healthcare delivery."),
  ALTER COLUMN network_mnemonic SET OPTIONS (description="The \"network_mnemonic\" field is a shorthand identifier for the healthcare network associated with the encounter. It is used to categorize and manage encounters within larger healthcare systems, facilitating data organization and reporting. This field helps in understanding the network context of the encounter, supporting network-specific workflows, and ensuring efficient resource allocation and management."),
  ALTER COLUMN medical_record_num SET OPTIONS (description="The \"medical_record_num\" field is a unique identifier for a patient's medical record within a healthcare facility. It is crucial for accessing and managing a patient's clinical information, supporting continuity of care, and ensuring accurate documentation. This field links the encounter to the patient's comprehensive medical history, facilitating clinical decision-making and enhancing patient safety."),
  ALTER COLUMN coid SET OPTIONS (description="The \"coid\" field represents a unique identifier for a clinical object or entity within the FHIR system. It is used to link the encounter to specific clinical data or resources, supporting data integration and interoperability. This field is essential for ensuring accurate data retrieval and management, facilitating clinical workflows, and enhancing the overall efficiency of healthcare delivery."),
  ALTER COLUMN facility_mnemonic SET OPTIONS (description="The \"facility_mnemonic\" field is a shorthand identifier for the healthcare facility where the encounter took place. It is used to categorize and manage encounters within larger healthcare systems, supporting data organization and reporting. This field helps in understanding the facility context of the encounter, ensuring efficient resource allocation, and facilitating communication and coordination across different facilities."),
  ALTER COLUMN fhir_visit_status SET OPTIONS (description="The \"fhir_visit_status\" field in a FHIR Encounter resource indicates the current status of the encounter, such as planned, in-progress, or completed. This status is crucial for understanding the stage of the patient's interaction with the healthcare system. It helps in workflow management, resource allocation, and clinical decision-making. Accurate status tracking ensures effective communication among healthcare providers and supports operational efficiency."),
  ALTER COLUMN fhir_patient_class_code SET OPTIONS (description="The \"fhir_patient_class_code\" field represents a coded value that categorizes the patient class within the healthcare setting, such as inpatient, outpatient, or emergency. This classification is essential for resource planning, billing, and reporting. It helps in determining the level of care required and the appropriate setting for the patient's treatment. Consistent use of patient class codes supports interoperability and data exchange across systems."),
  ALTER COLUMN fhir_patient_class_display SET OPTIONS (description="The \"fhir_patient_class_display\" field provides a human-readable representation of the patient class code, such as 'Inpatient' or 'Outpatient'. This display value aids in user interface design and enhances the readability of clinical data for healthcare providers. It ensures that the patient class information is easily understood by clinicians and administrative staff, facilitating effective communication and decision-making."),
  ALTER COLUMN patient_type SET OPTIONS (description="The \"patient_type\" field categorizes the patient based on specific criteria, such as new or established patient, or based on the type of care they are receiving. This classification is important for clinical workflows, billing, and reporting. It helps in identifying the appropriate care pathways and resource allocation for different patient groups. Accurate patient type classification supports efficient healthcare delivery and operational management."),
  ALTER COLUMN admission_type SET OPTIONS (description="The \"admission_type\" field indicates the nature of the patient's admission, such as elective, emergency, or urgent. This information is critical for understanding the context of the encounter and planning the appropriate level of care. It impacts resource allocation, scheduling, and prioritization of services. Accurate admission type classification supports clinical decision-making and operational efficiency in healthcare settings."),
  ALTER COLUMN patient_class_code SET OPTIONS (description="The \"patient_class_code\" field is a coded value that categorizes the patient class, similar to \"fhir_patient_class_code\". It is used to classify patients based on their care setting, such as inpatient or outpatient. This classification is vital for billing, resource management, and reporting. Consistent use of patient class codes ensures interoperability and accurate data exchange across healthcare systems."),
  ALTER COLUMN account_status_code SET OPTIONS (description="The \"account_status_code\" field represents the current status of the patient's account, such as active, closed, or delinquent. This information is crucial for financial management, billing, and reimbursement processes. It helps in tracking the financial status of the patient's account and ensuring timely payment and resolution of outstanding balances. Accurate account status tracking supports efficient revenue cycle management."),
  ALTER COLUMN vip_indicator_code SET OPTIONS (description="The \"vip_indicator_code\" field is used to identify patients who are considered VIPs (Very Important Persons) within the healthcare setting. This designation may affect the level of service and attention provided to the patient. It is important for ensuring that VIP patients receive the appropriate level of care and privacy. Accurate VIP identification supports personalized care and enhances patient satisfaction."),
  ALTER COLUMN financial_class_code SET OPTIONS (description="The \"financial_class_code\" field categorizes the patient's financial responsibility or insurance coverage, such as self-pay, Medicare, or private insurance. This classification is essential for billing, reimbursement, and financial planning. It helps in determining the patient's financial obligations and the appropriate billing processes. Accurate financial class classification supports efficient revenue cycle management and financial reporting."),
  ALTER COLUMN mode_of_arrival_code SET OPTIONS (description="The \"mode_of_arrival_code\" field indicates how the patient arrived at the healthcare facility, such as by ambulance, walk-in, or referral. This information is important for understanding the context of the encounter and planning the appropriate level of care. It impacts resource allocation, triage, and prioritization of services. Accurate mode of arrival tracking supports operational efficiency and effective patient management."),
  ALTER COLUMN accommodation_code SET OPTIONS (description="The \"accommodation_code\" field in a FHIR Encounter resource represents the specific type of accommodation provided to the patient during the encounter. This can include various types of hospital rooms or wards. It is crucial for resource allocation, billing, and patient care planning. The code is typically drawn from a standardized code system to ensure consistency across healthcare systems."),
  ALTER COLUMN accommodation_code_category SET OPTIONS (description="The \"accommodation_code_category\" field categorizes the type of accommodation provided during an encounter. It provides a higher-level classification than the specific accommodation code, aiding in reporting and analysis. This categorization helps in understanding resource utilization patterns and can be used for operational and financial planning."),
  ALTER COLUMN hospital_service_type_code SET OPTIONS (description="The \"hospital_service_type_code\" field identifies the type of service provided during the encounter, such as surgical, medical, or pediatric services. This code is essential for clinical documentation, billing, and resource management. It ensures that the services rendered are accurately captured and categorized for operational and financial purposes."),
  ALTER COLUMN hospital_service_type_text SET OPTIONS (description="The \"hospital_service_type_text\" field provides a human-readable description of the type of service provided during the encounter. This text complements the service type code by offering a more understandable representation, which can be useful for clinical staff and patients to comprehend the nature of the services rendered."),
  ALTER COLUMN admit_source_code SET OPTIONS (description="The \"admit_source_code\" field indicates the source from which the patient was admitted to the healthcare facility, such as a referral from a physician or transfer from another hospital. This information is vital for understanding patient flow, resource allocation, and for analyzing patterns in patient admissions."),
  ALTER COLUMN patient_id SET OPTIONS (description="The \"patient_id\" field uniquely identifies the patient involved in the encounter. It is a critical element for linking the encounter to the patient's medical record, ensuring that all relevant clinical information is associated with the correct individual. This identifier is essential for maintaining continuity of care and for data integrity across healthcare systems."),
  ALTER COLUMN appointment_id SET OPTIONS (description="The \"appointment_id\" field links the encounter to a specific appointment, if applicable. This connection is important for tracking the patient's journey through the healthcare system, ensuring that scheduled services are delivered, and for analyzing appointment adherence and outcomes."),
  ALTER COLUMN account_id SET OPTIONS (description="The \"account_id\" field associates the encounter with a specific financial account, which is used for billing and reimbursement purposes. This linkage is crucial for managing the financial aspects of healthcare delivery, ensuring that services are billed correctly and that payments are tracked accurately."),
  ALTER COLUMN deceased_date_time SET OPTIONS (description="The \"deceased_date_time\" field records the date and time of a patient's death, if applicable, during the encounter. This information is critical for clinical documentation, legal reporting, and for updating the patient's medical record. It ensures that care providers are aware of the patient's status and can adjust care plans accordingly."),
  ALTER COLUMN admission_date SET OPTIONS (description="The \"admission_date\" field in a FHIR Encounter resource represents the date and time when a patient is formally admitted to a healthcare facility. Key Considerations: Data Type: Typically represented as a dateTime data type in FHIR, including time zone. Clinical Significance: Marks the start of the encounter, crucial for determining the duration and for clinical and operational purposes. Billing and Reimbursement: Essential for accurate billing and reimbursement calculations. Clinical Documentation: Used to document the patient's admission time for continuity of care and medical record keeping. Quality Improvement: Can be used to analyze admission patterns and improve patient flow. Relationship to Encounter Period: The \"admission_date\" is closely related to the period element of the Encounter resource, which defines the overall timeframe of the encounter. Special Considerations: Accuracy: Ensuring accurate admission dates is critical for data quality and clinical decision-making."),
  ALTER COLUMN discharge_date SET OPTIONS (description="The \"discharge_date\" field in a FHIR Encounter resource represents the date and time when the patient was officially discharged from the encounter. Key Considerations: Data Type: Typically represented as an instant data type in FHIR, which is a date and time with time zone. Clinical Significance: Marks the end of the encounter, crucial for determining the duration and for various clinical and operational purposes. Billing and Reimbursement: Essential for accurate billing and reimbursement calculations. Clinical Documentation: Used to document the patient's discharge time for continuity of care and medical record keeping. Quality Improvement: Can be used to analyze length of stay, identify potential delays, and improve patient flow. Relationship to Encounter Period: The \"discharge_date\" is closely related to the period element of the Encounter resource, which defines the overall timeframe of the encounter. S"),
  ALTER COLUMN is_valid_date_ind SET OPTIONS (description="The \"is_valid_date_ind\" field indicates whether the associated date fields in the FHIR Encounter resource are valid and reliable. Key Considerations: Data Type: Boolean, representing true or false. Clinical Significance: Ensures data integrity by confirming the validity of critical date fields such as admission and discharge dates. Data Quality: Helps in identifying and flagging potential data entry errors or inconsistencies. Operational Use: Can be used in data validation processes to ensure accurate reporting and analysis. Special Considerations: Implementation: The criteria for determining validity should be clearly defined and consistently applied. Impact: Invalid dates can affect clinical decision-making, billing, and reporting, making this indicator crucial for maintaining data quality."),
  ALTER COLUMN alt_admission_date_time SET OPTIONS (description="The \"alt_admission_date_time\" field provides an alternative representation of the admission date and time in a FHIR Encounter resource. Key Considerations: Data Type: Typically represented as a dateTime data type in FHIR, including time zone. Clinical Significance: Offers flexibility in capturing admission times from different systems or formats, ensuring comprehensive data capture. Data Integration: Useful in scenarios where data is aggregated from multiple sources with varying date formats. Special Considerations: Consistency: Ensure that the alternative date aligns with the primary admission date to avoid discrepancies. Usage: Primarily used for data reconciliation and integration purposes, rather than direct clinical decision-making."),
  ALTER COLUMN hl7_admission_date_time SET OPTIONS (description="The \"hl7_admission_date_time\" field captures the admission date and time as represented in HL7 messaging standards within a FHIR Encounter resource. Key Considerations: Data Type: Typically represented as a dateTime data type in FHIR, including time zone. Interoperability: Facilitates data exchange between systems using HL7 standards, ensuring consistent and accurate data transfer. Clinical Significance: Marks the start of the encounter, crucial for determining the duration and for clinical and operational purposes. Special Considerations: Alignment: Ensure that the HL7 date aligns with other admission date fields to maintain data consistency. Usage: Primarily used in systems that rely on HL7 messaging for data exchange, supporting interoperability and data integration."),
  ALTER COLUMN alt_discharge_date_time SET OPTIONS (description="The \"alt_discharge_date_time\" field provides an alternative representation of the discharge date and time in a FHIR Encounter resource. Key Considerations: Data Type: Typically represented as a dateTime data type in FHIR, including time zone. Clinical Significance: Offers flexibility in capturing discharge times from different systems or formats, ensuring comprehensive data capture. Data Integration: Useful in scenarios where data is aggregated from multiple sources with varying date formats. Special Considerations: Consistency: Ensure that the alternative date aligns with the primary discharge date to avoid discrepancies. Usage: Primarily used for data reconciliation and integration purposes, rather than direct clinical decision-making."),
  ALTER COLUMN hl7_discharge_date_time SET OPTIONS (description="The \"hl7_discharge_date_time\" field captures the discharge date and time as represented in HL7 messaging standards within a FHIR Encounter resource. Key Considerations: Data Type: Typically represented as a dateTime data type in FHIR, including time zone. Interoperability: Facilitates data exchange between systems using HL7 standards, ensuring consistent and accurate data transfer. Clinical Significance: Marks the end of the encounter, crucial for determining the duration and for various clinical and operational purposes. Special Considerations: Alignment: Ensure that the HL7 date aligns with other discharge date fields to maintain data consistency. Usage: Primarily used in systems that rely on HL7 messaging for data exchange, supporting interoperability and data integration."),
  ALTER COLUMN reason_for_visit_text SET OPTIONS (description="The \"reason_for_visit_text\" field in a FHIR Encounter resource captures the textual description of the reason for the patient's visit. Key Considerations: Data Type: String, allowing for free-text entry. Clinical Significance: Provides context for the encounter, aiding in clinical decision-making and care planning. Documentation: Essential for clinical documentation, offering insights into the patient's presenting complaints or conditions. Special Considerations: Standardization: While free-text allows flexibility, using standardized terminologies can enhance data consistency and interoperability. Usage: Primarily used for clinical documentation and communication, supporting the understanding of the patient's healthcare needs."),
  ALTER COLUMN mt_reason_for_visit_code SET OPTIONS (description="The \"mt_reason_for_visit_code\" field in a FHIR Encounter resource represents a coded value for the reason for the patient's visit. Key Considerations: Data Type: String, typically referencing a standardized coding system such as SNOMED CT or ICD. Clinical Significance: Provides a structured and standardized way to capture the reason for the encounter, facilitating data analysis and interoperability. Documentation: Complements the textual description, offering a concise and consistent representation of the visit reason. Special Considerations: Coding System: Ensure the use of appropriate and up-to-date coding systems to maintain data accuracy and relevance. Usage: Primarily used for data analysis, reporting, and interoperability, supporting efficient healthcare delivery and decision-making."),
  ALTER COLUMN insert_timestamp SET OPTIONS (description="The 'insert_timestamp' field captures the exact date and time when the record was inserted into the system, ensuring data integrity and traceability.");