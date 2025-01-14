import sqlite3
def get_score(id):
    if id is None:
        return None
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT score FROM user_status WHERE id = ?', (id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0]


def get_borrowed_books(id):
    if id is None:
        return None
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT borrowed_books FROM user_status WHERE id = ?', (id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0]

def get_book_name(id):
    if id is None:
        return None
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM books WHERE id = ?', (id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0]

def get_user_name(id):
    if id is None:
        return None
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE id = ?', (id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0]