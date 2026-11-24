CREATE DATABASE IF NOT EXISTS academy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE academy;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(100) NOT NULL,
  user_password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY user_name_UNIQUE (user_name)
);
