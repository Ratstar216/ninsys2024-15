import sqlite3

def main():
    # test.db というファイルを使う（なければ作られる）
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # テーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            borrowed_books INTEGER
        )
    ''')

    # データの挿入 (INSERT)
    cursor.execute('INSERT INTO user_status (id, score, borrowed_books) VALUES (?, ?, ?)', (1111, 0, None))
    cursor.execute('INSERT INTO user_status (id, score, borrowed_books) VALUES (?, ?, ?)', (1234, 0, None))
    cursor.execute('INSERT INTO user_status (id, score, borrowed_books) VALUES (?, ?, ?)', (1678, 0, None))
    cursor.execute('INSERT INTO user_status (id, score, borrowed_books) VALUES (?, ?, ?)', (1999, 0, None))
    cursor.execute('INSERT INTO user_status (id, score, borrowed_books) VALUES (?, ?, ?)', (2357, 0, None))

    # 変更を保存
    conn.commit()

    # データの取得 (SELECT)
    cursor.execute('SELECT * FROM user_status')
    rows = cursor.fetchall()
    for row in rows:
        # row = (id, name, age)
        print(row)

    # 使い終わったらクローズ
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
