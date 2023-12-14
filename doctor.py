import mysql.connector as sqltor
import greeting
import schedule
import appointment
import prescribe
import details
import voice
from pqueue import *  # Import necessary functions and shared_queue object

# h = HospitalScheduler()
con = sqltor.connect(host="localhost",user="root",passwd = "admin",database = "hcm")
cursor = con.cursor()

def doctor(userid):
    cursor.execute(f"SELECT doctor_name from doctors where doctor_id = '{userid}'")
    result=cursor.fetchall()
    dname = result[0][0]
    # print(dname)
    greet = greeting.greeting()
    greet = greet  + ' ' + dname
    print(greet)
    while True:
        # print(greet)
        print("1. Check your schedule(schedule)\n")
        print("2. Check your appointments(appointments)\n")
        print("3. Check patient details(details)\n")
        print("4. Prescribe medicines(prescribe)\n")
        print("5. Call next patient(call)\n")
        print("6. Logout\n")
        ans = input("Enter the action you want to perform : ")
        if ans.lower() == 'schedule':
            schedule.schedule(userid)
        elif ans.lower() == 'appointments':
            appointment.appointment(userid)
        elif ans.lower() == 'details':
            patientid = input("Enter the Patient Id : ")
            details.details(patientid)
        elif ans.lower() == 'prescribe':
            patientid = input("Enter the Patient Id : ")
            appointmentid = input("Enter the Appointment Id : ")
            prescribe.prescribe(userid,patientid,appointmentid)
        elif ans.lower() == 'view':
            doctorid = input("Enter the doctor id : ")
            display_schedule(doctorid)
        elif ans.lower() == 'call':
            removed_patient = remove_from_queue("D1")
            if removed_patient:
                print(f"Patient {removed_patient} please come in.")
                voice.text_to_speech(f"Patient {removed_patient} please come in.")
            else:
                print("No patients in the queue for this doctor.")
        elif ans.lower() == 'logout':
            print("Have a nice day ahead!")
            break
        else:
            print("Kindly enter a valid choice")

# doctor("D1")