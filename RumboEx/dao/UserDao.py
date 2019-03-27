import psycopg2
from RumboEx.config.dbconfig import pg_config


class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2.connect(connection_url)

    def insertCounselor(self, username, email, password, name, lastname):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        # self.conn.commit()
        query2 = 'insert into counselor(user_id) values(%s); ' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name="counselor"));'
        cursor.execute(query2, (user_id, user_id))
        self.conn.commit()
        return user_id

    def insertPsychologist(self, username, email, password, name, lastname):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        # self.conn.commit()
        query2 = 'insert into psychologist(user_id) values(%s); ' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name="psychologist"));'
        cursor.execute(query2, (user_id, user_id))
        self.conn.commit()
        return user_id

    def insertAdvisor(self, username, email, password, name, lastname):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        # self.conn.commit()
        query2 = 'insert into advisor(user_id) values(%s); ' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name="advisor"));'
        cursor.execute(query2, (user_id, user_id))
        self.conn.commit()
        return user_id
