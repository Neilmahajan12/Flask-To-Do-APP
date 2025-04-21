# Flask-To-Do-APP
# 📝 Flask To-Do App with User Login and Today's Tasks

A user-friendly To-Do List web app built using **Flask**, featuring:

- ✅ User registration & login
- 📋 Task management
- 📆 Mark tasks for “Today’s Work”
- 💾 SQLite + SQLAlchemy database
- 🎨 Styled with custom CSS
- 🔄 REST API for future integrations

---

## 🚀 Features

- 👤 **User Authentication** – Register, log in, and manage personal tasks
- 🧾 **Add/Delete Tasks** – Simple CRUD operations for your to-do list
- 📌 **Mark as Today's Task** – Highlight important tasks for today
- 🌐 **RESTful API** – Easily connect to frontend or mobile apps
- 💅 **Clean UI** – Styled using custom CSS for better UX
- ⚙️ **Flask-Migrate** – Database migrations made easy

---

## Technologies Used

- Python 3
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy
- Flask-Migrate
- Jinja2 (HTML templating)
- SQLite (default DB)

---
## project Structure
flask-todo-app/
│
├── app.py
├── models.py
├── templates/
   └── index.html
   └── login.html
   └── register.html
├── static/
   └── style.css
├── migrations/
├── requirements.txt
└── README.md

## REST API Endpoints

Method | Endpoint | Description
----------|------------------|-------------
GET       | /api/tasks      | List all tasks
POST      | /api/tasks      | Add a new task
PUT       | /api/tasks/<id> | Update task (mark today)
DELETE    | /api/tasks/<id> | Delete a task

## Author
Developed by Nilesh Mahajan
📧 Email: tusharmahajan1209@gmail.com

##  License
MIT License
