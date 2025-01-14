from read_qrcode_streamlit import read_qr_from_camera
from show_history import show_history
from register import register

import sqlite3

from datetime import datetime
from zoneinfo import ZoneInfo

import random 
import time


def main():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    while 1:
        r = input("Please select the mode: 1. Scan, 2. Show history, 3. Register, q. Quit: ")
        if r == 'q':
            break
        elif int(r) == 1:
            scan(conn, cursor)
            break
        elif int(r) == 2:
            print("Please scan the book's QR code")
            book_id = int(read_qr_from_camera())
            show_history(book_id)
            break
        elif int(r) == 3:
            register()
            break
        else:
            print("Invalid input")
            continue
    
    cursor.close()
    conn.close()
    


def scan(conn, cursor):
    while 1:
        print("please scan your QR code")
        user_id = int(read_qr_from_camera())
        cursor.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
        res = cursor.fetchone()
        if len(res) == 0:
            print("User not found")
            time.sleep(5)
            continue
        _, user_name = res
        break
    
    time.sleep(5)
    
    while 1:
        print("please scan the book's QR code")
        book_id = int(read_qr_from_camera())
        cursor.execute('SELECT id, name FROM books WHERE id = ?', (book_id,))
        res = cursor.fetchone()
        if len(res) == 0:
            print("Book not found")
            time.sleep(5)
            continue
        _, book_name = res
        break
    

    japan_timezone = ZoneInfo('Asia/Tokyo')
    now_japan = datetime.now(japan_timezone)
    formatted_time = now_japan.strftime('%Y-%m-%d %H:%M:%S')
    
    rnd_lat = random.uniform(33.6, 35.8)
    rnd_lon = random.uniform(137.0, 140.0)
    cursor.execute('INSERT INTO history (user_id, book_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (user_id, book_id, formatted_time, rnd_lat, rnd_lon))
    conn.commit()
    
    print("Successfully scanned")
    print("User ID: {}, User Name: {}".format(user_id, user_name))
    print("Book ID: {}, Book Name: {}".format(book_id, book_name))


    
        
if __name__ == '__main__':
    main()
        
        
    
        
