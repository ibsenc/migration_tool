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
    # print(collected_values)
    return collected_values["Name"][:3] + collected_values["ID"][:3]


# Custom Action for Token: {{GENERATE_PASSWORD}}
def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))

# Custom Action for Token: {{GENERATE_PASSWORD}}
id = 0
def generate_id():
    global id
    result = id + 1
    id = result
    return result

# CUSTOM FUNCTION ROUTER
def craft_value(token, table_column_to_csv_value):
    """
    This function can be modified to include your custom function. This routes
    all functions to the main application
    """

    if token == "{{GENERATE_USERNAME}}":
        return generate_username(table_column_to_csv_value)
    if token == "{{GENERATE_PASSWORD}}":
        return generate_password()
    if token == "{{GENERATE_ID}}":
        return generate_id()
    raise Exception(f"Found unrecognized token '{token}'. Please verify " +
                    "migration config in 'migration_config.py'.")
