import qrcode
from PIL import Image, ImageDraw, ImageFont
import sqlite3

def register():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    while 1:
        r = input("What do you want to register? 1. User, 2. Book, q. Quit: ")
        if r == 'q':
            break
        elif int(r) == 1:
            register_user(conn, cursor)
        elif int(r) == 2:
            register_book(conn, cursor)
    
        else:
            print("Invalid input")
            continue
    
    cursor.close()
    conn.close()

def register_user(conn, cursor):
    id = input("Enter your ID: ")
    name = input("Enter your name: ")
    try:
        cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (id, name))
        conn.commit()
    except:
        print("ID already exists or invalid input, try again")
        return
        
    generate_qr_code(id)
    
def register_book(conn, cursor):
    id = input("Enter the book's ID: ")
    name = input("Enter the book's name: ")
    try:
        cursor.execute('INSERT INTO books (id, name) VALUES (?, ?)', (id, name))
        conn.commit()
    except:
        print("ID already exists or invalid input, try again")
        return
    generate_qr_code(id)


def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=30,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # テキストを画像に描画するためのオブジェクト作成
    draw = ImageDraw.Draw(img)

    # フォントの読み込み
    try:
        font = ImageFont.truetype("Arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()

    # テキストサイズと位置の計算
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_size = (text_width, text_height)
    
    if text_size[0] > img.size[0]:
        font = ImageFont.truetype("Arial.ttf", 15)
        text_size = draw.textsize(text, font)
    
    text_position = ((img.size[0] - text_size[0]) // 2, img.size[1] - text_size[1] - 10)

    # 画像にテキストを描画
    draw.text(text_position, text, font=font, fill="black")
    img.save(f"qrcode/{text}.png")
    img.show()

if __name__ == "__main__":
    register()