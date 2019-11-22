-- drop table if exists entries;
CREATE TABLE RegisteredUser
(email VARCHAR(256) NOT NULL PRIMARY KEY UNIQUE,
name VARCHAR(256) NOT NULL,
 password VARCHAR(256) NOT NULL
);

CREATE TABLE Sleep
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 PRIMARY KEY (email, date)
 );

CREATE TABLE Exercise
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 intensity INTEGER CHECK(intensity >=1 AND intensity<=5),
 PRIMARY KEY (email, date)
 );

CREATE TABLE Work
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 difficulty INTEGER CHECK(difficulty >=1 AND difficulty<=5),
 PRIMARY KEY (email, date)
 );

CREATE TABLE Meals
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality <=5),
 PRIMARY KEY (email, date)
 );

CREATE TABLE Social
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality <=5),
  PRIMARY KEY (email, date)
 );

CREATE TABLE Downtime
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 PRIMARY KEY (email, date));

CREATE TABLE Environment
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
  date DATE NOT NULL,
 location VARCHAR(32) NOT NULL, -- specify city / state on front end
 avg_temp INTEGER NOT NULL CHECK(avg_temp < 140 AND avg_temp > -40),
 type text NOT NULL CHECK (type IN ('indoor', 'outdoor')),
 weather text NOT NULL CHECK (weather IN ('sunny', 'partly cloudy',
                'cloudy', 'rainy', 'snowy', 'inclement weather', 'overcast', 'foggy', 'smog')),
PRIMARY KEY (email, date)
);


CREATE TABLE Mood
(email VARCHAR(256) NOT NULL REFERENCES RegisteredUser(email),
date DATE NOT NULL,
stress INTEGER CHECK(stress >=1 AND stress <=5),
energy INTEGER CHECK(energy >=1 AND energy <=5),
happiness INTEGER NOT NULL CHECK(happiness >=1 AND happiness <=5),
PRIMARY KEY (email, date)
);
