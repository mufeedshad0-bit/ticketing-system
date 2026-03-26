from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect('tickets.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
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

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect(url_for('admin'))
        else:
            return "❌ Invalid credentials"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

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

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tickets (name, email, issue, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'Open', ?)
    ''', (name, email, issue, priority, datetime.now()))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# ---------------- ADMIN ----------------

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if search:
        query += " AND issue LIKE ?"
        params.append(f"%{search}%")

    if status_filter:
        query += " AND status=?"
        params.append(status_filter)

    cursor.execute(query, params)
    tickets = cursor.fetchall()

    # 📊 Dashboard stats
    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'")
    open_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='In Progress'")
    progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        tickets=tickets,
        total=total,
        open_count=open_count,
        progress=progress,
        resolved=resolved
    )

# ---------------- UPDATE ----------------

@app.route('/update/<int:id>', methods=['POST'])
def update_ticket(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    status = request.form['status']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status=? WHERE id=?", (status, id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

# ---------------- DELETE ----------------

@app.route('/delete/<int:id>', methods=['POST'])
def delete_ticket(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run()
