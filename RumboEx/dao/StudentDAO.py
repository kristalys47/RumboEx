import psycopg2
from RumboEx.config.dbconfig import pg_config


class StudentDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2.connect(connection_url)

    def insertStudent(self, username, email, password, name, lastname, program, student_num, phone_num):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        query2 = 'insert into student(student_num, enrolled_program, user_id, phone_num) values(%s, %s, %s, %s) ' \
                 'returning user_id;' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name=%s)) ' \
                 'returning user_id, role_id;'
                # 'insert into mentors_students(mentor_id, student_id) values(%s, %s), (%s, %s), (%s, %s); ' \
        cursor.execute(query2, (student_num, program, user_id, phone_num, user_id, 'student'))
        result = cursor.fetchall()
        if result:
            self.conn.commit()
        else:
            cursor.execute('rollback;',)
        return user_id

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
                'nullif(s.student_num, null) as student_num, ' \
                's.enrolled_program as program_num, p.name as program_name, ' \
                'f.faculty_num, f.name as faculty_name, ' \
                'r.id as role_id, r.name as role_name, ' \
                'nullif(s.phone_num, null) as phone_num ' \
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
                'nullif(s.student_num, null) as student_num, ' \
                's.enrolled_program as program_num, p.name as program_name, ' \
                'f.faculty_num, f.name as faculty_name, ' \
                'r.id as role_id, r.name as role_name,' \
                'nullif(s.phone_num, null) as phone_num ' \
                'from ' \
                '"user" as u inner join student as s on u.id=s.user_id ' \
                'inner join users_roles as ur on ur.user_id=u.id ' \
                'inner join "role" as r on r.id=ur.role_id ' \
                'inner join program as p on p.program_num=s.enrolled_program ' \
                'inner join faculty as f on f.faculty_num=p.faculty_num ' \
                'where u.id=%s;'
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

    def getStudentsByMentorId(self, mentor_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                'u.id, u.username, u.name, u.lastname, u.email, u.password, ' \
                'nullif(s.student_num, null) as student_num, ' \
                's.enrolled_program as program_num, p.name as program_name, ' \
                'f.faculty_num, f.name as faculty_name, ' \
                'r.id as role_id, r.name as role_name, ' \
                'nullif(s.phone_num, null) as phone_num ' \
                'from ' \
                '"user" as u inner join student as s on u.id=s.user_id ' \
                'inner join users_roles as ur on ur.user_id=u.id ' \
                'inner join "role" as r on r.id=ur.role_id ' \
                'inner join program as p on p.program_num=s.enrolled_program ' \
                'inner join faculty as f on f.faculty_num=p.faculty_num ' \
                'inner join mentors_students as m on (u.id=m.student_id) ' \
                'where m.mentor_id=%s;'
        cursor.execute(query, (mentor_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # PUT Methods

    def changePhoneNumber(self, phone, user_id):
        cursor = self.conn.cursor()
        query = 'update student set phone_num = %s where user_id = %s returning user_id, phone_num as new_phone_num;'
        cursor.execute(query,(phone,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changeStundentNumber(self, studentNum, user_id):
        cursor = self.conn.cursor()
        query = 'update student set student_num = %s where user_id = %s returning user_id, student_num as new_student_num;'
        cursor.execute(query,(studentNum,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changeProgram(self, program, user_id):
        cursor = self.conn.cursor()
        query = 'update student set enrolled_program = %s where user_id = %s returning user_id, enrolled_program as enrolled_program;'
        cursor.execute(query,(program,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changeName(self, name, user_id):
        cursor = self.conn.cursor()
        query = 'update "user" set name=%s where id=%s returning id, name as new_name;'
        cursor.execute(query,(name,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changeLastname(self, lastname, user_id):
        cursor = self.conn.cursor()
        query = 'update "user" set lastname=%s where id=%s returning id, lastname as new_lastname;'
        cursor.execute(query,(lastname,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changeUsername(self, username, user_id):
        cursor = self.conn.cursor()
        query = 'update "user" set username=%s where id=%s returning id, username as new_username;'
        cursor.execute(query,(username,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changeEmail(self, email, user_id):
        cursor = self.conn.cursor()
        query = 'update "user" set email=%s where id=%s returning id, email as new_email;'
        cursor.execute(query,(email,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res

    def changePassword(self, password, user_id):
        cursor = self.conn.cursor()
        query = 'update "user" set password=%s where id=%s returning id;'
        cursor.execute(query,(password,user_id,))
        res = cursor.fetchone()
        if res:
            self.conn.commit()
        return res