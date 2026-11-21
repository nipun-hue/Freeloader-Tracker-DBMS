# Freeloader-Tracker-DBMS
DBMS project for tracking group tasks, student contributions and peer reviews

# Freeloader Tracker & Task Auditor

### Database Management Systems (DBMS) Project

A web-based application designed to monitor student contributions, manage academic group projects, assign tasks, and identify freeloaders through peer reviews and reliability scores.

---

## 1. Project Overview

In academic group projects, it can be difficult to determine how much each student contributes. Some students complete most of the work, while others contribute very little.

**Freeloader Tracker & Task Auditor** addresses this problem by providing a centralized platform for managing projects, monitoring tasks, evaluating individual contributions, and identifying underperforming team members.

## 2. Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Database Connector | MySQL Connector for Python |
| API Communication | REST APIs, JSON |

## 3. Main Features

### Admin Portal
- Add and manage student accounts
- Add and manage professor accounts
- View registered users
- Update and delete user details

### Professor Portal
- Create, update, and delete projects
- Assign students to project teams
- View supervised projects
- Monitor team members and assigned tasks
- Check student reliability scores
- View overdue task alerts

### Student Portal
- View enrolled projects
- Create and manage project tasks
- Assign tasks to team members
- Update task status
- Submit peer reviews
- View received and submitted reviews
- Monitor individual contribution scores

## 4. Database Design

The project uses a relational MySQL database named `Project`.

**Main Tables:**
1. Professor
2. Student
3. Project
4. ProjectSupervision
5. TeamMembership
6. Task
7. TaskAssignment
8. PeerReview
9. Alert

**Database Concepts Implemented:**
- Primary Keys
- Foreign Keys
- Composite Keys
- Referential Integrity
- SQL Joins
- Aggregate Functions
- Database Views
- Triggers
- CRUD Operations

### Database Views

**StudentReliability:** Calculates the average peer-review contribution score received by each student.

**ProjectReliabilityScore:** Calculates student contribution scores for individual projects.

### Database Trigger

**trg_task_overdue_alert**

Automatically inserts an alert into the `Alert` table when a task's status changes to `Overdue`.

## 5. Project Structure

```text
Freeloader-Tracker-DBMS/
│
├── app.py
├── Website.html
├── database.sql
├── requirements.txt
└── README.md
```

## 6. Installation and Setup

### Prerequisites

Install the following software:

- Python 3
- MySQL Server
- MySQL Workbench (recommended)
- A modern web browser

### Step 1: Download the Project

Download the repository as a ZIP file from GitHub and extract it.

Alternatively, clone it:

```bash
git clone https://github.com/nipun-hue/Freeloader-Tracker-DBMS.git
```

### Step 2: Set Up the Database

1. Open MySQL Workbench.
2. Connect to your local MySQL Server.
3. Open `database.sql`.
4. Execute the SQL script to create the `Project` database, tables, views, and trigger.

**Note:** The script creates a new database. If a database named `Project` already exists, review the script before executing it again.

### Step 3: Configure the Backend

Open `app.py` and locate the database connection:

```python
mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Project'
)
```

Enter your own local MySQL password in the `password` field if required.

Never publish your personal database password.

### Step 4: Install Python Dependencies

Open Command Prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 5: Start the Backend

Run:

```bash
python app.py
```

The Flask backend starts at:

`http://127.0.0.1:5000`

Keep this terminal running while using the website.

### Step 6: Open the Frontend

Open `Website.html` in your web browser.

The frontend communicates with the Flask backend using REST API requests.

## 7. How to Use the Application

1. Log in as an administrator and create student and professor accounts.
2. Log in as a professor and create a project.
3. Assign registered students to the project team.
4. Log in as a student to create tasks and assign responsibilities.
5. Update task statuses as work progresses.
6. Submit peer reviews for team members assigned to tasks.
7. View reliability scores from the professor dashboard.
8. Change a task's status to `Overdue` to demonstrate the automated database alert.

### Demo Administrator Login

- **Role:** Admin
- **User ID:** Any non-empty value, such as `admin`
- **Password:** `admin123`

These are demonstration credentials defined in the original backend. This application is intended for local academic demonstration, not public production deployment.

## 8. Reliability Score Calculation

Student reliability is calculated using the average contribution weight received through peer reviews.

\[
\text{Reliability Score} = \frac{\text{Sum of Contribution Weights}}{\text{Number of Reviews}}
\]

Contribution weights range from **1 to 5**.

A lower score indicates lower peer-rated contribution, while a higher score indicates stronger peer-rated contribution.

## 9. Project Demonstration

A demonstration video can be linked here to showcase the Admin, Professor, and Student portals, task management, peer reviews, and database functionality.

## 10. Conclusion

The Freeloader Tracker & Task Auditor demonstrates how relational database concepts can be applied to a real-world academic problem.

By combining project management, task tracking, peer reviews, reliability calculations, and automated database alerts, the application helps improve transparency and accountability in student group projects.

---

**Project Type:** Academic DBMS Project

**Technologies:** Python Flask, MySQL, HTML, CSS, JavaScript
