import matplotlib.pyplot as plt
import japanize_matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sqlite3


def show_history(id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name FROM books WHERE id = ?', (id,))
    book_name = cursor.fetchone()[0] 

    cursor.execute('''
        SELECT timestamp, latitude, longitude
        FROM history
        WHERE book_id = ?
        ORDER BY timestamp ASC
    ''', (id,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black')
    # ax.add_feature(cfeature.OCEAN, edgecolor='black')
    
    min_lat = min(row[1] for row in rows) - 0.1
    min_lon = min(row[2] for row in rows) - 0.1
    max_lat = max(row[1] for row in rows) + 0.1
    max_lon = max(row[2] for row in rows) + 0.1
    
    lats = [row[1] for row in rows]
    lons = [row[2] for row in rows]
    for i, row in enumerate(rows):
        timestamp, lat, lon = row
        plt.plot(lon, lat, marker=f'${i}$', color='blue', transform=ccrs.PlateCarree())
        plt.text(lon + 0.05, lat, timestamp, transform=ccrs.PlateCarree(),
                 fontsize=8, color='blue',
                 bbox=dict(boxstyle='round,pad=0.2', 
                           alpha=0.5, facecolor='white'))
        
    plt.plot(lons, lats, marker='', color='orange', linewidth=1, alpha=0.4,
            transform=ccrs.PlateCarree())
    
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
    
    plt.title("History of Book ID: {}, TITLE: {}".format(id, book_name))
    plt.show()

if __name__ == "__main__":
    show_history(2558)
        