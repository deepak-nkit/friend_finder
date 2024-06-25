CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE,
        Email VARCHAR(255) NOT NULL UNIQUE, 
        Password TEXT,
        pincode INTEGER NOT NULL,
        Name Text,
        Number TEXT  UNIQUE,
        Address TEXT,
        JoinedOn DATE
        );

CREATE TABLE IF NOT EXISTS topic( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER ,  
                TopicName VARCHAR(100) NOT NULL,
                FOREIGN KEY(User_id) REFERENCES user(id)
                
             );       


CREATE TABLE IF NOT EXISTS session(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        User_id INTEGER,
        Token TEXT NOT NULL UNIQUE,
        FOREIGN KEY(User_id) REFERENCES user(id)
        );
                       


INSERT OR IGNORE INTO user (Username , Email , Password , pincode , JoinedOn) VALUES ('ram', 'ram@gmail.com' , '$2b$12$mTuNpT1JuinqMJghHDKIye00w.YXcfmMNpeSHFRyNJGifU4J0ZgXG' ,32207,'2024-06-22 18:11:30');

INSERT OR IGNORE INTO user (Username , Email , Password , pincode , JoinedOn) VALUES ('dev', 'dev@g.com', '$2b$12$8wd3s57ZaZzFb.cMjmezs.4/lYCcCHcdwgFmifEtjEv2rMpQjmLfC' , 32207 , '2024-06-22 18:27:23');

INSERT OR IGNORE INTO user (Username , Email , Password , pincode , JoinedOn) VALUES ('kiki' , 'kiki@g.com', '$2b$12$jZ3S2G6TU6s.zj8xjWGnbOAmcbXQbYQWYUAJQrHug922/FPuf2ndC', 32207 , '2024-06-23 15:04:04');

INSERT OR IGNORE INTO user (Username , Email , Password , pincode , JoinedOn) VALUES ('totoro' , 'totoro@g.com', '$2b$12$6STr0ekuxdzorcqulAxx8.moPE52tTkI4EFVvPjXd0oRxx9vgHeIS',32207 , '2024-06-23 15:17:43');

INSERT OR IGNORE INTO user (Username , Email , Password , pincode , JoinedOn) VALUES ('panda' , 'panda@gmail.com' , '$2b$12$615xZWyCPeh6t8a3OINbV.Z84pExrrja7T0N/tvLQjqfLmbbdFG2S' , 70707 , ' 2024-06-25 20:40:07');


INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (1, 'coding');
INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (1 , 'game');

INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (2 , 'coding');
INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (2, 'gaming');

INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (3, 'coding');

INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (4,'fighting');
INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (4,'comedy');

INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (5 , 'toy');
INSERT OR IGNORE INTO topic (User_id , TopicName) VALUES (5 , 'joy');

