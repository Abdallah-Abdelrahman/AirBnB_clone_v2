-- Prepares a MySQL server for the project (test)
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- CREATE USER
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Assign privileges
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';
