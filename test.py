from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'skyfall'
DATABASE = 'msgapi.db'



#CONECTION SQLITE3
def get_db():
    conn = sqlite3.connect('msgapi.db')
    return conn


@app.route('/all_messages', methods=['GET'])
def all_messages():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM Messages;')
    messages = cur.fetchall()
    cur.close()
    return messages











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


if __name__ == '__main__':
    app.run(debug=True)













