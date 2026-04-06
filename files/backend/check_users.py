from database import get_db

def check_users():
    db = get_db()
    c = db.execute('SELECT * FROM users')
    users = c.fetchall()
    db.close()
    for u in users:
        print(u)

if __name__ == "__main__":
    check_users()
