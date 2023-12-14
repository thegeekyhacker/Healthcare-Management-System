import mysql.connector as sqltor
import greeting
import schedule
import appointment
import createapp
import newpatient
import opdbill
import bill
from pqueue import *
# from pqueue import add_to_queue, display_schedule, shared_queue 
con = sqltor.connect(host="localhost",user="root",passwd = "admin",database = "hcm")
cursor = con.cursor()
def admin(userid):
    cursor.execute(f"Select first_name,middle_name,last_name from administrativestaff where admin_id = '{userid}'")
    result = cursor.fetchall()
    first_name = result[0][0]
    middle_name = result[0][1]
    last_name = result[0][2]
    aname = first_name + ' ' + middle_name + ' ' + last_name;
    # print(aname)
    greet = greeting.greeting()
    greet = greet  + ' ' + aname
    print(greet)
    while True:
        # print(greet)
        print("1. Check Doctors Schedule(schedule)\n")
        print("2. Check Appointments (appointments)\n")
        print("3. Create Appointment(creatapp)\n")
        print("4. New Patient Registration(reg)\n")
        print("5. OPD Bill(opdB)\n")
        print("6. Hospital Bill(hbill)\n")
        print("7. Add to queue(add)\n")
        print("8. View queue(view)\n")
        print("9. Logout\n")
        ans = input("Enter the action you want to perform : ")
        if ans.lower() == 'schedule':
            doctor_id = input("Enter the Doctor Id : ")
            schedule.schedule(doctor_id)
        elif ans.lower() == 'appointments':
            doctor_id = input("Enter the Doctor Id : ")
            appointment.appointment(doctor_id)
        elif ans.lower() == 'createapp':
            createapp.createapp()
        elif ans.lower() == 'reg':
            newpatient.newpatient()
        elif ans.lower() == 'opdB':
            opdbill.opdbill(userid)
        elif ans.lower() == 'hbill': 
            bill.hbill(userid)
        elif ans.lower() == 'add':
            doctorid = input("Enter Doctor Id : ")
            patientid = input("Enter patient Id : ")
            add_to_queue(doctorid,patientid)
            # h.display_schedule("D1")
        elif ans.lower() == 'view':
            docid = input("Enter the Doctor Id : ")
            display_schedule(docid)
        elif ans.lower() == 'logout':
            print("Have a nice day ahead!")
            break
        else:
            print("Kindly enter a valid choice")

admin('A1')