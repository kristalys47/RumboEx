import psycopg2
from RumboEx.config.dbconfig import pg_config


class StudentDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2.connect(connection_url)

    def insertStudent(self, username, email, password, name, lastname, program, student_num):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        query2= 'insert into student(student_num, enrolled_program, user_id) values(%s, %s, %s); insert into student_enrolled(student_num) values(%s)'
        cursor.execute(query2, (student_num, program, user_id, student_num))
        self.conn.commit()
        return "Inserted"

    def getallusers(self):
        cursor = self.conn.cursor()
        query = 'select id, username, name, lastname from "user";'
        cursor.execute(query)
        users = []
        for user in cursor:
            users.append(user)
        return users