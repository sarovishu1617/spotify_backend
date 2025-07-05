from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow Flutter to access

# Database setup (run this only once to create db & table)
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'User registered'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'fail', 'message': 'User already exists'})

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT name, email FROM users WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({'status': 'success', 'name': user[0], 'email': user[1]})
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
