CSV_FILE_PATH = "resources/listings_no_comma.csv"

"""
❗️ NOTICE❗️

Your configuration should include tables to be populated with a single
CSV file.

MIGRATION_CONFIG should include tables in order of
least dependent (on top) to most dependent (on bottom).
"""
MIGRATION_CONFIG = {
    # Table name (case sensitive)
    "User": {
        # Table column name to CSV column name (case sensitive)
        "ID": "host_id",
        "Name": "host_name",
        "UserName": "{{GENERATE_USERNAME}}",
        "Password": "{{GENERATE_PASSWORD}}"
    }
}

UNIQUE_FIELDS = {
    # Table name (case sensitive)
    "User": {
        # Unique table column name (case sensitive)
        "ID": set()
    }
}

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123",
    "database": "Gr8BnBApplication"
}
