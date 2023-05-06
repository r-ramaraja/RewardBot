CREATE TABLE employee(    
    full_name VARCHAR(50),
    github_id VARCHAR(20),
    slack_id VARCHAR(20),
    points INT,
);

CREATE TABLE audit(
    awarder VARCHAR(50),
    awardee VARCHAR(50),
    award VARCHAR(50),
    award_date DATE    
);