from RumboEx.config.dbconfig import pg_config
import psycopg2


class ProgramDAO:
    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    # GET Methods


    def get_faculties(self):
        cursor = self.conn.cursor()
        query = "select * from faculty"
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_programs(self, faculty_num):
        cursor = self.conn.cursor()
        query = "select * from program where faculty_num=%s"
        cursor.execute(query, (faculty_num, ))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result
