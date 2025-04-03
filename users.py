from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO users (username, password_hash) VALUES (?, ?)"""
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id
    return None

def get_username(user_id):
    sql = """SELECT username FROM users WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_id(username):
    sql = """SELECT id FROM users WHERE username = ?"""
    result = db.query(sql, [username])[0]
    return result[0] if result else None

def get_other_users(user_id):
    sql = """SELECT id, username FROM users WHERE id != ?"""
    return db.query(sql, [user_id])

def get_top5():
    sql = """SELECT username, COUNT(e.id) kills
            FROM users u
            LEFT JOIN events e ON e.user_id = u.id
            WHERE e.confirm_status = 1
            GROUP BY username
            ORDER BY COUNT(e.id) DESC
            LIMIT 5"""
    return db.query(sql)