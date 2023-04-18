from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
DATABASE = 'msgapi.db'

if __name__ == '__main__':
    app.run(debug=True)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute('INSERT INTO Messages (sender, recipient, message, datetime) VALUES (?, ?, ?, datetime())',
                  (sender, recipient, message))
        db.commit()
        c.close()
    return jsonify({'message': 'Message sent successfully!'})


@app.route('/inbox/<recipient>', methods=['GET'])
def get_inbox(recipient):
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute('SELECT sender, message FROM Messages WHERE recipient = ?', (recipient,))
        messages = c.fetchall()
        c.close()
    return jsonify([{'sender': message[0], 'message': message[1]} for message in messages])
