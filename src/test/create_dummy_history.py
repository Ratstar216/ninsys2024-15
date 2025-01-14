import sqlite3

def main():
    # test.db というファイルを使う（なければ作られる）
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # テーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')

    # データの挿入 (INSERT)
    cursor.execute('INSERT INTO history (user_id, book_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (2357, 2334, '2025-01-01 10:00:00', 35.6812, 139.7671))
    cursor.execute('INSERT INTO history (user_id, book_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (2357, 2558, '2025-01-02 10:00:00', 35.6895, 139.6917))
    cursor.execute('INSERT INTO history (user_id, book_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (2357, 9999, '2025-01-03 10:00:00', 35.7295, 139.7114))

    # 変更を保存
    conn.commit()

    # データの取得 (SELECT)
    cursor.execute('SELECT * FROM history')
    rows = cursor.fetchall()
    for row in rows:
        # row = (id, name, age)
        print(row)

    # 使い終わったらクローズ
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
