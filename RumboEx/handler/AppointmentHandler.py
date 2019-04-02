from flask import jsonify
from RumboEx.dao.AppointmentDAO import AppointmentDAO

dao = AppointmentDAO()
class AppointmentHandler:

    def appointmentDic(self,appointment):
        return {'reasons': appointment[0],
                'date': appointment[1],
                'comment1': appointment[2],
                'student_num':appointment[3],
                'mentor_id':appointment[4],
                'confirmation': appointment[5],
                'appointment_id': appointment[6]
                }

    def insertAppointment(self, reasons,comment1,student_num,mentor_id):
        id = dao.insert_appointment(reasons,comment1,student_num,mentor_id)
        return jsonify(result = id),200

    def insertINtoReason(self,reason):
        id = dao.insertIntoReason(reason)
        return jsonify(result = id),200

    def insertiIntoReasonsToAppointment(self):
        id = dao.insertiIntoReasonsToAppointment()
        return jsonify(result = id),200
    def getAllAppointments(self):
        appointments = dao.getAllAppointments()
        result = []
        for appointment in appointments:
            result.append(self.appointmentDic(appointment))
        return jsonify(Appointments = result ),200

    def getAppointmentsByReason(self,r_id):
        appointments = dao.getAppoinmentByReason(r_id)
        result = []
        for current in appointments:
            result.append(current)
        return jsonify(Appointments = result),200