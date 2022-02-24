"""
❗️ NOTICE❗️

Your configuration should include tables to be populated with a single
CSV file.

MIGRATION_CONFIG should include tables in order of
least dependent (on top) to most dependent (on bottom).
"""
MIGRATION_CONFIG = [
    {
        "resource_path": "resources/neighbourhoods_no_comma.csv",
        "tables": [
            {
                "name": "Neighborhood",
                "mappings": [
                    {
                        "table_column": "Neighborhood",
                        "csv_column": "neighbourhood"
                    },
                    {
                        "table_column": "NeighborhoodGroup",
                        "csv_column": "neighbourhood_group"
                    }
                ]
            }
        ]
    },
    {
        "resource_path": "resources/listings_no_comma.csv",
        "tables": [
            {
                "name": "Amenity",
                "mappings": [
                    {
                        "table_column": "Title",
                        "csv_column": "amenities",
                        "foreach": True
                    }
                ]
            },
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
                "resource_path": "resources/listings_no_comma.csv",
                "name": "Listing",
                "mappings": [
                    {
                        "table_column": "ID",
                        "csv_column": "id"
                    },
                    {
                        "table_column": "ListingUrl",
                        "csv_column": "listing_url"
                    },
                    {
                        "table_column": "Name",
                        "csv_column": "name"
                    },
                    {
                        "table_column": "Description",
                        "csv_column": "description"
                    },
                    {
                        "table_column": "NeighborhoodOverview",
                        "csv_column": "neighborhood_overview"
                    },
                    {
                        "table_column": "PictureUrl",
                        "csv_column": "picture_url"
                    },
                    {
                        "table_column": "HostID",
                        "csv_column": "host_id"
                    },
                    {
                        "table_column": "Neighborhood",
                        "csv_column": "neighbourhood_cleansed"
                    },
                    {
                        "table_column": "Accommodates",
                        "csv_column": "accommodates"
                    },
                    {
                        "table_column": "Bathrooms",
                        "csv_column": "bathrooms"
                    },
                    {
                        "table_column": "Bedrooms",
                        "csv_column": "bedrooms"
                    },
                    {  # Processed
                        "table_column": "Price",
                        "csv_column": "price"
                    },
                    {  # Processed
                        "table_column": "HasAvailability",
                        "csv_column": "has_availability"
                    },
                    {
                        "table_column": "NumberOfReviews",
                        "csv_column": "number_of_reviews"
                    },
                    {
                        "table_column": "FirstReview",
                        "csv_column": "first_review"
                    },
                    {
                        "table_column": "LastReview",
                        "csv_column": "last_review"
                    },
                    {
                        "table_column": "License",
                        "csv_column": "license"
                    },
                    {  # Processed
                        "table_column": "InstantBookable",
                        "csv_column": "instant_bookable"
                    },
                    {
                        "table_column": "Latitude",
                        "csv_column": "latitude"
                    },
                    {
                        "table_column": "Longitude",
                        "csv_column": "longitude"
                    },
                    {
                        "table_column": "RoomType",
                        "csv_column": "room_type"
                    },
                    {
                        "table_column": "PropertyType",
                        "csv_column": "property_type"
                    },
                ]
            },
            {
                "name": "ListingRating",
                "mappings": [
                    {
                        "table_column": "ListingID",
                        "csv_column": "id"
                    },
                    {
                        "table_column": "HostID",
                        "csv_column": "host_id"
                    },
                    {
                        "table_column": "Rating",
                        "csv_column": "review_scores_rating"
                    },
                    {
                        "table_column": "Accuracy",
                        "csv_column": "review_scores_accuracy"
                    },
                    {
                        "table_column": "Cleanliness",
                        "csv_column": "review_scores_cleanliness"
                    },
                    {
                        "table_column": "Checkin",
                        "csv_column": "review_scores_checkin"
                    },
                    {
                        "table_column": "Communication",
                        "csv_column": "review_scores_communication"
                    },
                    {
                        "table_column": "Location",
                        "csv_column": "review_scores_location"
                    },
                    {
                        "table_column": "Value",
                        "csv_column": "review_scores_value"
                    }
                ]
            },
            {
                "name": "HostRating",
                "mappings": [
                    {
                        "table_column": "HostID",
                        "csv_column": "host_id"
                    },
                    {
                        "table_column": "Rating",
                        "csv_column": "{{GENERATE_AVERAGE_RATING}}"
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
    },
    {
        "resource_path": "resources/calendar_no_comma.csv",
        "tables": [
            {
                "name": "Calendar",
                "mappings": [
                    {
                        "table_column": "ListingId",
                        "csv_column": "listing_id"
                    },
                    {
                        "table_column": "Date",
                        "csv_column": "date"
                    },
                    {
                        "table_column": "Available",
                        "csv_column": "available"
                    },
                    {
                        "table_column": "Price",
                        "csv_column": "price"
                    },
                    {
                        "table_column": "AdjustedPrice",
                        "csv_column": "adjusted_price"
                    },
                    {
                        "table_column": "MinimumNights",
                        "csv_column": "minimum_nights"
                    },
                    {
                        "table_column": "MaximumNights",
                        "csv_column": "maximum_nights"
                    }
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
    "Neighborhood": {
        "Neighborhood": set()
    }
}

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "Gr8BnBApplication"
}
