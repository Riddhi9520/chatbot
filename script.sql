CREATE DATABASE chatbot;
USE chatbot; -- always run this querry

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM chat_history; -- used to display chat history

-- used to delete chat_history
SET SQL_SAFE_UPDATES = 0;
DELETE FROM chat_history;
SET SQL_SAFE_UPDATES = 1;

-- used to set the id back to 1 
SET FOREIGN_KEY_CHECKS = 0;
ALTER TABLE chat_history AUTO_INCREMENT = 1;
SET FOREIGN_KEY_CHECKS = 1;


