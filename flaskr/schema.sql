-- drop table if exists entries;
CREATE TABLE RegisteredUser
(id INTEGER NOT NULL PRIMARY KEY UNIQUE AUTOINCREMENT,
 name VARCHAR(256) NOT NULL,
 email VARCHAR(256) NOT NULL UNIQUE,
 password VARCHAR(256) NOT NULL
);

CREATE TABLE Sleep
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 PRIMARY KEY (user_id, date)
 );

CREATE TABLE Exercise
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 intensity INTEGER CHECK(intensity >=1 AND intensity<=5),
 PRIMARY KEY (user_id, date)
 );

CREATE TABLE Work
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 difficulty INTEGER CHECK(difficulty >=1 AND difficulty<=5),
 PRIMARY KEY (user_id, date)
 );

CREATE TABLE Meals
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
 date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality <=5),
 PRIMARY KEY (user_id, date)
 );

CREATE TABLE Social
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality <=5),
  PRIMARY KEY (user_id, date)
 );

CREATE TABLE Downtime
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
date DATE NOT NULL,
 hours DECIMAL(4, 2) NOT NULL CHECK(hours <= 24.00),
 quality INTEGER CHECK(quality >=1 AND quality<=5),
 PRIMARY KEY (user_id, date));

CREATE TABLE Environment
(user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
  date DATE NOT NULL,
 location VARCHAR(32) NOT NULL, -- specify city / state on front end
 avg_temp INTEGER NOT NULL CHECK(avg_temp < 140 AND avg_temp > -40),
 type text NOT NULL CHECK (type IN ('indoor', 'outdoor')),
 weather text NOT NULL CHECK (weather IN ('sunny', 'partly cloudy',
                'cloudy', 'rainy', 'snowy', 'inclement weather', 'overcast', 'foggy', 'smog')),
PRIMARY KEY (user_id, date)
);

CREATE INDEX IDX_ID
ON RegisteredUser(id);

CREATE TABLE Mood
(user_id TEXT NOT NULL,
date TEXT NOT NULL,
happiness INTEGER NOT NULL,
PRIMARY KEY (user_id, date)
);
-- CREATE TABLE Mood
-- (user_id INTEGER NOT NULL REFERENCES RegisteredUser(id),
-- date DATE NOT NULL,
-- stress INTEGER NOT NULL CHECK(stress >=1 AND stress <=5),
-- energy INTEGER NOT NULL CHECK(energy >=1 AND energy <=5),
-- happiness INTEGER NOT NULL CHECK(happiness >=1 AND happiness <=5),
-- PRIMARY KEY (user_id, date)
-- );
