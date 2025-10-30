import flask
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt

## pip install flask-cors
## pip install flask-bcrypt
## pip install psycopg2-binary

# completed
# user, admin login
# feedback entry
# show all feedback to admin <--
#


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="proj1",
        user="postgres",
        password="root1234"
    )

def get_feedbacks():
    # Connect to PostgreSQL
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Fetch feedbacks
    cursor.execute("""
        SELECT feedback_id, reg_no, category, date_time, feedback, status, admin_comments
        FROM feedbacks
        ORDER BY date_time DESC
    """)

    feedbacks = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return feedbacks

#home page
@app.route('/home')
def home():
    return render_template('landpg.html')

# sign in page
@app.route('/feedlog')
def feedlog():
    return render_template('feedlog.html')

# feedback page after student login
@app.route('/regpg')
def regpg():
    return render_template('regpg.html')

# Submit feedback
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    required = ['reg_no', 'category', 'feedback']
    if not all(data.get(field) for field in required):
        return jsonify({"message": "Missing fields"}), 400
    try:
        conn = get_db()
        cur = conn.cursor()

        # Step 1: Fetch user details from users table
        cur.execute("SELECT * FROM users WHERE reg_no = %s;", (data['reg_no'],))
        user = cur.fetchone()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        print("User details:", user)

        # Step 2: Insert feedback into feedbacks table
        cur.execute("""
            INSERT INTO feedbacks (reg_no, category, feedback)
            VALUES (%s, %s, %s)
            RETURNING feedback_id;
        """, (
            data['reg_no'],
            data['category'],
            data['feedback']
        ))

        feedback_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Feedback submitted", "feedback_id": feedback_id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# admin page
@app.route('/admin_home2')
def admin_home2():
    return render_template('admin_home2.html')


##### login APIs
@app.route('/api/login_user', methods=['POST'])
def login_user():
    # debug
    data = request.get_json()
    print("Received JSON:", data)

    #data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing credentials"}), 400  #missing credentials

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Check hashed password
        #if bcrypt.check_password_hash(user['password'], password):
        #    return jsonify({"success": True, "redirect": "/regpg"})

        #check password
        if user['password'].strip() == password:
            return jsonify({"success": True, "redirect": "/regpg"})
        else:
            return jsonify({"success": False, "message": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing credentials"}), 400
    

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM admins WHERE email = %s;", (email,))
        admin = cur.fetchone()
        cur.close()
        conn.close()

        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404

        if admin['password'].strip() == password:
            #print("✅ Admin login successful:", username)
            return jsonify({"success": True, "redirect": "/admin_home2"})
        else:
            return jsonify({"success": False, "message": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# display feedbacks from table
@app.route('/feedrep')
def feedrep():
    feedbacks = get_feedbacks()
    return render_template('feedrep.html', feedbacks=feedbacks)

# New Route for updating feedback
@app.route('/api/update_feedback', methods=['POST'])
def update_feedback():
    feedback_id = request.form['feedback_id']
    admin_comments = request.form['admin_comments']
    status = request.form['status']

    # Validate input
    if not admin_comments:
        return jsonify({"message": "Admin comments are required!"}), 400

    try:
        # Update the database
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE feedbacks
            SET status = %s, admin_comments = %s
            WHERE feedback_id = %s
        """, (status, admin_comments, feedback_id))

        # Commit the changes
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Feedback updated successfully!"})

    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/admin_add_comments')
def admin_add_comments():
    return render_template('admin_add_comments.html')

@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(debug=True)


"""
curl -X POST http://127.0.0.1:5000/api/login_user \
-H "Content-Type: application/json" \
-d '{"email": "john.doe@gmail.com", "password": "p1"}'

CREATE TABLE users (
    reg_no CHAR(9) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    block CHAR(20),
    room_no INT,
    mess_name VARCHAR(100),
    mess_type VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(30) NOT NULL
);

CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(30) NOT NULL
);

CREATE TABLE feedbacks (
    feedback_id SERIAL PRIMARY KEY,
    reg_no VARCHAR(9) REFERENCES users(reg_no) ON DELETE CASCADE,
    category VARCHAR(100),
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    feedback TEXT NOT NULL,
    status VARCHAR(10) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Resolved')),
    admin_id INTEGER REFERENCES admins(admin_id) ON DELETE SET NULL,
    admin_comments TEXT
);


"""
