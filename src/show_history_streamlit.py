import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sqlite3
from gemini import ask_gemini
from get_functions import get_book_name

def show_history(book_id):
    """
    指定した book_id の履歴をデータベースから取得し、
    Cartopy を使った地図上にプロットしたグラフを Streamlit 上に表示する。
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # 書籍名の取得
    cursor.execute('SELECT name FROM books WHERE id = ?', (book_id,))
    res = cursor.fetchone()
    if res is None:
        st.write("The book is not registered.")
        cursor.close()
        conn.close()
        return
    book_name = res[0]

    # 履歴データの取得
    cursor.execute('''
        SELECT timestamp, latitude, longitude
        FROM history
        WHERE book_id = ?
        ORDER BY timestamp ASC
    ''', (book_id,))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not rows:
        st.write("No history found for this book.")
        return

    # 履歴のテーブル的な出力（テキストで確認したい場合）
    st.write("## 取得データ一覧")
    for row in rows:
        st.write(row)
    
    # 地図を表示するための Figure を作成
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # 地図にいくつかのフィーチャーを追加
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    
    # 座標範囲を計算
    min_lat = min(row[1] for row in rows) - 0.1
    min_lon = min(row[2] for row in rows) - 0.1
    max_lat = max(row[1] for row in rows) + 0.1
    max_lon = max(row[2] for row in rows) + 0.1
    
    # 軌跡をプロット
    lats = [row[1] for row in rows]
    lons = [row[2] for row in rows]
    for i, (timestamp, lat, lon) in enumerate(rows):
        ax.plot(lon, lat, marker=f'${i}$', color='blue', transform=ccrs.PlateCarree())
        ax.text(lon + 0.05, lat, timestamp,
                transform=ccrs.PlateCarree(),
                fontsize=8, color='blue',
                bbox=dict(boxstyle='round,pad=0.2', alpha=0.5, facecolor='white'))
        
    # 全体の軌跡を線で表示
    ax.plot(lons, lats, marker='', color='orange', linewidth=1, alpha=0.4, transform=ccrs.PlateCarree())
    
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
    ax.set_title(f"History of Book ID: {book_id}, TITLE: {book_name}")
    
    st.pyplot(fig)
    r = ask_gemini(get_book_name(book_id), rows)
    st.write("説明")
    st.write(r)

def main():
    st.title("書籍の履歴マップ表示アプリ")
    
    # Book ID をユーザー入力で受け取る
    book_id = st.number_input("Book ID を入力してください", min_value=1, step=1, value=1)
    
    # ボタンを押したら実行
    if st.button("履歴を表示"):
        show_history(book_id)

if __name__ == "__main__":
    main()
