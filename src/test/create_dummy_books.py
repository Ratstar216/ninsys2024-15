import sqlite3

def main():
    # test.db というファイルを使う（なければ作られる）
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # テーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    # データの挿入 (INSERT)
    cursor.execute('INSERT INTO books (id, name) VALUES (?, ?)', (2334, "線形代数入門"))
    cursor.execute('INSERT INTO books (id, name) VALUES (?, ?)', (2558, "解析入門"))
    cursor.execute('INSERT INTO books (id, name) VALUES (?, ?)', (2953, "And then there were none"))

    # 変更を保存
    conn.commit()

    # データの取得 (SELECT)
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    for row in rows:
        # row = (id, name, age)
        print(row)

    # 使い終わったらクローズ
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
