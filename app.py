from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)



@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        sender = data['sender']
        recipient = data['recipient']
        message = data['message']

        conn = sqlite3.connect('msgapi.db')
        c = conn.cursor()

        c.execute('INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)', (sender, recipient, message))
        conn.commit()

        conn.close()

        return jsonify({'message': 'Message sent successfully!'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/inbox/<recipient>', methods=['GET'])
def get_inbox(recipient):
    try:
        conn = sqlite3.connect('msgapi.db')
        c = conn.cursor()

        c.execute('SELECT sender, message FROM messages WHERE recipient = ?', (recipient,))
        messages = c.fetchall()

        conn.close()

        return jsonify([{'sender': message[0], 'message': message[1]} for message in messages]), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)











