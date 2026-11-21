from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import date
import uuid

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def get_db_connection():
    try:
        return mysql.connector.connect(host='localhost', user='root', password='', database='Project')
    except Error as e:
        print(f"DB Error: {e}")
        return None

# ================= AUTHENTICATION =================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    role, user_id, password = data.get('role'), data.get('user_id'), data.get('password')
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    
    try:
        if role == 'admin' and password == 'admin123': return jsonify({"success": True, "role": "admin"})
        elif role == 'professor':
            cursor.execute("SELECT name FROM Professor WHERE prof_id = %s AND password = %s", (user_id, password))
            rec = cursor.fetchone()
            if rec: return jsonify({"success": True, "name": rec['name'], "prof_id": user_id, "role": "professor"})
        elif role == 'student':
            cursor.execute("SELECT name FROM Student WHERE student_id = %s AND password = %s", (user_id, password))
            rec = cursor.fetchone()
            if rec: return jsonify({"success": True, "name": rec['name'], "student_id": user_id, "role": "student"})
        return jsonify({"error": "Invalid credentials or role"}), 401
    finally:
        if conn.is_connected(): cursor.close(); conn.close()

# ================= ADMIN ENDPOINTS (CRUD) =================
@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT student_id, name, email FROM Student")
        students = cursor.fetchall()
        cursor.execute("SELECT prof_id, name FROM Professor")
        profs = cursor.fetchall()
        return jsonify({"success": True, "students": students, "professors": profs})
    finally: cursor.close(); conn.close()

@app.route('/api/admin/add_professor', methods=['POST'])
def add_professor():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Professor (prof_id, name, password) VALUES (%s, %s, %s)", (data['prof_id'], data['name'], data['password']))
        conn.commit()
        return jsonify({"success": True, "message": f"Professor {data['name']} added."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/admin/add_student', methods=['POST'])
def add_student():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Student (student_id, name, email, password) VALUES (%s, %s, %s, %s)", (data['student_id'], data['name'], data['email'], data['password']))
        conn.commit()
        return jsonify({"success": True, "message": f"Student {data['name']} added."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/admin/users/<role>/<user_id>', methods=['DELETE'])
def delete_user(role, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        table = 'Student' if role == 'Student' else 'Professor'
        id_column = 'student_id' if role == 'Student' else 'prof_id'
        cursor.execute(f"DELETE FROM {table} WHERE {id_column} = %s", (user_id,))
        conn.commit()
        return jsonify({"success": True, "message": f"{role} {user_id} deleted successfully."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/admin/users/<role>', methods=['PUT'])
def update_user(role):
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        if role == 'Student':
            cursor.execute("UPDATE Student SET name=%s, email=%s, password=%s WHERE student_id=%s", (data['name'], data['email'], data['password'], data['id']))
        else:
            cursor.execute("UPDATE Professor SET name=%s, password=%s WHERE prof_id=%s", (data['name'], data['password'], data['id']))
        conn.commit()
        return jsonify({"success": True, "message": f"{role} {data['id']} updated successfully."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

# ================= PROFESSOR & PROJECT ENDPOINTS =================
@app.route('/api/projects/create', methods=['POST'])
def create_project():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        if str(data['deadline']) < str(date.today()):
            return jsonify({"error": "Project deadline cannot be in the past."}), 400
            
        cursor.execute("INSERT INTO Project (project_id, title, deadline) VALUES (%s, %s, %s)", (data['project_id'], data['title'], data['deadline']))
        cursor.execute("INSERT INTO ProjectSupervision (prof_id, project_id) VALUES (%s, %s)", (data['prof_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Project created."})
    except Error as e: conn.rollback(); return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        if str(data['deadline']) < str(date.today()):
            return jsonify({"error": "Project deadline cannot be in the past."}), 400
            
        cursor.execute("UPDATE Project SET title=%s, deadline=%s WHERE project_id=%s", (data['title'], data['deadline'], project_id))
        conn.commit()
        return jsonify({"success": True, "message": "Project updated successfully."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Project WHERE project_id=%s", (project_id,))
        conn.commit()
        return jsonify({"success": True, "message": "Project deleted successfully."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/teams/assign', methods=['POST'])
def assign_team_member():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO TeamMembership (student_id, project_id) VALUES (%s, %s)", (data['student_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Assigned to project."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/teams/remove', methods=['DELETE'])
def remove_team_member():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TeamMembership WHERE student_id=%s AND project_id=%s", (data['student_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Student removed from project."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/professor/projects/<prof_id>', methods=['GET'])
def get_professor_dashboard(prof_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.project_id, p.title, p.deadline, COUNT(DISTINCT tm.student_id) AS member_count
            FROM Project p JOIN ProjectSupervision ps ON p.project_id = ps.project_id
            LEFT JOIN TeamMembership tm ON p.project_id = tm.project_id
            WHERE ps.prof_id = %s GROUP BY p.project_id
        """, (prof_id,))
        my_projects = cursor.fetchall()
        cursor.execute("SELECT project_id, title, deadline FROM Project")
        return jsonify({"success": True, "my_projects": my_projects, "all_projects": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/projects/<project_id>/team_scores', methods=['GET'])
def get_project_team_scores(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT tm.student_id, s.name, AVG(pr.contribution_weight) AS project_reliability_score
            FROM TeamMembership tm JOIN Student s ON tm.student_id = s.student_id
            LEFT JOIN PeerReview pr ON tm.student_id = pr.reviewee_id AND tm.project_id = pr.project_id
            WHERE tm.project_id = %s GROUP BY tm.student_id ORDER BY project_reliability_score DESC
        """, (project_id,))
        return jsonify({"success": True, "team_scores": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/professor/alerts/<prof_id>', methods=['GET'])
def get_alerts(prof_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.alert_id, a.task_id, p.project_id, a.alert_type, a.alert_timestamp
            FROM Alert a JOIN Task t ON a.task_id = t.task_id AND a.project_id = t.project_id
            JOIN Project p ON t.project_id = p.project_id JOIN ProjectSupervision ps ON p.project_id = ps.project_id
            WHERE ps.prof_id = %s ORDER BY a.alert_timestamp DESC
        """, (prof_id,))
        return jsonify({"success": True, "alerts": cursor.fetchall()})
    finally: cursor.close(); conn.close()

# ================= STUDENT & TASK ENDPOINTS =================
@app.route('/api/student/projects/<student_id>', methods=['GET'])
def get_student_projects(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.project_id, p.title, p.deadline,
            (SELECT AVG(contribution_weight) FROM PeerReview WHERE reviewee_id = tm.student_id AND project_id = tm.project_id) AS my_score
            FROM TeamMembership tm JOIN Project p ON tm.project_id = p.project_id
            WHERE tm.student_id = %s
        """, (student_id,))
        return jsonify({"success": True, "projects": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/student/<project_id>/team', methods=['GET'])
def get_team_members(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT s.student_id, s.name, s.email FROM TeamMembership tm JOIN Student s ON tm.student_id = s.student_id WHERE tm.project_id = %s", (project_id,))
        return jsonify({"success": True, "team": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/tasks/create', methods=['POST'])
def create_task():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if str(data['deadline']) < str(date.today()):
            return jsonify({"error": "Task deadline cannot be in the past."}), 400
            
        cursor.execute("SELECT deadline FROM Project WHERE project_id = %s", (data['project_id'],))
        proj = cursor.fetchone()
        if not proj: return jsonify({"error": "Project not found."}), 404
        
        # Ensures Task deadline never exceeds Project deadline
        if str(data['deadline']) > str(proj['deadline']):
            return jsonify({"error": f"Task deadline cannot be later than project deadline ({proj['deadline']})"}), 400

        cursor.execute("INSERT INTO Task (task_id, project_id, title, status, deadline) VALUES (%s, %s, %s, 'Pending', %s)", (data['task_id'], data['project_id'], data['title'], data['deadline']))
        if data.get('assigned_student_id'):
            cursor.execute("INSERT INTO TaskAssignment (student_id, task_id, project_id) VALUES (%s, %s, %s)", (data['assigned_student_id'], data['task_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Task created."})
    except Error as e: conn.rollback(); return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/tasks/<project_id>', methods=['GET'])
def get_project_tasks(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT t.task_id, t.title, t.status, t.deadline, 
                   GROUP_CONCAT(s.student_id SEPARATOR ', ') AS assigned_ids,
                   GROUP_CONCAT(s.name SEPARATOR ', ') AS assigned_names
            FROM Task t LEFT JOIN TaskAssignment ta ON t.task_id = ta.task_id AND t.project_id = ta.project_id
            LEFT JOIN Student s ON ta.student_id = s.student_id
            WHERE t.project_id = %s GROUP BY t.task_id
        """, (project_id,))
        return jsonify({"success": True, "tasks": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/tasks/update_status', methods=['PUT'])
def update_task_status():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        # Just update the task. Your MySQL Trigger will automatically catch this 
        # and create the perfect Alert row in the background!
        cursor.execute("UPDATE Task SET status = %s WHERE task_id = %s AND project_id = %s", 
                       (data['status'], data['task_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Task status updated."})
    except Error as e: 
        return jsonify({"error": str(e)}), 400
    finally: 
        cursor.close()
        conn.close()

@app.route('/api/tasks/edit', methods=['PUT'])
def edit_task():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if str(data['deadline']) < str(date.today()):
            return jsonify({"error": "Task deadline cannot be in the past."}), 400
            
        cursor.execute("SELECT deadline FROM Project WHERE project_id = %s", (data['project_id'],))
        proj = cursor.fetchone()
        
        # Validates against Project Deadline
        if proj and str(data['deadline']) > str(proj['deadline']):
            return jsonify({"error": f"Task deadline cannot be later than project deadline ({proj['deadline']})"}), 400

        cursor.execute("UPDATE Task SET title = %s, deadline = %s WHERE task_id = %s AND project_id = %s", (data['title'], data['deadline'], data['task_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Task updated."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/tasks/<project_id>/<task_id>', methods=['DELETE'])
def delete_task(project_id, task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Task WHERE task_id=%s AND project_id=%s", (task_id, project_id))
        conn.commit()
        return jsonify({"success": True, "message": "Task deleted successfully."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/tasks/assign', methods=['POST'])
def assign_task_member():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO TaskAssignment (student_id, task_id, project_id) VALUES (%s, %s, %s)", 
                       (data['student_id'], data['task_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Student assigned to task."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/tasks/remove_assignment', methods=['DELETE'])
def remove_task_member():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TaskAssignment WHERE student_id=%s AND task_id=%s AND project_id=%s", 
                       (data['student_id'], data['task_id'], data['project_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Student removed from task."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

# ================= REVIEW ENDPOINTS =================
@app.route('/api/reviews/submit', methods=['POST'])
def submit_review():
    data = request.json
    
    # 1. Self-Review Prevention Check
    if data['reviewer_id'] == data['reviewee_id']:
        return jsonify({"error": "Self-reviews are not permitted."}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 2. Task Assignment Verification Check
        # Ensure the person being reviewed was actually assigned to this specific task
        cursor.execute("""
            SELECT * FROM TaskAssignment 
            WHERE student_id = %s AND task_id = %s AND project_id = %s
        """, (data['reviewee_id'], data['task_id'], data['project_id']))
        
        assignment = cursor.fetchone()
        if not assignment:
            return jsonify({"error": f"Cannot review: Student {data['reviewee_id']} is not assigned to task {data['task_id']}."}), 400

        # 3. If they pass the checks, insert the review
        cursor = conn.cursor() # Switch back to standard cursor for the INSERT
        cursor.execute("""
            INSERT INTO PeerReview (review_id, task_id, project_id, reviewer_id, reviewee_id, contribution_weight, feedback) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['review_id'], data['task_id'], data['project_id'], data['reviewer_id'], data['reviewee_id'], int(data['contribution_weight']), data['feedback']))
        
        conn.commit()
        return jsonify({"success": True, "message": "Review submitted successfully."})
        
    except Error as e: 
        return jsonify({"error": str(e)}), 400
    finally: 
        cursor.close()
        conn.close()

@app.route('/api/student/<student_id>/reviews', methods=['GET'])
def get_received_reviews(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT pr.review_id, pr.project_id, pr.task_id, pr.contribution_weight, pr.feedback, s.name AS reviewer_name
            FROM PeerReview pr JOIN Student s ON pr.reviewer_id = s.student_id WHERE pr.reviewee_id = %s
        """, (student_id,))
        return jsonify({"success": True, "reviews": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/student/<student_id>/given_reviews', methods=['GET'])
def get_given_reviews(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT pr.review_id, pr.project_id, pr.task_id, pr.contribution_weight, pr.feedback, s.name AS reviewee_name
            FROM PeerReview pr JOIN Student s ON pr.reviewee_id = s.student_id WHERE pr.reviewer_id = %s
        """, (student_id,))
        return jsonify({"success": True, "reviews": cursor.fetchall()})
    finally: cursor.close(); conn.close()

@app.route('/api/reviews/edit', methods=['PUT'])
def edit_review():
    data, conn = request.json, get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE PeerReview SET contribution_weight = %s, feedback = %s WHERE review_id = %s", (int(data['contribution_weight']), data['feedback'], data['review_id']))
        conn.commit()
        return jsonify({"success": True, "message": "Review updated."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

@app.route('/api/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM PeerReview WHERE review_id=%s", (review_id,))
        conn.commit()
        return jsonify({"success": True, "message": "Review deleted."})
    except Error as e: return jsonify({"error": str(e)}), 400
    finally: cursor.close(); conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)