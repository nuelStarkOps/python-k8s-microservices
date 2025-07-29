-- user for auth service
-- user table to contain users that will have access to our API

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123'; -- user to access the db via auth service

-- create DB
CREATE DATABASE auth; 

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost'; -- grant permissions for auth service to make changes to auth service DB

USE auth;

-- create table 
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- create initial user to have access to auth service api
INSERT INTO user (email, password) VALUES ('nuelthedeveloper@gmail.com', 'Admin123');