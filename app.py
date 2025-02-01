from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "auth.db"

# Initialize database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key TEXT PRIMARY KEY,
                approved INTEGER DEFAULT 0
            )
        """)
    conn.close()

init_db()

# Register a new key
@app.route("/register", methods=["POST"])
def register_key():
    data = request.json
    key = data.get("key")
    
    if not key:
        return jsonify({"error": "Key is required"}), 400
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO keys (key) VALUES (?)", (key,))
        conn.commit()
    
    return jsonify({"message": "Key registered successfully"}), 200

# Check if key is approved
@app.route("/check/<key>", methods=["GET"])
def check_key(key):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT approved FROM keys WHERE key = ?", (key,))
        result = cursor.fetchone()
    
    if result and result[0]:
        return jsonify({"approved": True}), 200
    return jsonify({"approved": False}), 200

# Admin - Get pending keys
@app.route("/pending_keys", methods=["GET"])
def get_pending_keys():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM keys WHERE approved = 0")
        keys = [row[0] for row in cursor.fetchall()]
    
    return jsonify({"pending_keys": keys}), 200

# Admin - Approve a key
@app.route("/approve/<key>", methods=["POST"])
def approve_key(key):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE keys SET approved = 1 WHERE key = ?", (key,))
        conn.commit()
    
    return jsonify({"message": f"Key {key} approved"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
