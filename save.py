import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('Muhammadyusuf.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            create table if not exists users(
                id integer primary key,
                name varchar not null,
                age integer,
                address varchar,
                photo varchar)""")

    def add_user(self, name, age, address, photo):
        self.cursor.execute("""insert into users
                            (name, age, address, photo)
                            values (?, ?, ?, ?)""",
                            (name, age, address, photo))
        self.connection.commit()

    def show_users(self):
        users = self.cursor.execute("select * from users")
        return users.fetchall()
    #
    def get_user(self, id):
        user = self.cursor.execute("select * from users where id=?",
                                   (id, ))
        return user.fetchone()

    def update_user_name(self, id, name):
        self.cursor.execute("update users set name=? where id=?", (name, id))
        self.connection.commit()

    def update_user_age(self, id, age):
        self.cursor.execute("update users set age=? where id=?", (age, id))
        self.connection.commit()

    def update_user_address(self, id, address):
        self.cursor.execute("update users set address=? where id=?", (address, id))
        self.connection.commit()

    def update_user_photo(self, id, photo):
        self.cursor.execute("update users set photo=? where id=?", (photo, id))
        self.connection.commit()


db = Database()



