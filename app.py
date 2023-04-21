from flask import Flask, request
import sqlite3

app = Flask(__name__)


#CONECTION TO SQLITE
def get_db():
    conn = sqlite3.connect('msgapi.db')
    return conn


#PROFILE/REGISTER
@app.route('/register_user', methods=['POST'])
def register_user():
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT ')




@app.route('/profile/<name>', methods=['GET'])
def profile(name):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM Users WHERE name = ?', (name,))
    profile_info = cur.fetchall()
    cur.close()
    return profile_info



