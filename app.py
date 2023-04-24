from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


#CONECTION TO SQLITE
def get_db():
    conn = sqlite3.connect('msgapi.db')
    return conn


#PROFILE/REGISTER
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO Users(name, lastname, email, password) VALUES (?, ?, ?, ?)',
                (data['name'], data['lastname'], data['email'], data['password']))
    db.commit()
    db.close()
    response = {'message': "Registered"}
    return jsonify(response)


#SHOW PROFILE
@app.route('/profile/<user_id>', methods=['GET'])
def profile(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    profile_info = cur.fetchall()
    cur.close()
    return profile_info


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data['sender_id']
    recipient_id = data['recipient_id']
    content = data['content']
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute('INSERT INTO Messages (sender_id, recipient_id, content, datetime) VALUES (?, ?, ?, datetime())',
                  (sender_id, recipient_id, content))
        db.commit()
        c.close()
        return {'Message': 'Message sent!!'}


#RUN FLASK APP
if __name__ == '__main__':
    app.run(debug=True)
