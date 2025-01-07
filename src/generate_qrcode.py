import qrcode
from PIL import Image, ImageDraw, ImageFont

class RESTAUNT_QR:
    def __init__(self):
        self.sentence = ""

    def generate_qr_code(selr,command):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=30,
            border=4,
        )
        qr.add_data(command)
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
        bbox = draw.textbbox((0, 0), command, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_size = (text_width, text_height)
        
        if text_size[0] > img.size[0]:
            font = ImageFont.truetype("Arial.ttf", 15)
            text_size = draw.textsize(command, font)
        
        text_position = ((img.size[0] - text_size[0]) // 2, img.size[1] - text_size[1] - 10)

        # 画像にテキストを描画
        draw.text(text_position, command, font=font, fill="black")
        img.show()

    def choose_order(self):
        order = input("注文したい品物を入力してください")
        number = input("個数を入力してください")
        self.sentence = number + order
        self.sentence = order
        self.generate_qr_code(self.sentence)


    def main(self):
        for i in range(1):
            self.choose_order()

if __name__ == "__main__":
    res_qr = RESTAUNT_QR()
    res_qr.main()