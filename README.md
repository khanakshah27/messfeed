# messfeed
# MessFeed - Mess Feedback Management System

## Project Overview
MessFeed is a web-based system where students can submit feedback about their mess facilities, and admins can efficiently manage complaints. The system ensures transparency in mess quality monitoring, allowing users to track and resolve issues effectively.

---

## Features
User Authentication** (Students & Admins)  
Submit Feedback** with categories like Food Quality, Cleanliness, etc.  
Track Previous Feedback Entries**  
Admin Dashboard** for Managing Complaints  
Secure MySQL Database Integration**  

---

##Project Structure

```
/messfeed
│── /frontend               # Contains HTML, CSS, JavaScript files
│   ├── index.html          # Login Page
│   ├── feedback.html       # Feedback Submission Page
│   ├── my_feedbacks.html   # View Submitted Feedbacks
│   ├── feedback_report.html # Reports Page
│   ├── admin_dashboard.html # Admin Panel
│── /backend                # Node.js & MySQL API
│   ├── server.js           # Main API logic
│   ├── database.sql        # MySQL database setup
│── package.json            # Backend dependencies
│── README.md               # Documentation
```

---

##  Tech Stack
🔹 **Frontend**: HTML, CSS, JavaScript  
🔹 **Backend**: Node.js, Express.js  
🔹 **Database**: MySQL  
🔹 **Authentication**: JWT (JSON Web Token)  
🔹 **Styling**: Custom CSS  

---

## Setup Instructions

### **1️⃣ Clone the Repository**

git clone https://github.com/khanakshah27/messfeed.git
cd messfeed


### **2️⃣ Install Backend Dependencies**
```sh
cd backend
npm install
```

### **3️⃣ Setup MySQL Database**
- Create a database using `database.sql` script:
```sh
mysql -u root -p < database.sql
```
- Update **server.js** with your **MySQL credentials**.

### **4️⃣ Start the Backend Server**
```sh
node server.js
```
Runs on **http://localhost:5000**

### **5️⃣ Open the Frontend**
- Open `index.html` in a browser.

---

## 📌 Pages & Functionalities

### **1️⃣ Login Page (`index.html`)**
- Users enter their **Registration Number** and **Password**.
- Redirects:
  - **Students** → Feedback submission page.
  - **Admins** → Admin dashboard.

### **2️⃣ Feedback Submission Page (`feedback.html`)**
- Students fill in:
  - **Mess Name**
  - **Type of Mess** (Value/Special)
  - **Block Name**
  - **Room Number**
  - **Feedback Category** (Food Quality, Hygiene, etc.)
  - **Feedback Description**
- Submit feedback to store it in the database.

### **3️⃣ My Feedbacks Page (`my_feedbacks.html`)**
- Displays past feedback entries.
- Shows status (Pending/Resolved) and admin comments.

### **4️⃣ Feedback Report Page (`feedback_report.html`)**
- Summarized reports of mess complaints.
- Trends in mess feedback over time.

### **5️⃣ Admin Dashboard (`admin_dashboard.html`)**
- Admins can:
  - **View all feedback submissions.**
  - **Filter by category and status.**
  - **Change feedback status (Pending → Resolved).**
  - **Add comments to resolved issues.**

---
