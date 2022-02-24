import random
import string


"""
These functions are meant to generate values based on the values of the
migration config.

Example usage:

MIGRATION_CONFIG = {
    "User": {
        "UserName": "{{GENERATE_USERNAME}}",
        "Password": "{{GENERATE_PASSWORD}}"
    }
}
"""


# CUSTOM FUNCTIONS


# Custom Action for Token: {{GENERATE_USERNAME}}
def generate_username(collected_values):
    return collected_values["Name"][:3] + collected_values["ID"][:3]


# Custom Action for Token: {{GENERATE_PASSWORD}}
def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))


# Custom Action for Token: {{GENERATE_AVERAGE_RATING}}
def generate_average_rating(collected_values, cursor):
    host_id = collected_values["HostID"]

    host_count_query = f"SELECT COUNT(*) FROM HostRating WHERE HostID = {host_id};"
    cursor.execute(host_count_query)
    host_rating_count_results = cursor.fetchone()

    if (host_rating_count_results[0] > 0):
        return None

    host_average_query = f"SELECT AVG(Score) FROM ListingRating WHERE ScoreType = 'Rating' AND HostID = {host_id};"
    cursor.execute(host_average_query)
    select_average_host_rating_results = cursor.fetchone()

    return select_average_host_rating_results[0]


# CUSTOM FUNCTION ROUTER
def craft_value(token, table_column_to_csv_value, cursor=None):
    """
    This function can be modified to include your custom function. This routes
    all functions to the main application
    """

    if token == "{{GENERATE_USERNAME}}":
        return generate_username(table_column_to_csv_value)
    if token == "{{GENERATE_PASSWORD}}":
        return generate_password()
    if token == "{{GENERATE_AVERAGE_RATING}}":
        return generate_average_rating(table_column_to_csv_value, cursor)
    raise Exception(f"Found unrecognized token '{token}'. Please verify " +
                    "migration config in 'migration_config.py'.")
