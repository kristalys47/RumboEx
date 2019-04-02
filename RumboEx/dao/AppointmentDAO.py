from RumboEx.config.dbconfig import pg_config
import psycopg2

r_id_general =0
a_id_general=0
class AppointmentDAO:

    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    #POST an appointment
    def insert_appointment(self,reasons, comment1,student_num,mentor_id,):
        cursor = self.conn.cursor()
        for current2 in reasons:
            print (current2)
        query = "insert into appointment_form (a_reasons, a_date, a_comment, student_num, mentor_id) " \
                "values(%s,'now',%s,%s,%s) returning appointment_id;"
        cursor.execute(query,(reasons,comment1,student_num,mentor_id))
        appointment_id = cursor.fetchone()[0]
        print(appointment_id)
        global a_id_general
        a_id_general = appointment_id
        self.conn.commit()
        return appointment_id

    #insert into reasons table
    def insertIntoReason(self,reason):
        cursor = self.conn.cursor()
        #print("reasons inside DAO:")
        #print(reason)
        query = "insert into reasons(reason) values (%s) returning r_id;"
        cursor.execute(query,[reason])
        r_id = cursor.fetchone()[0]
        global r_id_general
        r_id_general= r_id
        self.conn.commit()
        print("inside DAO insert reason")
        print(r_id)
        return r_id

    #insert into reasons_to_appointment
    def insertiIntoReasonsToAppointment(self):
        cursor = self.conn.cursor()
        print(r_id_general,a_id_general)
        query = "insert into reasons_to_appointment(r_id,appointment_id)  values (%s,%s)"
        cursor.execute(query,(r_id_general,a_id_general))
        return "inserted into reason_to_appointment"

    #GET all appointments in the system
    def getAllAppointments(self):
        cursor = self.conn.cursor()
        query = "select * from appointment_form;"
        cursor.execute(query)
        appointments =[]
        for appointment in cursor:
            appointments.append(appointment)
        return appointments

    #GET appointments of a specific mentor
    def getAppointmentByMentor(self, mentor_id):
        cursor = self.conn.cursor()
        query = "select * from appointment_form where mentor_id = %s"
        cursor.execute(query)
        allAppointments = []
        for current in cursor:
            allAppointments.append(current)
        return allAppointments

    #Get all appointments by a specific reason
    def getAppoinmentByReason(self,reason):
        cursor = self.conn.cursor()
        query = "select * from appointment_form " \
                "where appointment_id = " \
                "(select appointment_id " \
                "from reasons_to_appointment natural inner join reasons " \
                "where r_id = %s ); "
        cursor.execute(query)
        result = []
        for current in cursor:
            result.append(current)
        return result
