
# Create schema and use it
CREATE SCHEMA IF NOT EXISTS Gr8BnBApplication;
USE Gr8BnBApplication;

# Drop tables, respecting referential integrity (child first, then parent)
DROP TABLE IF EXISTS PropertyType;
DROP TABLE IF EXISTS RoomType;
DROP TABLE IF EXISTS Calendar;
DROP TABLE IF EXISTS Neighborhood;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS ListingBookmark;
DROP TABLE IF EXISTS Connection;
DROP TABLE IF EXISTS Guest;
DROP TABLE IF EXISTS Host;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Listing;


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

ALTER TABLE User CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER TABLE Host CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;