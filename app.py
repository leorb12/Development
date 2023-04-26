from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


#CONECTION TO SQLITE
def get_db():
    conn = sqlite3.connect('msgapi.db')
    return conn


# Error handling for invalid requests
@app.errorhandler(400)
def bad_request(error):
    response = jsonify({'message': error.description})
    response.status_code = 400
    return response


# Error handling for database errors
@app.errorhandler(500)
def internal_error(error):
    response = jsonify({'message': 'Database error'})
    response.status_code = 500
    return response


#PROFILE/REGISTER
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute('INSERT INTO Users(name, lastname, email, password) VALUES (?, ?, ?, ?)',
                    (data['name'], data['lastname'], data['email'], data['password']))
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        return jsonify({'message': 'email already registered'}), 400
    finally:
        cur.close()
        db.close()
        response = {'message': "Registered"}
        return jsonify(response)


#SHOW PROFILE
@app.route('/profile/<user_id>', methods=['GET'])
def profile(user_id):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    except sqlite3.IntegrityError:
        db.rollback()
    finally:
        profile_info = cur.fetchall()
        cur.close()
        db.close()
        return profile_info


#SEND MESSAGE
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data['sender_id']
    recipient_id = data['recipient_id']
    content = data['content']
    db = get_db()
    c = db.cursor()
    try:
        c.execute('INSERT INTO Messages (sender_id, recipient_id, content, datetime) VALUES (?, ?, ?, datetime())',
                  (sender_id, recipient_id, content))
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        return jsonify({'message': 'error sending message'}), 400
    finally:
        c.close()
        db.close()
        return {'Message': 'Message sent!!'}


#CHECK INBOX MESSAGES
@app.route('/inbox/<recipient_id>')
def check_inbox(recipient_id):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute('SELECT content FROM Messages WHERE recipient_id == ?', (recipient_id,))
    except sqlite3.IntegrityError:
        db.rollback()
        return jsonify({'message': 'error retrieving message'})
    finally:
        message = cur.fetchall()
        cur.close()
        db.close()
        return message


@app.route('/find_message/<recipient_id')
def find_message(recipient_id):
    db = get_db()
    db.cursor()
    db.execute('SELECT content FROM Messages WHERE recipient_id == ?', (recipient_id,))


#RUN FLASK APP
if __name__ == '__main__':
    app.run(debug=True)
