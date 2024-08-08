import sqlite3


def connect():
    conn = sqlite3.connect('testdb.db')
    cursor = conn.cursor()
    return conn, cursor


def create_table():
    conn, cursor = connect()
    cursor.executescript('''
    drop table if exists users;
    create table if not exists users(
        user_id integer primary key autoincrement,
        chat_id integer not null
    );
    
    DROP TABLE IF EXISTS test_images;
    CREATE TABLE IF NOT EXISTS test_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id integer references users(user_id),
        photo_path TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()


def get_user_id(chat_id: int):
    conn, cursor = connect()

    cursor.execute('select user_id from users where chat_id=?', (chat_id,))
    try:
        return cursor.fetchone()[0]
    except Exception as e:
        return


def create_user(chat_id: int):
    conn, cursor = connect()
    if get_user_id(chat_id):
        return
    cursor.execute('insert into users(chat_id) values (?)', (chat_id,))
    conn.commit()
    conn.close()





def create_photo_path(user_id: int, photo_path: str):
    conn, cursor = connect()
    cursor.execute('insert into test_images(user_id, photo_path) values (?, ?)',
                   (user_id, photo_path))
    conn.commit()
    conn.close()


def get_user_photo_path(user_id: int):
    conn, cursor = connect()
    cursor.execute('select photo_path from test_images where user_id=?', (user_id,))
    try:
        return cursor.fetchone()[0]
    except Exception as e:
        return


# create_table()