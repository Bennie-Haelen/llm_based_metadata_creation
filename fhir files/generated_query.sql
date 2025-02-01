
-- Dynamic SQL generated from the mapping spreadsheet and table schema
SELECT
  nested_0 AS patient_location,
  t.admission_date AS admission_date,
  t.hospital_service_type_text AS hospital_service_type_text,
  nested_1 AS discharge_disposition,
  t.vip_indicator_code AS vip_indicator_code,
  t.fhir_patient_class_code AS fhir_patient_class_code,
  t.discharge_date AS discharge_date,
  t.patient_type AS patient_type,
  t.mt_reason_for_visit_code AS mt_reason_for_visit_code,
  t.mode_of_arrival_code AS mode_of_arrival_code,
  t.hospital_service_type_code AS hospital_service_type_code,
  t.fhir_visit_status AS fhir_visit_status,
  t.reason_for_visit_text AS reason_for_visit_text
FROM
  `your_dataset.your_table` AS t
  LEFT JOIN UNNEST(t.patient_location) AS nested_0
  LEFT JOIN UNNEST(t.discharge_disposition) AS nested_1
