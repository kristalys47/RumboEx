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
        query = "select * from course natural inner join student_courses where student_courses.user_id = %s;"
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_course_by_course_id(self, course_id):
        cursor = self.conn.cursor()
        query = "select * from course where codification = %s;"
        cursor.execute(query, (course_id,))
        result = cursor.fetchone()
        if not result:
            return None
        return result
