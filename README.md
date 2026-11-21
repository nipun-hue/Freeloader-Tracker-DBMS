<div align="center">

# 🎯 Freeloader Tracker & Task Auditor

### A DBMS-powered academic group project accountability system

**Track tasks · Review contributions · Surface reliability scores · Audit overdue work**

![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/UI-HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

**[Features](#-features) · [Screenshots](#-project-screenshots) · [Database](#-database-design) · [Quick Start](#-quick-start) · [Demo](#-demonstration)**

</div>

---

## 📌 Overview

In academic group projects, it can be difficult to distinguish individual effort from the team's overall result. **Freeloader Tracker & Task Auditor** provides a local web application for managing project teams, assigning tasks, recording peer feedback, and calculating contribution-based reliability scores.

The project demonstrates practical **relational database design**, including composite keys, foreign keys, joins, views, and a MySQL trigger.

## ✨ Features

| 👤 Admin | 👨‍🏫 Professor | 🎓 Student |
|---|---|---|
| Register students and professors | Create, update, and delete projects | View enrolled projects |
| View and update user records | Assign students to project teams | Create and manage tasks |
| Delete users | View team membership and task progress | Assign tasks to team members |
| | View project-level reliability scores | Update task status |
| | Review overdue-task alerts | Submit, edit, and view peer reviews |

### How the contribution audit works

1. **Create a project** and enroll its student team.
2. **Create and assign tasks** to team members.
3. **Submit peer reviews** with a contribution weight from **1 to 5**.
4. **Calculate reliability scores** using the average weight received.
5. **Flag overdue tasks**: when a task's status changes to `Overdue`, a MySQL trigger creates an alert.

> **Note:** The overdue alert is triggered by a **status change**, not by a background scheduler checking calendar deadlines.

## 🖼️ Project Screenshots

<div align="center">

<table>
<tr>
<td align="center"><strong>Screenshot 1</strong><br/><img src="https://github.com/user-attachments/assets/ea8e16ea-284c-4b1c-bcd4-b3cf5c208e27" alt="Project screenshot 1" width="560" /></td>
</tr>
<tr>
<td align="center"><strong>Screenshot 2</strong><br/><img src="https://github.com/user-attachments/assets/c8574ec6-fb8c-4b69-a056-4e87cb7591e6" alt="Project screenshot 2" width="560" /></td>
</tr>
<tr>
<td align="center"><strong>Screenshot 3</strong><br/><img src="https://github.com/user-attachments/assets/23e570cd-7b1c-4750-a698-9a486e1ce064" alt="Project screenshot 3" width="560" /></td>
</tr>
<tr>
<td align="center"><strong>Screenshot 4</strong><br/><img src="https://github.com/user-attachments/assets/a30de7fe-93a1-4c50-8312-c7195423983d" alt="Project screenshot 4" width="560" /></td>
</tr>
<tr>
<td align="center"><strong>Screenshot 5</strong><br/><img src="https://github.com/user-attachments/assets/f517097e-5832-4a9d-bd3c-74e35d94005a" alt="Project screenshot 5" width="560" /></td>
</tr>
</table>

</div>

## 🧰 Technology Stack

| Layer | Technology | Purpose |
|:--|:--|:--|
| Frontend | HTML, CSS, JavaScript | Interactive browser interface |
| Backend | Python, Flask | REST API and application logic |
| Cross-origin requests | Flask-CORS | Frontend-to-backend requests |
| Database | MySQL | Relational data storage |
| Connector | mysql-connector-python | Python–MySQL integration |
| API data format | JSON | Client/server communication |

## 🗄️ Database Design

**Database name:** `Project`

| Table | Responsibility |
|:--|:--|
| `Professor` | Professor accounts |
| `Student` | Student accounts |
| `Project` | Project details and deadlines |
| `ProjectSupervision` | Professor–project relationships |
| `TeamMembership` | Student–project relationships |
| `Task` | Project tasks and statuses |
| `TaskAssignment` | Task assignments to enrolled students |
| `PeerReview` | Contribution weights and feedback |
| `Alert` | Overdue task alerts |

**Database views:** `StudentReliability` and `ProjectReliabilityScore`.

**Trigger:** `trg_task_overdue_alert` inserts a record into `Alert` when a task is updated to `Overdue` from another status.

**DBMS concepts:** primary keys, composite keys, foreign keys, referential integrity, SQL joins, aggregation, views, triggers, and CRUD operations.

### Reliability scoring

```text
Reliability score = Sum of received contribution weights / Number of received reviews
```

Each peer-review contribution weight is between **1 and 5**. Scores reflect submitted peer ratings; students without reviews do not have a meaningful rated average yet.

## 📂 Repository Structure

```text
Freeloader-Tracker-DBMS/
├── app.py            # Flask backend and API routes
├── Website.html      # Frontend (HTML, CSS, JavaScript)
├── database.sql      # MySQL schema, views, and trigger
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3
- MySQL Server
- MySQL Workbench (recommended)
- A modern web browser

### 1. Download the repository

```bash
git clone https://github.com/nipun-hue/Freeloader-Tracker-DBMS.git
cd Freeloader-Tracker-DBMS
```

Alternatively, select **Code → Download ZIP** on GitHub and extract it.

### 2. Initialize the database

Open `database.sql` in MySQL Workbench and execute the script against your local MySQL server.

> The script starts with `CREATE DATABASE Project;`. If you already have a database named `Project`, do not rerun it blindly. Back up existing data and review the script first.

### 3. Configure your local MySQL connection

In `app.py`, locate the connection configuration:

```python
mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Project'
)
```

Set `password` to your **local** MySQL password if your server requires one. **Do not commit real credentials to a public repository.**

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start Flask

```bash
python app.py
```

The backend runs locally at `http://127.0.0.1:5000`. Keep the terminal open.

### 6. Launch the website

Open `Website.html` in your browser. The frontend sends requests to `http://127.0.0.1:5000/api`.

## 🧪 Demo Walkthrough

1. Sign in as the demo administrator and create professor/student accounts.
2. Sign in as a professor, create a project, and enroll registered students.
3. Sign in as a student, create tasks, and assign them to enrolled teammates.
4. Submit peer reviews for students assigned to those tasks.
5. Return to the professor dashboard to view project reliability scores.
6. Set a task status to `Overdue` and inspect the generated alert.

<details>
<summary><strong>Local demo administrator credentials</strong></summary>

- **Role:** Admin
- **User ID:** Any non-empty value (for example, `admin`)
- **Password:** `admin123`

These credentials are hardcoded for the academic demonstration. The project is **not production-ready**: authentication and access controls would need to be redesigned before public deployment.

</details>

## 🎥 Demonstration

The project demonstration video can be linked here when available.

<!-- Replace the line above with a link to your uploaded video. -->

## 🔒 Security & Scope

This is a **local academic DBMS demonstration**, not a hosted production service. The backend uses a demo administrator password and Flask debug mode. Run it locally, avoid exposing the Flask server to the public internet, and never publish personal database credentials.

---

<div align="center">

**Built as an academic Database Management Systems project**

*Python · Flask · MySQL · HTML · CSS · JavaScript*

</div>
