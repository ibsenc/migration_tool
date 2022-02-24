
# Create schema and use it
CREATE SCHEMA IF NOT EXISTS Gr8BnBApplication;
USE Gr8BnBApplication;

# Drop tables, respecting referential integrity (child first, then parent)
DROP TABLE IF EXISTS Calendar;
DROP TABLE IF EXISTS ListingAmenity;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS ListingRating;
DROP TABLE IF EXISTS HostRating;
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

# Create Table Guest
CREATE TABLE Guest (
    ID INT UNSIGNED,
    CONSTRAINT pk_Guest_ID PRIMARY KEY (ID),
    CONSTRAINT fk_Guest_ID FOREIGN KEY (ID)
        REFERENCES User (ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# Create Table Review
# TODO: Integrate foreign key reference with Listing table
CREATE TABLE Review (
    ID BIGINT UNSIGNED,
    Date DATE,
    ReviewerID INT UNSIGNED,
    Comments TEXT,
    -- ListingID INT UNSIGNED,
    CONSTRAINT pk_Review_ID PRIMARY KEY (ID),
    CONSTRAINT fk_Review_ReviewerID FOREIGN KEY (ReviewerID)
        REFERENCES Guest (ID)
        ON UPDATE CASCADE ON DELETE SET NULL/*,
    CONSTRAINT fk_Review_ListingID FOREIGN KEY (ListingID)
        REFERENCES Listing (ID)
        ON UPDATE CASCADE ON DELETE CASCADE */
);

CREATE TABLE Calendar(
	ID INT AUTO_INCREMENT,
	ListingId INT,
	Date DATE,
	Available BOOLEAN,
	Price VARCHAR(255),
	AdjustedPrice VARCHAR(255),
	MinimumNights INT,
	MaximumNights INT,
	CONSTRAINT pk_Calendar_ID PRIMARY KEY(ID)
	-- CONSTRAINT fk_Calendar_ListingId FOREIGN KEY(ListingId)
-- 		REFERENCES Listing(ListingId)
-- 		ON UPDATE CASCADE ON DELETE CASCADE
);


ALTER TABLE User CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Host CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Guest CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Review CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
