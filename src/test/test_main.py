import sys
sys.path.append('src')
from show_history import show_history

import sqlite3

from datetime import datetime
from zoneinfo import ZoneInfo

USER_ID = 1234
BOOK_ID = 2334

def main():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    while 1:
        r = input("Please select the mode: 1. Scan, 2. Show history: ")
        if int(r) == 1:
            scan(conn, cursor)
            break
        elif int(r) == 2:
            print("Please scan the book's QR code")
            book_id = BOOK_ID
            show_history(book_id)
            break
        else:
            print("Invalid input")
            continue
    
    cursor.close()
    conn.close()
    


def scan(conn, cursor):
    while True:
        print("please scan your QR code")
        user_id = USER_ID
        cursor.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
        res = cursor.fetchone()
        if len(res) == 0:
            print("User not found")
            continue
        _, user_name = res
        break
    
    while True:
        print("please scan the book's QR code")
        book_id = BOOK_ID
        cursor.execute('SELECT id, name FROM books WHERE id = ?', (book_id,))
        if len(res) == 0:
            print("Book not found")
            continue
        _, book_name = res
        break
    

    japan_timezone = ZoneInfo('Asia/Tokyo')
    now_japan = datetime.now(japan_timezone)
    formatted_time = now_japan.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('INSERT INTO history (book_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?)', (book_id, formatted_time, 36.6812, 138.7671))
    conn.commit()


    
        
if __name__ == '__main__':
    main()
        
        
    
        
