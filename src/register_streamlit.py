import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import sqlite3
import os

# -- 必要に応じてフォルダ作成（QRコード画像の保存先） --
# os.makedirs("qrcode", exist_ok=True)

# -- セッションステートでボタン押下フラグを初期化 --
if "user_register_button_pressed" not in st.session_state:
    st.session_state["user_register_button_pressed"] = False

if "book_register_button_pressed" not in st.session_state:
    st.session_state["book_register_button_pressed"] = False

def create_connection():
    """DB 接続を作成して返す。"""
    return sqlite3.connect('test.db')

def create_table_if_not_exists():
    """users と books テーブルが無ければ作成する。"""
    conn = create_connection()
    cursor = conn.cursor()
    # users テーブル作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT
        )
    """)
    # books テーブル作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()

def generate_qr_code(text):
    """引数のテキストを持つ QR コードを生成し、画像として返す。"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=30,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    draw = ImageDraw.Draw(img)

    # フォントの読み込み
    try:
        font = ImageFont.truetype("Arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()

    # テキストサイズの計算
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # テキストが大きすぎる場合は文字サイズを小さく
    if text_width > img.size[0]:
        try:
            font = ImageFont.truetype("Arial.ttf", 15)
        except IOError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

    text_position = ((img.size[0] - text_width) // 2, img.size[1] - text_height - 10)
    draw.text(text_position, text, font=font, fill="black")

    # ローカル保存（必要な場合）
    img.save(f"qrcode/{text}.png")
    
    return img

def register_user(user_id, name):
    """ユーザを DB に登録し、QRコードを生成して返す。"""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, name))
        conn.commit()
    except sqlite3.IntegrityError:
        # 重複キーなど
        st.error("ID が既に存在するか、無効です。")
        conn.close()
        return None

    conn.close()
    qr_img = generate_qr_code(user_id)
    return qr_img

def register_book(book_id, name):
    """書籍を DB に登録し、QRコードを生成して返す。"""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO books (id, name) VALUES (?, ?)', (book_id, name))
        conn.commit()
    except sqlite3.IntegrityError:
        # 重複キーなど
        st.error("ID が既に存在するか、無効です。")
        conn.close()
        return None

    conn.close()
    qr_img = generate_qr_code(book_id)
    return qr_img

# -- ボタン押下時のコールバック関数 --
def on_user_register_button_click():
    """ユーザ登録ボタンが押された時に呼ばれるコールバック。"""
    st.session_state["user_register_button_pressed"] = True

def on_book_register_button_click():
    """書籍登録ボタンが押された時に呼ばれるコールバック。"""
    st.session_state["book_register_button_pressed"] = True

def register():

    # テーブルが無い場合は作成しておく
    create_table_if_not_exists()

    # サイドバーで操作を選択できるようにする
    option = st.sidebar.radio("登録するものを選択", ("User", "Book"))

    if option == "User":
        st.header("ユーザ登録")

        # ユーザ情報用のテキスト入力 (セッションキー付き)
        user_id = st.text_input("ユーザ ID を入力", key="user_id")
        user_name = st.text_input("ユーザ名を入力", key="user_name")

        # ボタンにコールバックをセット
        st.button(
            "ユーザ登録",
            key="user_register_button",
            on_click=on_user_register_button_click
        )

        # ボタンが押されたら登録処理を実行
        if st.session_state["user_register_button_pressed"]:
            if user_id and user_name:
                qr_img = register_user(user_id, user_name)
                if qr_img is not None:
                    st.success(f"ユーザ '{user_name}' を登録しました")
                    st.image(qr_img, caption="QR Code", use_column_width=True)
            else:
                st.error("ID と名前を入力してください")

            # 処理が終わったらフラグをオフにしておく
            st.session_state["user_register_button_pressed"] = False

    elif option == "Book":
        st.header("書籍登録")

        # 書籍情報用のテキスト入力 (セッションキー付き)
        book_id = st.text_input("書籍 ID を入力", key="book_id")
        book_name = st.text_input("書籍名を入力", key="book_name")

        # ボタンにコールバックをセット
        st.button(
            "書籍登録",
            key="book_register_button",
            on_click=on_book_register_button_click
        )

        # ボタンが押されたら登録処理を実行
        if st.session_state["book_register_button_pressed"]:
            if book_id and book_name:
                qr_img = register_book(book_id, book_name)
                if qr_img is not None:
                    st.success(f"書籍 '{book_name}' を登録しました")
                    st.image(qr_img, caption="QR Code", use_column_width=True)
            else:
                st.error("ID と書籍名を入力してください")

            # 処理が終わったらフラグをオフにしておく
            st.session_state["book_register_button_pressed"] = False

if __name__ == "__main__":
    register()
