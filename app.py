from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="your_db_name",
        user="your_db_user",
        password="your_db_password"
    )

# User registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    required = ['reg_number', 'password', 'student_name']
    if not all(data.get(field) for field in required):
        return jsonify({"message": "Missing fields"}), 400
    try:
        hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (reg_number, password, student_name)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (data['reg_number'], hashed, data['student_name']))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# User/Admin login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    reg_number = data.get('reg_number')
    password = data.get('password')
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
  
    cur.execute("SELECT * FROM users WHERE reg_number=%s", (reg_number,))
    user = cur.fetchone()
    if user and bcrypt.check_password_hash(user['password'], password):
        cur.close()
        conn.close()
        return jsonify({"message": "Login successful", "role": user['role'], "id": user['id']}), 200

    cur.execute("SELECT * FROM admins WHERE username=%s", (reg_number,))
    admin = cur.fetchone()
    if admin and bcrypt.check_password_hash(admin['password'], password):
        cur.close()
        conn.close()
        return jsonify({"message": "Admin login successful", "role": "admin", "id": admin['id']}), 200
    cur.close()
    conn.close()
    return jsonify({"message": "Invalid credentials"}), 401

# Submit feedback
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    required = ['user_id', 'registration_number', 'mess_name', 'student_name', 'mess_type',
                'block', 'category', 'room_no', 'feedback']
    if not all(data.get(field) for field in required):
        return jsonify({"message": "Missing fields"}), 400
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO feedback (user_id, registration_number, mess_name, student_name, mess_type, block,
                category, room_no, feedback)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id;
        """, (
            data['user_id'], data['registration_number'], data['mess_name'], data['student_name'],
            data['mess_type'], data['block'], data['category'], data['room_no'], data['feedback']
        ))
        feedback_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Feedback submitted", "feedback_id": feedback_id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get feedback list (all or user's)
@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if role == 'student':
        cur.execute("SELECT * FROM feedback WHERE user_id=%s ORDER BY timestamp DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM feedback ORDER BY timestamp DESC;")
    feedbacks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(feedbacks)

# Get single feedback by id
@app.route('/api/feedback/<int:fid>', methods=['GET'])
def get_feedback(fid):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM feedback WHERE id=%s", (fid,))
    feedback = cur.fetchone()
    cur.close()
    conn.close()
    if feedback:
        return jsonify(feedback)
    return jsonify({"message": "Feedback not found"}), 404

# Update feedback status/admin comment
@app.route('/api/feedback/<int:fid>', methods=['PUT'])
def update_feedback(fid):
    data = request.get_json()
    status = data.get('status')
    admin_comment = data.get('admin_comment')
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE feedback SET status=%s, admin_comment=%s WHERE id=%s
        """, (status, admin_comment, fid))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Feedback updated"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Delete feedback
@app.route('/api/feedback/<int:fid>', methods=['DELETE'])
def delete_feedback(fid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM feedback WHERE id=%s", (fid,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Feedback deleted"}), 200

# Get all users (admin use)
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, reg_number, student_name, role FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

# Update user role (admin)
@app.route('/api/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    data = request.get_json()
    role = data.get('role')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role=%s WHERE id=%s", (role, uid))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "User role updated"}), 200

if __name__ == '__main__':
    app.run(debug=True)
