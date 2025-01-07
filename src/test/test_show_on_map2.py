import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_with_cartopy(lat, lon):
    # 投影法を PlateCarree として設定（単純な経緯度投影）
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # 海岸線などの地理情報を追加
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    
    # 地図の範囲を緯度経度で指定（例: ±10度を表示）
    ax.set_extent([lon - 5, lon + 5, lat - 5, lat + 5], crs=ccrs.PlateCarree())
    
    # 指定した場所を点で表示
    plt.plot(lon, lat, marker='o', color='red', transform=ccrs.PlateCarree())
    
    plt.title("Cartopy Example")
    plt.show()

if __name__ == "__main__":
    # 例: 東京駅付近
    lat = 35.6812
    lon = 139.7671
    plot_with_cartopy(lat, lon)
