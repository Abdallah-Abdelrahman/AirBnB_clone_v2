-- Prepares a MySQL server FOR the project (dev)
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- CREATE USER
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Assign privileges
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
