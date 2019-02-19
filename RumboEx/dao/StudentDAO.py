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
        query2= 'insert into student(student_num, enrolled_program, user_id) values(%s, %s, %s); insert into student_enrolled(student_num) values(%s); insert into users_roles(user_id, role_id) values (%s, 1);'
        cursor.execute(query2, (student_num, program, user_id, student_num, user_id))
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

    def getallstudent(self):
        cursor = self.conn.cursor()
        query = 'select ' \
                'u.id, u.username, u.name, u.lastname, u.email, u.password, ' \
                's.student_num, s.enrolled_program as program_num, ' \
                'p.name as program_name, ' \
                'f.faculty_num, f.name as faculty_name, ' \
                'r.id as role_id, r.name as role_name ' \
                'from ' \
                '"user" as u inner join student as s on u.id=s.user_id ' \
                'inner join users_roles as ur on ur.user_id=u.id ' \
                'inner join "role" as r on r.id=ur.role_id ' \
                'inner join program as p on p.program_num=s.enrolled_program ' \
                'inner join faculty as f on f.faculty_num=p.faculty_num;'
        cursor.execute(query)
        student = []
        for user in cursor:
            student.append(user)
        return student

    def getStudent(self, user_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                'u.id, u.username, u.name, u.lastname, u.email, u.password, ' \
                's.student_num, ' \
                's.enrolled_program as program_num, p.name as program_name, ' \
                'f.faculty_num, f.name as faculty_name, ' \
                'r.id as role_id, r.name as role_name ' \
                'from ' \
                '"user" as u inner join student as s on u.id=s.user_id ' \
                'inner join users_roles as ur on ur.user_id=u.id ' \
                'inner join "role" as r on r.id=ur.role_id ' \
                'inner join program as p on p.program_num=s.enrolled_program ' \
                'inner join faculty as f on f.faculty_num=p.faculty_num ' \
                'where u.id=%s;'
        cursor.execute(query, (user_id,))
        return cursor.fetchone()