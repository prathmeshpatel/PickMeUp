SELECT AVG(Meals.hours) AS meal_hours, AVG(Mood.happiness) AS happiness
FROM Meals, Mood
WHERE Mood.happiness=5 GROUP BY Mood.user_id;

SELECT AVG(Social.hours) AS social_hours, AVG(Mood.happiness) AS happiness
FROM Social, Mood
WHERE Mood.happiness=5 GROUP BY Mood.user_id;

SELECT AVG(Downtime.hours) AS downtime_hours, AVG(Mood.happiness) AS happiness
FROM Downtime, Mood
WHERE Mood.happiness=5 GROUP BY Mood.user_id;

SELECT Sleep.hours, Mood.user_id, Mood.happiness
FROM Mood, Sleep
WHERE Sleep.user_id= 1112 and Mood.user_id = 1112;

SELECT AVG(Meals.quality) AS meal_quality, AVG(Mood.happiness) AS happiness
FROM Meals, Mood
WHERE Mood.happiness = 1 GROUP BY Mood.user_id;

UPDATE Mood
SET happiness= 5
WHERE user_id = 1113 and date = '2019-10-06';

SELECT RegisteredUser.name, Environment.avg_temp, Mood.happiness
FROM Environment, Mood, RegisteredUser
WHERE Environment.avg_temp > 65
AND Environment.user_id = Mood.user_id AND RegisteredUser.id = Mood.user_id;

SELECT RegisteredUser.name, MAX(Social.hours) AS max_social_hours, MIN(Social.hours) AS min_social_hours, AVG(Mood.happiness) AS happiness
FROM Social, Mood, RegisteredUser
WHERE Mood.happiness > 3 AND  Social.user_id=Mood.user_id AND RegisteredUser.id=Mood.user_id
GROUP BY RegisteredUser.name;

SELECT RegisteredUser.name, MIN(Sleep.hours) AS min_sleep_hours, AVG(Mood.happiness) AS happiness
FROM Sleep, Mood, RegisteredUser
WHERE Mood.happiness > 3 AND  Sleep.user_id=Mood.user_id AND RegisteredUser.id=Mood.user_id
GROUP BY RegisteredUser.name;