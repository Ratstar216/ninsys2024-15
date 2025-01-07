import folium

def create_map_with_multiple_locations(locations, output_filename='multi_map.html'):
    """
    locations: [(lat, lon, '場所名'), (lat, lon, '場所名'), ...] の形式を想定
    """
    # 地図の中心は、最初の要素を元にする or 平均値などでも OK
    if not locations:
        print("場所のリストが空です。")
        return

    # 最初の地点を中心にする例
    first_lat, first_lon, _ = locations[0]
    m = folium.Map(location=[first_lat, first_lon], zoom_start=13)

    # すべての地点にマーカーを立てる
    for lat, lon, name in locations:
        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    m.save(output_filename)
    print(f"{output_filename} に地図を保存しました。")

if __name__ == '__main__':
    # 複数スポットのリスト (例：東京周辺)
    spots = [
        (35.6812, 139.7671, '東京駅'),
        (35.6895, 139.6917, '新宿駅'),
        (35.6580, 139.7017, '渋谷駅'),
        (35.7295, 139.7114, '池袋駅')
    ]
    create_map_with_multiple_locations(spots, output_filename='tokyo_multi.html')
