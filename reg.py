from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="password",  
    database="mess_feedback"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('regpg.html') 

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        reg_no = request.form['registration_number']
        mess_name = request.form['mess_name']
        student_name = request.form['student_name']
        mess_type = request.form['mess_type']
        block = request.form['block']
        category = request.form['category']
        room_no = request.form['room_no']
        
        query = """
        INSERT INTO feedback (registration_number, mess_name, student_name, mess_type, block, category, room_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (reg_no, mess_name, student_name, mess_type, block, category, room_no)
        cursor.execute(query, values)
        db.commit()
        
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
