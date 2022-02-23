import csv

"""
You should not need to edit this file unless you are modifying the row counter
break comment at the bottom (to prevent processing of all rows).
"""

import mysql.connector

from custom_functions import craft_value
from migration_config import (CSV_FILE_PATH, MIGRATION_CONFIG, MYSQL_CONFIG)


def get_mysql_db():
    return mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        database=MYSQL_CONFIG["database"]
    )


def get_string_of_table_col_names(mapping):
    return ", ".join(mapping.keys())


def get_string_tokens(mapping):
    tokens = []
    for _ in range(len(mapping)):
        tokens.append("%s")
    return ", ".join(tokens)


def insert_into_db(mappings, values, cursor):
    table_column_names = get_string_of_table_col_names(mappings)
    table_column_value_tokens = get_string_tokens(mappings)
    query = f"INSERT IGNORE INTO {table_name} ({table_column_names}) VALUES " \
            f"({table_column_value_tokens})"

    cursor.execute(query, tuple(values))


def replace_comma_tokens(value):
    return value.replace("(c)", ",")


def insert_new_entry(row, table_name, cursor):
    table_mappings = MIGRATION_CONFIG[table_name]

    table_column_to_csv_value = {}
    for table_column_name in table_mappings:

        # From the table field we want to get, find the associated CSV value

        # "HostUrl" -> "host_url"
        csv_column_name = table_mappings[table_column_name]

        if csv_column_name in csv_col_to_index.keys():
            # "host_url" -> 9
            row_index = csv_col_to_index[csv_column_name]
            # 9 -> {VALUE_IN_CSV}
            csv_value = replace_comma_tokens(str(row[row_index]))
            # map["HostUrl"] = {VALUE_IN_CSV}
            table_column_to_csv_value[table_column_name] = csv_value
        else:
            custom_token = csv_column_name
            table_column_to_csv_value[table_column_name] = \
                craft_value(custom_token, table_column_to_csv_value)

    insert_into_db(table_mappings, table_column_to_csv_value.values(), cursor)


mydb = get_mysql_db()
mycursor = mydb.cursor()

# Loop through tables
for table_name in MIGRATION_CONFIG.keys():
    with open(CSV_FILE_PATH, newline='') as csvfile:
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
                insert_new_entry(row, table_name, mycursor)
            row_counter += 1

            # You can un-comment this to load a smaller portion of the rows
            # if row_counter >= 5:
            #     break

# This commits all queries to the db, making changes in the DB you set up
mydb.commit()
