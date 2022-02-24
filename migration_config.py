"""
❗️ NOTICE❗️

Your configuration should include tables to be populated with a single
CSV file.

MIGRATION_CONFIG should include tables in order of
least dependent (on top) to most dependent (on bottom).
"""
MIGRATION_CONFIG = [
    {
        "resource_path": "resources/listings_no_comma.csv",
        "tables": [
            {
                "name": "User",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "host_id"
                    },
                    {
                        "table_column": "Name",
                        "csv_column": "host_name"
                    },
                    {
                        "table_column": "UserName",
                        "csv_column": "{{GENERATE_USERNAME}}"
                    },
                    {
                        "table_column": "Password",
                        "csv_column": "{{GENERATE_PASSWORD}}"
                    }
                ]
            },
            {
                "name": "Host",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "host_id"
                    },
                    {
                        "table_column": "HostUrl",
                        "csv_column": "host_url"
                    },
                    {
                        "table_column": "HostSince",
                        "csv_column": "host_since"
                    },
                    {
                        "table_column": "HostLocation",
                        "csv_column": "host_location"
                    },
                    {
                        "table_column": "HostAbout",
                        "csv_column": "host_about"
                    },
                    {
                        "table_column": "HostListingsCount",
                        "csv_column": "host_listings_count"
                    },
                    {
                        "table_column": "HostTotalListingsCount",
                        "csv_column": "host_total_listings_count"
                    },
                ]
            },
            {
                "name": "HostRating",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "{{GENERATE_ID}}"
                    },
                    {
                        "table_column": "HostID",
                        "csv_column": "host_id"
                    },
                    {
                        "table_column": "Rating",
                        "csv_column": "review_scores_rating"
                    }
                ]
            }
        ]
    },
    {
        "resource_path": "resources/reviews_no_comma.csv",
        "tables": [
            {
                "name": "User",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "reviewer_id"
                    },
                    {
                        "table_column": "Name",
                        "csv_column": "reviewer_name"
                    },
                    {
                        "table_column": "UserName",
                        "csv_column": "{{GENERATE_USERNAME}}"
                    },
                    {
                        "table_column": "Password",
                        "csv_column": "{{GENERATE_PASSWORD}}"
                    }
                ]
            },
            {
                "name": "Guest",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "reviewer_id"
                    }
                ]
            },
            {
                "name": "Review",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "id"
                    },
                    {
                        "table_column": "Date",
                        "csv_column": "date"
                    },
                    {
                        "table_column": "ReviewerID",
                        "csv_column": "reviewer_id"
                    },
                    {
                        "table_column": "Comments",
                        "csv_column": "comments"
                    },
                    # {
                    #     "table_column": "ListingID",
                    #     "csv_column": "listing_id"
                    # }
                ]
            }
        ]
    }
]

UNIQUE_FIELDS = {
    # Table name (case sensitive)
    "User": {
        # Unique table column name (case sensitive)
        "ID": set()
    },
    "Host": {
        "ID": set()
    },
    "Guest": {
        "ID": set()
    },
    "Review": {
        "ID": set()
    },
    "HostRating": {
        "ID": set()
    }
}

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "Gr8BnBApplication"
}
