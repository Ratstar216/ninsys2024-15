from datetime import datetime
from zoneinfo import ZoneInfo

# 日本のタイムゾーンを設定
japan_timezone = ZoneInfo('Asia/Tokyo')

# 現在の日本時間を取得
now_japan = datetime.now(japan_timezone)

# フォーマットを指定して表示
formatted_time = now_japan.strftime('%Y-%m-%d %H:%M:%S')
print(formatted_time)
