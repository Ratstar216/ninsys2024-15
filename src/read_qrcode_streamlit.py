import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import io
import time

def read_qr_from_camera(key):
    """
    Streamlit でカメラから撮影し、QRコードを解析して文字列を返す関数。
    QRコードが見つからなければ None を返す。
    """
    st.write("カメラから写真を取得し、QRコードを解析します。")
    
    if "qr_text" not in st.session_state:
        st.session_state["qr_text"] = None
    
    # カメラから写真を撮影するためのウィジェット
    picture = st.camera_input("QRコードをカメラに映して撮影してください", key=key)
    
    
    while picture is None:
        time.sleep(1)
    
    
    if picture is not None:
        # 取得した画像を PIL 形式で読み込む
        img = Image.open(picture)
        
        # pyzbar でデコードする
        decoded_info = decode(img)
        if len(decoded_info) != 0:
            # 複数のQRコードが映った場合は先頭を返す例
            text = decoded_info[0].data.decode('utf-8')
            st.session_state["qr_text"] = text 
            st.success(f"QRコードを検出しました: {text}")
            # return text
        else:
            st.warning("QRコードが検出できませんでした。もう一度試してください。")
            print("QRコードが検出できませんでした。")   
   
    print(type(picture))
    return st.session_state["qr_text"]


def main():
    st.title("Streamlit版 QRコードリーダー")
    st.write("カメラ入力を使って QR コードをスキャンします。")

    result = read_qr_from_camera()
    if result:
        st.write(f"読み取ったテキスト: {result}")
    else:
        st.write("まだ QRコードを読み取っていません。")

if __name__ == "__main__":
    main("main")
