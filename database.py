import sqlite3
import json


class Database:

    def open_file(self, filename):
        with open('medicine/{}.json'.format(filename)) as f:
            return json.loads(f.read())

    def __init__(self):
        self.connection = sqlite3.Connection('medicine.sqlite', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def check_user(self, user_id):
        query = '''
        SELECT * 
        FROM users
        WHERE user_id = '{}'
        LIMIT 1
        '''.format(user_id)
        result = self.cursor.execute(query).fetchone()
        return False if result in [None, []] else True

    def create_user(self, user_id, firstname, username):
        query = '''
        INSERT INTO users (user_id, first_name, username)
        VALUES ('{}', '{}', '{}')        
        '''.format(user_id, firstname, username)
        self.cursor.execute(query)
        self.connection.commit()

    def update_user(self, user_id, key, value):
        query = '''
        UPDATE users
        SET {} = '{}'
        WHERE user_id = '{}'
        '''.format(key, value, user_id)
        self.cursor.execute(query)
        self.connection.commit()

    def get_user(self, user_id):
        query = '''
        SELECT *
        FROM users
        WHERE user_id = '{}'
        LIMIT 1 
        '''.format(user_id)
        result = self.cursor.execute(query).fetchone()
        return result

    def check_medicine(self, name):
        query = '''
        SELECT *
        FROM items
        WHERE name = '{}'
        LIMIT 1
        '''.format(name)
        result = self.cursor.execute(query).fetchone()
        return False if result in [None, []] else True

    def get_all_medicines_name(self):
        query = '''
        SELECT name
        FROM items
        '''
        return self.cursor.execute(query).fetchall()

    def get_medicine(self, name):
        query = '''
        SELECT *
        FROM items
        WHERE name = '{}'
        LIMIT 1
        '''.format(name)
        return self.cursor.execute(query).fetchone()


DB = Database()
