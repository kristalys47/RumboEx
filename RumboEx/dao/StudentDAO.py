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
        query = 'select  u.name, u.lastname, u.username, u.id as user_id, u.email, u.password, s.student_num, s.enrolled_program, r.name as role_name, r.id as role_id, p.name as program_name, d.name as department_name, p.department_num from  users_roles as ur  inner join "user" as u  on u.id=ur.user_id  inner join "role" as r on r.id=ur.role_id inner join student as s on s.user_id=u.id inner join student_enrolled as se on se.student_num=s.student_num inner join "program" as p on p.program_num=s.enrolled_program inner join department as d on d.department_num=p.department_num where r.id=1;'
        cursor.execute(query)
        student = []
        for user in cursor:
            student.append(user)
        return student