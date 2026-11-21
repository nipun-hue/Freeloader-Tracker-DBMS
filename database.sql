CREATE DATABASE Project;
USE Project;

CREATE TABLE Professor (
    prof_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Student (
    student_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Project (
    project_id VARCHAR(10) PRIMARY KEY,
    prof_id VARCHAR(10) NOT NULL,
    title VARCHAR(200) NOT NULL,
    deadline DATE NOT NULL,
    FOREIGN KEY (prof_id) REFERENCES Professor(prof_id) ON DELETE CASCADE
);

CREATE TABLE TeamMembership (
    student_id VARCHAR(10),
    project_id VARCHAR(10),
    PRIMARY KEY (student_id, project_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

CREATE TABLE Task (
    task_id VARCHAR(10),
    project_id VARCHAR(10),
    title VARCHAR(200) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    deadline DATE NOT NULL,
    PRIMARY KEY (task_id, project_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

CREATE TABLE TaskAssignment (
    student_id VARCHAR(10),
    task_id VARCHAR(10),
    project_id VARCHAR(10),
    PRIMARY KEY (student_id, task_id, project_id),
    
    FOREIGN KEY (student_id, project_id) REFERENCES TeamMembership(student_id, project_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id, project_id) REFERENCES Task(task_id, project_id) ON DELETE CASCADE
);

CREATE TABLE PeerReview (
    review_id VARCHAR(10) PRIMARY KEY,
    task_id VARCHAR(10) NOT NULL,
    project_id VARCHAR(10) NOT NULL,
    reviewer_id VARCHAR(10) NOT NULL,
    reviewee_id VARCHAR(10) NOT NULL,
    contribution_weight INT,
    feedback TEXT,
    
    CHECK (contribution_weight BETWEEN 1 AND 5),
    
    CHECK (reviewer_id != reviewee_id),
    
    FOREIGN KEY (reviewer_id, project_id) REFERENCES TeamMembership(student_id, project_id) ON DELETE CASCADE,
    
    FOREIGN KEY (reviewee_id, project_id) REFERENCES TeamMembership(student_id, project_id) ON DELETE CASCADE,
    
    FOREIGN KEY (task_id, project_id) REFERENCES Task(task_id, project_id) ON DELETE CASCADE
);

CREATE TABLE Alert (
    alert_id VARCHAR(10) PRIMARY KEY,
    task_id VARCHAR(10) NOT NULL,
    project_id VARCHAR(10) NOT NULL,
    alert_type VARCHAR(200) NOT NULL,
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id, project_id) REFERENCES Task(task_id, project_id) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER trg_task_overdue_alert
AFTER UPDATE ON Task
FOR EACH ROW
BEGIN
    DECLARE responsible_student VARCHAR(100);

	SELECT s.name INTO responsible_student
    FROM TaskAssignment ta
    JOIN Student s ON ta.student_id = s.student_id
    WHERE ta.task_id = NEW.task_id AND ta.project_id = NEW.project_id
    LIMIT 1;

    IF responsible_student IS NULL THEN
        SET responsible_student = 'Unassigned Student';
    END IF;

    IF NEW.status = 'Overdue' AND OLD.status != 'Overdue' THEN
        INSERT INTO Alert (alert_id, task_id, project_id, alert_type)
        VALUES (
            CONCAT('A-', NEW.task_id), 
            NEW.task_id, 
            NEW.project_id, 
            CONCAT('Missed Deadline Alert: Task Overdue by ', responsible_student)
        );
    END IF;
END; //

DELIMITER ;


CREATE VIEW StudentReliability AS
SELECT 
    s.student_id,
    s.name,
    COALESCE(AVG(pr.contribution_weight), 0) AS avg_reliability_score
FROM Student s
LEFT JOIN PeerReview pr ON s.student_id = pr.reviewee_id
GROUP BY s.student_id, s.name;

ALTER TABLE Professor ADD COLUMN password VARCHAR(100) NOT NULL;

ALTER TABLE Student ADD COLUMN password VARCHAR(100) NOT NULL;

CREATE TABLE ProjectSupervision (
    prof_id VARCHAR(10),
    project_id VARCHAR(10),
    PRIMARY KEY (prof_id, project_id),
    FOREIGN KEY (prof_id) REFERENCES Professor(prof_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

ALTER TABLE Project DROP FOREIGN KEY project_ibfk_1;
ALTER TABLE Project DROP COLUMN prof_id;
CREATE OR REPLACE VIEW ProjectReliabilityScore AS
SELECT 
    tm.project_id,
    tm.student_id,
    AVG(pr.contribution_weight) AS project_score
FROM TeamMembership tm
LEFT JOIN PeerReview pr 
    ON tm.student_id = pr.reviewee_id AND tm.project_id = pr.project_id
GROUP BY tm.project_id, tm.student_id;