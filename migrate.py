import csv

"""
You should not need to edit this file unless you are modifying the row counter
break comment at the bottom (to prevent processing of all rows).
"""

import mysql.connector

from custom_functions import craft_value
from migration_config import (MIGRATION_CONFIG, MYSQL_CONFIG, UNIQUE_FIELDS)


def get_mysql_db():
    return mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"]
    )


def get_string_of_table_col_names(table_mappings):
    table_columns = []
    for table_mapping in table_mappings:
        table_columns.append(table_mapping["table_column"])
    return ", ".join(table_columns)


def get_string_tokens(mapping):
    tokens = []
    for _ in range(len(mapping)):
        tokens.append("%s")
    return ", ".join(tokens)


def insert_into_db(table_name, table_mappings, values, cursor):
    table_column_names = get_string_of_table_col_names(table_mappings)
    table_column_value_tokens = get_string_tokens(table_mappings)
    query = f"INSERT INTO {table_name} ({table_column_names}) VALUES " \
            f"({table_column_value_tokens})"

    cursor.execute(query, tuple(values))


def replace_comma_tokens(value):
    return value.replace("(c)", ",")


def insert_new_entry(row, table_name, cursor):
    table_name = table["name"]
    table_mappings = table["mappings"]

    table_column_to_csv_value = {}
    for table_mapping in table_mappings:

        # From the table field we want to get, find the associated CSV value

        table_column = table_mapping["table_column"]
        # "HostUrl" -> "host_url"
        csv_column = table_mapping["csv_column"]

        if csv_column in csv_col_to_index.keys():
            # Table Column --> Row Index -> CSV Value
            row_index = csv_col_to_index[csv_column]
            csv_value = replace_comma_tokens(str(row[row_index]))

            # Address boolean to bit mapping 'f' to 0 and 't' to 1
            if csv_value == 'f':
                csv_value = 0
            elif csv_value == 't':
                csv_value = 1

            if "Nights" in table_column and not csv_value:
                csv_value = 0

            # map["HostUrl"] = {VALUE_IN_CSV}
            table_column_to_csv_value[table_column] = csv_value

        else:
            custom_token = csv_column
            table_column_to_csv_value[table_column] = \
                craft_value(custom_token, table_column_to_csv_value)

        if table_name in UNIQUE_FIELDS and table_column in UNIQUE_FIELDS[table_name].keys():
            set_of_unique_values = UNIQUE_FIELDS[table_name][table_column]
            current_value = table_column_to_csv_value[table_column]

            # Ensuring no duplicates exist for a unique field
            if current_value not in set_of_unique_values:
                set_of_unique_values.add(current_value)

            # Found duplicate of unique field, skipping row
            else:
                return

    insert_into_db(
        table_name, table_mappings, table_column_to_csv_value.values(), cursor)


mydb = get_mysql_db()
mycursor = mydb.cursor()

for csv_config in MIGRATION_CONFIG:

    resource_path = csv_config["resource_path"]
    print(f"Processing resource: '{resource_path}'")

    for table in csv_config["tables"]:

        print(f"  Table: '{table['name']}'")

        with open(resource_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            row_counter = 0
            csv_col_to_index = None
            for row in csvreader:
                if row_counter == 0:
                    # Create and populate csv col -> row index map
                    csv_col_to_index = {}
                    for i in range(len(row)):
                        csv_col_to_index[row[i]] = i
                else:
                    insert_new_entry(row, table, mycursor)
                row_counter += 1

                # You can un-comment this to load a smaller portion of the rows
                # if row_counter >= 5:
                #     break

# This commits all queries to the db, making changes in the DB you set up
print(f"Committing collected queries to database '{MYSQL_CONFIG['database']}.'")
mydb.commit()
print("Migration complete.")
