
# Create schema and use it
CREATE SCHEMA IF NOT EXISTS Gr8BnBApplication;
USE Gr8BnBApplication;

# Drop tables, respecting referential integrity (child first, then parent)
DROP TABLE IF EXISTS Calendar;
DROP TABLE IF EXISTS ListingAmenity;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS HostRating;
DROP TABLE IF EXISTS ListingRating;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Guest;
DROP TABLE IF EXISTS Listing;
DROP TABLE IF EXISTS Host;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Neighborhood;

# Create Table Neighborhood
CREATE TABLE Neighborhood (
    Neighborhood VARCHAR(255),
    NeighborhoodGroup VARCHAR(255),
    CONSTRAINT pk_Neighborhood_Neighborhood PRIMARY KEY (Neighborhood)
);
ALTER TABLE Neighborhood CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

# Create Table User
CREATE TABLE User (
    ID INT UNSIGNED,
    Name VARCHAR(255) NOT NULL,
    UserName VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    CONSTRAINT pk_User_ID PRIMARY KEY (ID)
);

# Create Table Host
CREATE TABLE Host (
	ID INT UNSIGNED,
    HostUrl TEXT,
    HostSince DATE NOT NULL,
    HostLocation VARCHAR(255),
    HostAbout TEXT,
    HostListingsCount INT UNSIGNED DEFAULT 0,
    HostTotalListingsCount INT UNSIGNED DEFAULT 0,
    CONSTRAINT pk_Host_ID PRIMARY KEY (ID),
    CONSTRAINT fk_Host_ID
		FOREIGN KEY (ID)
		REFERENCES User(ID)
		ON UPDATE CASCADE ON DELETE CASCADE
);

# Create Table Listing
CREATE TABLE Listing (
    ID INT UNSIGNED,
    ListingUrl TEXT,
    Name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
    Description TEXT,
    NeighborhoodOverview TEXT,
    PictureUrl VARCHAR(255),
    HostID INT UNSIGNED,
    Neighborhood VARCHAR(255),
    Accommodates INT,
    BathroomsText VARCHAR(255),
    Bedrooms INT DEFAULT 0,
    Price DECIMAL(13, 2),
    HasAvailability BOOLEAN,
    NumberOfReviews INT,
    FirstReview DATE NULL,
    LastReview DATE NULL,
    License VARCHAR(255),
    InstantBookable BOOLEAN,
    Latitude DECIMAL(10, 5),
    Longitude DECIMAL(10, 5),
    RoomType ENUM('Entire home/apt', 'Private room', 'Shared room', 'Hotel room'),
    PropertyType Text,

    CONSTRAINT pk_Listing_ID PRIMARY KEY (ID),
    CONSTRAINT fk_Listing_HostID
        FOREIGN KEY (HostID)
        REFERENCES Host(ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
ALTER TABLE Listing CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Listing  ADD  CONSTRAINT fk_Listing_Neighborhood FOREIGN KEY (Neighborhood) REFERENCES Neighborhood(Neighborhood) ON UPDATE CASCADE ON DELETE SET NULL;


# Create Table Guest
CREATE TABLE Guest (
    ID INT UNSIGNED,
    CONSTRAINT pk_Guest_ID PRIMARY KEY (ID),
    CONSTRAINT fk_Guest_ID FOREIGN KEY (ID)
        REFERENCES User (ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# Create Table Review
CREATE TABLE Review (
    ID BIGINT UNSIGNED,
    Date DATE,
    ReviewerID INT UNSIGNED,
    Comments TEXT,
    ListingID INT UNSIGNED,
    CONSTRAINT pk_Review_ID PRIMARY KEY (ID),
    CONSTRAINT fk_Review_ReviewerID FOREIGN KEY (ReviewerID)
        REFERENCES Guest (ID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_Review_ListingID FOREIGN KEY (ListingID)
        REFERENCES Listing (ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# Create ListingRating
CREATE TABLE ListingRating (
    ID INT AUTO_INCREMENT,
    ListingID INT UNSIGNED,
    HostID INT UNSIGNED,
    ScoreType ENUM('Rating', 'Accuracy', 'Cleanliness', 'Checkin', 'Communication', 'Location', 'Value') NOT NULL,
    Score DECIMAL(2,1) NULL,
    CONSTRAINT pk_ListingRating_ID PRIMARY KEY (ID),
    CONSTRAINT uq_ListingRating_Rating UNIQUE (ListingID, ScoreType),
    CONSTRAINT fk_ListingRating_ListingID FOREIGN KEY (ListingID)
        REFERENCES Listing (ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT fk_ListingRating_HostID FOREIGN KEY (HostID)
        REFERENCES Host (ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# Create HostRating
CREATE TABLE HostRating (
	ID INT UNSIGNED AUTO_INCREMENT,
    HostID INT UNSIGNED,
    Rating DECIMAL(3,2) NULL DEFAULT NULL,
    CONSTRAINT pk_HostRating_ID PRIMARY KEY (ID),
    CONSTRAINT fk_HostRating_HostID FOREIGN KEY (HostID)
		REFERENCES Host (ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# Create Amenity
CREATE TABLE Amenity(
	ID INT AUTO_INCREMENT,
	Title TEXT,
	CONSTRAINT pk_Amenity_ID PRIMARY KEY(ID)
);

# Create ListingAmenity
CREATE TABLE ListingAmenity (
    ID INT AUTO_INCREMENT,
    ListingID INT UNSIGNED,
    AmenityID INT,
    CONSTRAINT pk_ListingAmenity_ID PRIMARY KEY (ID),
    CONSTRAINT fk_ListingAmenity_ListingID FOREIGN KEY (ListingID)
        REFERENCES Listing (ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT fk_ListingAmenity_AmenityID FOREIGN KEY (AmenityID)
        REFERENCES Amenity (ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# Create Calendar
CREATE TABLE Calendar(
	ID INT AUTO_INCREMENT,
	ListingID INT UNSIGNED,
	Date DATE,
	Available BOOLEAN,
	Price DECIMAL(13, 2),
	AdjustedPrice DECIMAL(13, 2),
	MinimumNights INT DEFAULT 0,
	MaximumNights INT DEFAULT 0,
	CONSTRAINT pk_Calendar_ID PRIMARY KEY(ID),
	CONSTRAINT fk_Calendar_ListingId FOREIGN KEY(ListingID)
		REFERENCES Listing(ID)
		ON UPDATE CASCADE ON DELETE CASCADE
);


ALTER TABLE User CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Host CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Guest CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Review CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER DATABASE Gr8BnBApplication CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci; 
