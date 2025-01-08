from create_dummy_books import main as create_dummy_books
from create_dummy_users import main as create_dummy_users
from create_dummy_history import main as create_dummy_history

def main():
    create_dummy_books()
    create_dummy_users()
    create_dummy_history()

if __name__ == '__main__':
    main()
