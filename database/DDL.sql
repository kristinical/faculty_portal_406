/*******************************************************
Author: Kristin Eberman
Project: Education Expeditions Faculty Portal
CS406 | Spring 2023 | Oregon State University
DATA DEFINITION QUERIES
********************************************************/

-- Disable foreign key checks and commits
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- CREATE PROGRAMS TABLE
CREATE OR REPLACE Table Programs (
    programID INT NOT NULL AUTO_INCREMENT UNIQUE,
    programName VARCHAR(255) NOT NULL,
    faculty VARCHAR(255) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    university VARCHAR(255) NOT NULL,
    startDate VARCHAR(50) NOT NULL,
    endDate VARCHAR(50) NOT NULL,
    PRIMARY KEY (programID)
);

-- CREATE USERS TABLE
-- programID FK links to Programs in a 1:1 relationship
CREATE OR REPLACE Table Users (
    userID INT NOT NULL AUTO_INCREMENT UNIQUE,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(50) NOT NULL,
    admin BOOLEAN NOT NULL,
    programID INT NULL,
    PRIMARY KEY (userID),
    CONSTRAINT fk_Program_User FOREIGN KEY (programID)
        REFERENCES Programs (programID)
        ON DELETE CASCADE
);

-- CREATE TASKS TABLE
-- programID FK links to Programs in a M:1 relationship
CREATE OR REPLACE Table Tasks (
    taskID INT NOT NULL AUTO_INCREMENT UNIQUE,
    taskName VARCHAR(255) NOT NULL,
    dueDate VARCHAR(50) NOT NULL,
    taskType ENUM ('Upload', 'Submit', 'Pay') NOT NULL,
    completed BOOLEAN DEFAULT 0 NOT NULL,
    programID INT NOT NULL,
    PRIMARY KEY (taskID),
    CONSTRAINT fk_Program_Tasks FOREIGN KEY (programID)
        REFERENCES Programs (programID)
        ON DELETE CASCADE
);

-- INSERT SAMPLE DATA INTO PROGRAMS
INSERT INTO Programs (programName, faculty, destination, university, startDate, endDate)
    VALUES ('Traditional vs. Modern Architecture', 'Dr. Jane Doe', 'Japan', 'Oregon State University', '2023-06-16', '2023-07-06'),
    ('Public Health', 'Dr. Marni Healer', 'Ghana', 'Explorer Institution', '2023-07-08', '2023-07-23'),
    ('Elementary Education', 'Dr. Terry Teacher', 'England', 'Adventure College', '2023-07-12', '2023-08-02'),
    ('Environmental Sustainability', 'Dr. Victoria Flores', 'Peru', 'University of Travel', '2023-08-06', '2023-08-26');

-- INSERT SAMPLE DATA INTO USERS
INSERT INTO Users (username, password, admin, programID)
    VALUES ('admin', 'adminpw', 1, NULL),
    ('japan_faculty', 'japan', 0, 1),
    ('ghana_faculty', 'ghana', 0, 2),
    ('england_faculty', 'england', 0, 3),
    ('peru_faculty', 'peru', 0, 4);

-- INSERT SAMPLE DATA INTO TASKS
INSERT INTO Tasks (taskName, dueDate, taskType, completed, programID)
    VALUES ('Submit Program Proposal', '2023-03-16', 'Upload', 1, 1),
    ('Submit Program Agreement', '2023-05-16', 'Upload', 1, 1),
    ('Pay Final Invoice', '2023-06-01', 'Pay', 0, 1),
    ('Submit Student Details', '2023-06-12', 'Submit', 0, 1),
    ('Submit Program Proposal', '2023-04-08', 'Upload', 1, 2),
    ('Submit Program Agreement', '2023-05-08', 'Upload', 1, 2),
    ('Pay Final Invoice', '2023-06-08', 'Pay', 0, 2),
    ('Submit Student Details', '2023-07-01', 'Submit', 0, 2),
    ('Submit Program Proposal', '2023-04-12', 'Upload', 1, 3),
    ('Submit Program Agreement', '2023-05-12', 'Upload', 1, 3),
    ('Pay Final Invoice', '2023-06-12', 'Pay', 0, 3),
    ('Submit Student Details', '2023-07-05', 'Submit', 0, 3),
    ('Submit Program Proposal', '2023-05-06', 'Upload', 1, 4),
    ('Submit Program Agreement', '2023-06-06', 'Upload', 0, 4),
    ('Pay Final Invoice', '2023-07-06', 'Pay', 0, 4),
    ('Submit Student Details', '2023-07-31', 'Submit', 0, 4);

-- Re-enable foreign key checks and commits
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
