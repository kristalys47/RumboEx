from RumboEx.config.dbconfig import pg_config
import psycopg2


class CourseDAO:
    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    # GET Methods

    def get_courses_by_student_id(self, student_id):
        cursor = self.conn.cursor()

        query = 'select ' \
                'c.course_id, c.name, c.codification, c.credits, s.section_num, s.section_id, e.enrolled_id ' \
                'from ' \
                'enrolled as e  ' \
                'natural inner join course as c ' \
                'natural inner join section as s ' \
                'where e.student_id=%s;'
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_course_by_course_id(self, course_id):
        cursor = self.conn.cursor()
        query = "select * from course where course_id = %s;"
        cursor.execute(query, (course_id,))
        result = cursor.fetchone()
        if not result:
            return None
        return result

    def get_section_times_by_section_id(self, section_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                's.day, s.start_time, s.end_time ' \
                'from section_time as s ' \
                'where section_id=%s;'
        cursor.execute(query, (section_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_grades_by_course_id(self, enrolled_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                'g.grade_id, g.g_name, g.grade, g.total, g.weight, g.g_date ' \
                'from ' \
                'grades as g natural inner join enrolled ' \
                'where enrolled.enrolled_id=%s;'
        cursor.execute(query, (enrolled_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    # POST Methods

    def insert_grade(self, name, grade, total, weight, date, student_id, course_id):
        cursor = self.conn.cursor()
        query1 = 'select e.enrolled_id from enrolled as e natural inner join section as s ' \
                 'where e.student_id=%s and s.course_id=%s;'
        cursor.execute(query1, (student_id, course_id, ))
        enrolled_id = cursor.fetchone()[0]
        if not enrolled_id:
            return None
        # if date is None:
        #     date = 'null'
        print(enrolled_id, name, grade, total, weight, date, student_id, course_id)
        query2 = 'insert into grades (g_name, grade, total, weight, g_date, enrolled_id) values (%s, %s, %s, %s, %s, %s) returning grade_id;'
        cursor.execute(query2, (name, grade, total, weight, date, enrolled_id, ))
        grade_id = cursor.fetchone()
        self.conn.commit()
        return grade_id

    def insert_course(self, name, codification, credits, professor_id):
        cursor = self.conn.cursor()
        query = 'insert into course (name, codification, credits, professor_id) values (%s, %s, %s, %s) returning course_id;'
        cursor.execute(query, (name, codification, credits, professor_id, ))
        course_id = cursor.fetchone()
        self.conn.commit()
        return course_id

    def insert_section(self, section_num, course_id):
        cursor = self.conn.cursor()
        query = 'insert into section (section_num, course_id) values (%s, %s) returning section_id;'
        cursor.execute(query, (section_num, course_id,))
        section_id = cursor.fetchone()
        self.conn.commit()
        return section_id

    def add_course_to_student(self, section_id, user_id):
        cursor = self.conn.cursor()
        query = 'insert into enrolled (student_id, section_id) values (%s, %s) returning enrolled_id;'
        cursor.execute(query, (user_id, section_id,))
        enrolled_id = cursor.fetchone()
        self.conn.commit()
        return enrolled_id