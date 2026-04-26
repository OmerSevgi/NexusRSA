import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "chat.db"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def init_db():
    """Veritabanını ve tabloları oluşturur."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Kullanıcılar tablosu (password_hash eklendi)
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, public_key TEXT, password_hash TEXT)''')
    # Mesajlar tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  sender TEXT, receiver TEXT, 
                  encrypted_content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    public_key = data.get('public_key')
    
    if not username or not password or not public_key:
        return jsonify({"error": "Eksik bilgi"}), 400
    
    hashed_pw = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, public_key, password_hash) VALUES (?, ?, ?)", 
                  (username, public_key, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({"message": "Başarıyla kayıt olundu"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Kullanıcı adı zaten alınmış"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve şifre gerekli"}), 400
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row and check_password_hash(row[0], password):
        return jsonify({"message": "Giriş başarılı"}), 200
    else:
        return jsonify({"error": "Hatalı kullanıcı adı veya şifre"}), 401

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, public_key FROM users")
    users = [{"username": row[0], "public_key": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    sender = data.get('sender')
    receiver = data.get('receiver')
    encrypted_content = data.get('encrypted_content')
    
    if not sender or not receiver or not encrypted_content:
        return jsonify({"error": "Eksik bilgi"}), 400
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, receiver, encrypted_content) VALUES (?, ?, ?)", 
              (sender, receiver, encrypted_content))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mesaj gönderildi"}), 201

@app.route('/messages/<username>', methods=['GET'])
def get_messages(username):
    # Bu kullanıcıya gelen tüm mesajları getirir
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT sender, receiver, encrypted_content, timestamp FROM messages WHERE receiver = ? OR sender = ?", (username, username))
    messages = [{"sender": row[0], "receiver": row[1], "encrypted_content": row[2], "timestamp": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
