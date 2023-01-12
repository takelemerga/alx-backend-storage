-- Creates a stored procedure AddBonus that adds a new
-- that adds a new correction for a student
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    INSERT INTO projects(name)
    SELECT project_name FROM DUAL
    WHERE NOT EXISTS(SELECT * FROM projects WHERE name = project_name LIMIT 1);

    INSERT INTO corrections(user_id, project_id, score) 
    VALUES (
    user_id,
    (SELECT id FROM projects WHERE name = project_name),
    score); 
END $$
DELIMITER;
