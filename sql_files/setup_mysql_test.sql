-- prepares a MySQL server for the project:
-- A database hbnb_test_db
-- A new user hbnb_test(in localhost)
-- The password of hbnb_test should be set to hbnb_test_pwd
-- hbnb_test should have all PRIVILEGES on the DATABASE hbnb_test_db (and only this DATABASE)
-- hbnb_test should have SELECT PRIVILEGES on the DATABASE performance_schema(and only this DATABASE)
-- if the DATABASE hbnb_test_db or the user hbnb_test already exists, your script shouldn't fail

CREATE DATABASE IF NOT EXISTS `hbnb_test_db`;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
