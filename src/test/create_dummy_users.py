import sqlite3

def main():
    # test.db というファイルを使う（なければ作られる）
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # テーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    ''')

    # データの挿入 (INSERT)
    cursor.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (1234, "Alice", 30))
    cursor.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (1678, "Bob", 25))
    cursor.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (1999, "Charlie", 100))
    cursor.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (2357, "Gandalf", 1000))

    # 変更を保存
    conn.commit()

    # データの取得 (SELECT)
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        # row = (id, name, age)
        print(row)

    # 使い終わったらクローズ
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
