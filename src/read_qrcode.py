import cv2
from pyzbar.pyzbar import decode

def read_qr_from_camera():
    # 0 はカメラのデバイス番号（Mac の場合、0 で認識されるケースが多い）
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("カメラが見つかりませんでした。")
        return
    
    print("カメラを起動しました。QR コードをカメラに映してください。")
    print("終了するにはキーボードの 'q' を押してください。")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("カメラからフレームを取得できませんでした。")
            break
        
        # pyzbar でデコード
        decoded_info = decode(frame)
        if len(decoded_info) != 0:
            for info in decoded_info:
                text = info.data.decode('utf-8')
                print("read_qr_from_camera", text)
                return text
        
        # フレーム上にデコードした結果を表示 (QR コードの位置と内容)
        for info in decoded_info:
            x, y, w, h = info.rect
            # QR コードの四角枠を描画
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # デコードした内容をフレーム上に描画
            text = info.data.decode('utf-8')
            print("text", text)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 255, 0), 2)
        
        # ウィンドウに表示
        cv2.imshow("QRコード Reader", frame)

        # 'q' が押されたらループを抜けて終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_from_camera()
