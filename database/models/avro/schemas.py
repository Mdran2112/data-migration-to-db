
EMPLOYEE_SCHEMA = {
    "namespace": "backup.avro",
    "type": "record",
    "name": "Employee",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "datetime", "type": "string"},
        {"name": "department_id", "type": "int"},
        {"name": "job_id", "type": "int"}
    ]
}

DEPARTMENT_SCHEMA = {
    "namespace": "backup.avro",
    "type": "record",
    "name": "Department",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "department", "type": "string"}
    ]
}

JOB_SCHEMA = {
    "namespace": "backup.avro",
    "type": "record",
    "name": "Job",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "job", "type": "string"}
    ]
}
