import csv

"""
You should not need to edit this file unless you are modifying the row counter
break comment at the bottom (to prevent processing of all rows).
"""

import mysql.connector

from custom_functions import craft_value
from migration_config import (MIGRATION_CONFIG, MYSQL_CONFIG, UNIQUE_FIELDS)


unique_amenities = set()


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


def get_string_tokens(num_tokens):
    tokens = []
    for _ in range(num_tokens):
        tokens.append("%s")
    return ", ".join(tokens)


def execute_insert_query(values, table_name, table_col_names, cursor):
    table_column_value_tokens = get_string_tokens(len(values))
    query = f"INSERT INTO {table_name} ({table_col_names}) VALUES " \
            f"({table_column_value_tokens})"

    cursor.execute(query, values)


def insert_into_db(table_name, table_mappings, table_column_to_csv_value, cursor):

    if table_name == "ListingRating":
        rating_columns = ["Rating", "Accuracy", "Cleanliness", "Checkin", "Communication", "Location", "Value"]
        for temp_rating_column in rating_columns:
            host_id = table_column_to_csv_value["HostID"]
            listing_id = table_column_to_csv_value["ListingID"]

            score = table_column_to_csv_value[temp_rating_column]
            score = score if score else None

            values = (listing_id, host_id, score, temp_rating_column)
            table_col_names = "ListingID, HostID, Score, ScoreType"
            execute_insert_query(values, table_name, table_col_names, cursor)

    else:
        values = tuple(table_column_to_csv_value.values())
        table_col_names = get_string_of_table_col_names(table_mappings)
        execute_insert_query(values, table_name, table_col_names, cursor)


def replace_comma_tokens(value):
    return value.replace("(c)", ",")


def extract_foreach_values(list_string, cursor):
    list_string = list_string.replace('["', "")
    list_string = list_string.replace('"]', "")
    values = list_string.split('", "')

    unique_values = []
    for value in values:
        if value not in unique_amenities:
            unique_values.append(value)
            unique_amenities.add(value)

    amenity_ids = []
    for unique_value in unique_values:
        # Insert into Amenity Table
        cursor.execute(f"INSERT INTO Amenity (Title) values (\"{unique_value}\");")
        cursor.execute("SELECT LAST_INSERT_ID()")
        create_amenity_result = cursor.fetchone()[0]
        amenity_ids.append(create_amenity_result)

    return amenity_ids


def insert_new_entry(row, table_name, cursor):
    table_name = table["name"]
    table_mappings = table["mappings"]

    foreach_values = None
    foreach_column = None

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

            if csv_value == "":
                csv_value = None

            if csv_value and len(csv_value) > 0 and csv_value[0] == "$":
                csv_value = csv_value.replace("$", "").replace(",", "")

            if csv_value and table_column in ["Name", "Description", "NeighborhoodOverview"]:
                csv_value = str(csv_value.encode("utf-8").decode('utf-8', 'ignore').encode("utf-8"))[2:-1]

            # Maps 'f' to 0 and 't' to 1
            if csv_value == 'f':
                csv_value = 0
            elif csv_value == 't':
                csv_value = 1

            # map["HostUrl"] = {VALUE_IN_CSV}
            table_column_to_csv_value[table_column] = csv_value

            if "foreach" in table_mapping.keys() and table_mapping["foreach"]:
                foreach_column = table_column
                foreach_values = extract_foreach_values(csv_value, cursor)

        else:
            custom_token = csv_column
            custom_value = craft_value(custom_token, table_column_to_csv_value, cursor)

            if (not custom_value):
                return

            table_column_to_csv_value[table_column] = custom_value     

        if table_name in UNIQUE_FIELDS and table_column in UNIQUE_FIELDS[table_name].keys():
            set_of_unique_values = UNIQUE_FIELDS[table_name][table_column]
            current_value = table_column_to_csv_value[table_column]

            # Ensuring no duplicates exist for a unique field
            if current_value not in set_of_unique_values:
                set_of_unique_values.add(current_value)

            # Found duplicate of unique field, skipping row
            else:
                return

    if not foreach_column:
        insert_into_db(
            table_name, table_mappings, table_column_to_csv_value, cursor)

    else:
        for foreach_value in foreach_values:
            table_column_to_csv_value[foreach_column] = foreach_value
            insert_into_db(table_name, table_mappings, table_column_to_csv_value, cursor)


mydb = get_mysql_db()
mycursor = mydb.cursor()

for csv_config in MIGRATION_CONFIG:

    resource_path = csv_config["resource_path"]
    print(f"Processing resource: '{resource_path}'")

    for table in csv_config["tables"]:

        print(f"  - Table: '{table['name']}'")

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

                # # You can un-comment this to load a smaller portion of the rows
                # if row_counter >= 5:
                #     break
        print(f"  - Committing collected queries for table '{table['name']}' to database '{MYSQL_CONFIG['database']}.'")
        mydb.commit()

# This commits all queries to the db, making changes in the DB you set up
print("Migration complete.")
