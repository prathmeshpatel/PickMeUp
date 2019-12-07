-- drop table if exists entries;
-- Added start and end time: military time (10pm would be written 22:00:00 etc)
-- removed quality / intensity

CREATE TABLE RegisteredUser
(email VARCHAR(256) NOT NULL PRIMARY KEY UNIQUE,
name VARCHAR(256) NOT NULL,
password VARCHAR(256) NOT NULL
);

CREATE TABLE Sleep
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 start_time TIME (0) NOT NULL,
 end_time TIME (0) NOT NULL,
 quality DECIMAL(4,2) NOT NULL
 PRIMARY KEY (email, date)
 );

CREATE TABLE Exercise
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 start_time TIME (0) NOT NULL,
 end_time TIME (0) NOT NULL,
 quality DECIMAL(4,2) NOT NULL
 PRIMARY KEY (email, date)
 );

CREATE TABLE Work
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 start_time TIME (0) NOT NULL,
 end_time TIME (0) NOT NULL,
 quality DECIMAL(4,2) NOT NULL
 PRIMARY KEY (email, date)
 );

CREATE TABLE Meals
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 start_time TIME (0) NOT NULL,
 end_time TIME (0) NOT NULL,
 quality DECIMAL(4,2) NOT NULL
 PRIMARY KEY (email, date)
 );

CREATE TABLE Social
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
date DATE NOT NULL,
start_time TIME (0) NOT NULL,
end_time TIME (0) NOT NULL,
quality DECIMAL(4,2) NOT NULL
PRIMARY KEY (email, date)
 );

CREATE TABLE Downtime
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 start_time TIME (0) NOT NULL,
 end_time TIME (0) NOT NULL,
 quality DECIMAL(4,2) NOT NULL
 PRIMARY KEY (email, date));

CREATE TABLE Mood
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
date DATE NOT NULL,
happiness INTEGER NOT NULL CHECK(happiness >=1 AND happiness <=5),
PRIMARY KEY (email, date)
);
