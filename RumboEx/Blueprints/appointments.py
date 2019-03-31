from flask import Blueprint, request
from RumboEx import rbac
from RumboEx.handler.AppointmentHandler import AppointmentHandler

appointments = Blueprint('appointments', __name__)


#insert appointment
@appointments.route('/insert_appointment_form',methods = ['POST'])
@rbac.exempt
def insertAppointment():
    if request.method == 'POST':
        appointment_info = request.get_json()
        print(appointment_info)
        counter = 0
        reasons = appointment_info["reasons"]
        date = appointment_info["date"]
        comment1 = appointment_info["comment1"]
        student_num = appointment_info["student_num"]
        mentor_id = appointment_info["mentor_id"]
        a_id = AppointmentHandler().insertAppointment(reasons, comment1, student_num, mentor_id)
        for reason in appointment_info["reasons"]:
            AppointmentHandler().insertINtoReason(appointment_info["reasons"][counter])
            AppointmentHandler().insertiIntoReasonsToAppointment()
            counter = counter +1
        return "good"


#get all appointments
@appointments.route('/appointments', methods = ['GET'])
#@rbac.allow(['student'],['GET'],with_children=False)
def getAllAppointments():
    if request.method =='GET':
        return AppointmentHandler().getAllAppointments();

@appointments.route('/appointments/<int:reason_id>', methods = ['GET'])
#@rbac.allow(['psychologyst', 'admin','counselor','mentor'],['GET'],with_children=False)
def getAppointmentsByReason(reason_id):
    if request.method == 'GET':
        return AppointmentHandler().getAppointmentsByReason(reason_id)

