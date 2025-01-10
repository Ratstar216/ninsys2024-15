import streamlit as st
import sqlite3
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo


from read_qrcode_streamlit import read_qr_from_camera
from show_history_streamlit import show_history
from register_streamlit import register


def do_scan():
    """
    スキャン処理を行う関数。
    元の scan(conn, cursor) の流れを踏襲しています。
    """
    # データベースに接続
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # 1) ユーザIDの読み取り
    st.write("Step 1: ユーザのQRコードを読み取ります")
    user_scan_btn = st.button("ユーザQRコードをスキャン")
    user_id = None
    if user_scan_btn:
        st.session_state["user_scan_btn"] = True
    if st.session_state["user_scan_btn"]:
        # 実際にはカメラ等から取得する想定
        user_id = int(read_qr_from_camera("user_id_1"))

        cursor.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
        res = cursor.fetchone()
        if res is None:
            st.error("User not found. 5秒待機して再スキャンしてください。")
            time.sleep(5)
        else:
            _, user_name = res
            st.success(f"ユーザ認証に成功: ID={user_id}, Name={user_name}")

    # 2) 本のIDの読み取り
    book_id = None
    if user_id is not None:
        st.write("Step 2: 書籍のQRコードを読み取ります")
        book_scan_btn = st.button("書籍QRコードをスキャン")
        if book_scan_btn:
            st.session_state["book_scan_btn"] = True
        if st.session_state["book_scan_btn"]:
            book_id = int(read_qr_from_camera("book_id_1"))

            cursor.execute('SELECT id, name FROM books WHERE id = ?', (book_id,))
            res = cursor.fetchone()
            if res is None:
                st.error("Book not found. 5秒待機して再スキャンしてください。")
                time.sleep(5)
            else:
                _, book_name = res
                st.success(f"書籍スキャンに成功: ID={book_id}, Name={book_name}")

    # 3) DBへの履歴登録
    if user_id is not None and book_id is not None:
        st.write("Step 3: 履歴への登録")
        st.write(f"User ID: {user_id}, User Name: {user_name}")
        st.write(f"Book ID: {book_id}, Book Name: {book_name}")
        register_btn = st.button("履歴をDBに登録")
        if register_btn:
            st.session_state["register_btn"] = True
        if st.session_state["register_btn"]:
            japan_timezone = ZoneInfo('Asia/Tokyo')
            now_japan = datetime.now(japan_timezone)
            formatted_time = now_japan.strftime('%Y-%m-%d %H:%M:%S')

            rnd_lat = random.uniform(33.6, 35.8)
            rnd_lon = random.uniform(137.0, 140.0)
            cursor.execute(
                'INSERT INTO history (user_id, book_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?)',
                (user_id, book_id, formatted_time, rnd_lat, rnd_lon)
            )
            conn.commit()
            st.success("Successfully scanned")
            st.write(f"User ID: {user_id}, User Name: {user_name}")
            st.write(f"Book ID: {book_id}, Book Name: {book_name}")

    # 処理が終わったらクローズ
    cursor.close()
    conn.close()


def do_show_history():
    """
    本の履歴（History）を表示する関数。
    元の「show_history(book_id)」を活用。
    """
    st.write("履歴を表示したい書籍のQRコードをスキャンしてください。")
    scan_book_btn = st.button("書籍QRコードをスキャン")
    if scan_book_btn:
        st.session_state["scan_book_btn"] = True
    if st.session_state["scan_book_btn"]:
        book_id = int(read_qr_from_camera("book_id_2"))
        st.write(f"Book ID: {book_id} をスキャンしました。")
        # show_history(book_id) の戻り値や標準出力に依存する場合は
        # 返り値をprintではなくreturnするように修正し、ここで受け取るなど対応が必要
        print("book_id", book_id)
        show_history(book_id)  # 標準出力している場合は、streamlit上で print 出力が見えないかもしれません
        st.success(f"Book ID {book_id} の履歴を表示しました。")
        print("show_history done")

def do_register():
    """
    新規登録の処理を行う関数。
    元の register() 関数を呼び出すだけにしています。
    実際には register() 内部の実装をGUI化する必要があるかもしれません。
    """
    st.write("新規登録を行います。")
    register_new_btn = st.button("登録開始")
    if register_new_btn:
        st.session_state["register_new_btn"] = True
    if st.session_state["register_new_btn"]:
        # register.py 内の register() をそのまま呼び出す
        # register() の中で input() などを使っている場合は、同様にStreamlit対応が必要
        register()
        


def main():
    st.title("ninsys2024-15: Streamlit版（仮）")
    
    if "user_scan_btn" not in st.session_state:
        st.session_state["user_scan_btn"] = False
    if "book_scan_btn" not in st.session_state:
        st.session_state["book_scan_btn"] = False
    if "register_btn" not in st.session_state:
        st.session_state["register_btn"] = False
    if "register_new_btn" not in st.session_state:
        st.session_state["register_new_btn"] = False
    if "scan_book_btn" not in st.session_state:
        st.session_state["scan_book_btn"] = False


    # モード選択をラジオボタンなどで実装
    mode = st.radio(
        "モードを選択してください",
        ("Scan", "Show History", "Register")
    )

    if mode == "Scan":
        do_scan()
    elif mode == "Show History":
        do_show_history()
    elif mode == "Register":
        do_register()


if __name__ == "__main__":
    main()
