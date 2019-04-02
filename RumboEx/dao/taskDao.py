from RumboEx.config.dbconfig import pg_config
import psycopg2


class TaskDAO:
    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    # GET Methods

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        query = "select * from task;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    # We don't need these methods

    # def get_personal_tasks(self):
    #     cursor = self.conn.cursor()
    #     query = "select * from task natural inner join personal_task;"
    #     cursor.execute(query)
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     if not result:
    #         return None
    #     return result
    #
    # def get_study_tasks(self):
    #     cursor = self.conn.cursor()
    #     query = "select * from task natural inner join study_task;"
    #     cursor.execute(query)
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     if not result:
    #         return None
    #     return result
    #
    # def get_course_tasks(self):
    #     cursor = self.conn.cursor()
    #     query = "select * from task natural inner join course_task;"
    #     cursor.execute(query)
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     if not result:
    #         return None
    #     return result
    #
    # def get_tasks_by_student_id(self, student_id):
    #     cursor = self.conn.cursor()
    #     query = "select * from task natural inner join student_tasks where student_id = %s;"
    #     cursor.execute(query, (student_id,))
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     if not result:
    #         return None
    #     return result

    def get_personal_tasks_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                't.task_id, t.task_name, t.task_description, t.start_time, t.end_time, t.finished ' \
                'from ' \
                'task as t inner join personal_task using(task_id) ' \
                'natural inner join student_tasks where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_study_tasks_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                't.task_id, t.task_name, t.task_description, t.start_time, t.end_time, t.finished, s.course_id ' \
                'from ' \
                'task as t inner join study_task as s using(task_id) ' \
                'natural inner join student_tasks where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_course_tasks_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                't.task_id, t.task_name, t.task_description, t.start_time, t.end_time, t.finished ' \
                'from task as t ' \
                'inner join course_task using (task_id) natural inner join student_tasks where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_appointment_tasks_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                't.task_id, t.task_name, t.task_description, t.start_time, t.end_time, t.finished ' \
                'from task as t inner join appointment_task using (task_id) ' \
                'natural inner join student_tasks where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_study_tasks_by_user_id_and_course_id(self, user_id, course_id):
        cursor = self.conn.cursor()
        query = "select " \
                "t.task_id, t.task_name, t.task_description, t.start_time, t.end_time, t.finished " \
                "from " \
                "task as t inner join study_task using (task_id) " \
                "natural inner join student_tasks " \
                "where user_id = %s and course_id=%s;"
        cursor.execute(query, (user_id, course_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_student_course(self, user_id):
        cursor = self.conn.cursor()
        query = 'select course.name from "user", student_courses, course where user_id = id and codification = course_id and user_id = %s;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_all_courses(self):
        cursor = self.conn.cursor()
        query = 'select name, codification, section from course;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_study_task_count_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = "select count(*) from study_task natural inner join student_tasks where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
           return None
        print(result)
        return result
   
    def get_personal_task_count_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = "select count(*) from personal_task natural inner join student_tasks where user_id = %s;"
        cursor.execute(query,(user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
           return None
        print(result)
        return result
    
    def get_appointment_task_count_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = "select count(*) from appointment_task natural inner join student_tasks where user_id = %s;"
        cursor.execute(query,(user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
           return None
        print(result)
        return result
    
    def get_course_task_count_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        query = "select count(*) from course_task natural inner join student_tasks where user_id = %s;"
        cursor.execute(query,(user_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
           return None
        print(result)
        return result

    # POST Methods

    def add_task(self, name, description, start_time, end_time, status):
        cursor = self.conn.cursor()
        print(name, description, start_time, end_time, status)
        query = "insert into task(task_name, task_description, start_time, end_time, finished) values (%s, %s, %s, %s, %s) returning task_id;"
        cursor.execute(query, (name, description, start_time, end_time, status,))
        task_id = cursor.fetchone()
        self.conn.commit()
        return task_id

    def add_personal_task(self, name, description, start_time, end_time, status):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into personal_task(task_id) values (%s);"
        cursor.execute(query, (task_id,))
        self.conn.commit()
        return task_id

    def add_study_task(self, name, description, start_time, end_time, status, course_id):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into study_task(task_id, course_id) values (%s, %s);"
        cursor.execute(query, (task_id, course_id,))
        self.conn.commit()
        return task_id

    def add_course_task(self, name, description, start_time, end_time, status, course_id):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into course_task(task_id, course_id) values (%s, %s);"
        cursor.execute(query, (task_id, course_id,))
        self.conn.commit()
        return task_id

    def add_appointment_task(self, name, description, start_time, end_time, status):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into appointment_task(task_id) values (%s);"
        cursor.execute(query, (task_id,))
        self.conn.commit()
        return task_id

    def add_task_to_user(self, user_id, task_id):
        cursor = self.conn.cursor()
        query = "insert into student_tasks(user_id, task_id) values (%s, %s) returning task_id;"
        cursor.execute(query, (user_id, task_id,))
        primary_key = cursor.fetchone()
        self.conn.commit()
        return primary_key

    # PUT Methods

    def change_task_name(self, task_id, task_name):
        cursor = self.conn.cursor()
        query = 'update task set task_name = %s where task_id = %s;'
        cursor.execute(query,(task_name,task_id,))
        self.conn.commit()

    def change_task_description(self, task_id, task_description):
        cursor = self.conn.cursor()
        query = 'update task set task_description = %s where task_id = %s;'
        cursor.execute(query,(task_description,task_id,))
        self.conn.commit()

    def change_task_start_time(self, task_id, task_start_time):
        cursor = self.conn.cursor()
        query = 'update task set start_time = %s where task_id = %s;'
        cursor.execute(query,(task_start_time,task_id,))
        self.conn.commit()

    def change_task_end_time(self, task_id, task_end_time):
        cursor = self.conn.cursor()
        query = 'update task set end_time = %s where task_id = %s;'
        cursor.execute(query,(task_end_time,task_id,))
        self.conn.commit()

    def change_task_finished(self, task_id, finished):
        cursor = self.conn.cursor()
        query = 'update task set finished = %s where task_id = %s;'
        cursor.execute(query,(finished,task_id,))
        self.conn.commit()