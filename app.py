from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"   # needed for login

# Create database
def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            issue TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # simple login (you can change later)
        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect('/admin')
        else:
            return "❌ Invalid credentials"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template('form.html')


# ---------------- SUBMIT ----------------

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']
    priority = request.form['priority']

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tickets (name, email, issue, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'Open', ?)
    ''', (name, email, issue, priority, datetime.now()))

    conn.commit()
    conn.close()

    return redirect('/')


# ---------------- ADMIN ----------------

@app.route('/admin')
def admin():
    # 🔐 protect page
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    conn.close()

    return render_template('admin.html', tickets=tickets)


# ---------------- UPDATE ----------------

@app.route('/update/<int:id>', methods=['POST'])
def update_ticket(id):
    if 'user' not in session:
        return redirect('/login')

    status = request.form['status']

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status=? WHERE id=?", (status, id))

    conn.commit()
    conn.close()

    return redirect('/admin')


# ---------------- DELETE ----------------

@app.route('/delete/<int:id>', methods=['POST'])
def delete_ticket(id):
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/admin')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)