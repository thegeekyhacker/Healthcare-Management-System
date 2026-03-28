from utility.greeting import greeting

from services import (
    appointment_service,
    auth_service,
    billing_service,
    doctor_service,
    patient_service,
    queue_service,
)


def admin(userid):
    aname = auth_service.get_admin_display_name(userid) or ""
    greet = greeting()
    greet = greet + " " + aname
    print(greet)
    while True:
        print("1. Check Doctors Schedule(schedule)\n")
        print("2. Check Appointments (appointments)\n")
        print("3. Create Appointment(creatapp)\n")
        print("4. New Patient Registration(reg)\n")
        print("5. OPD Bill(opdbill)\n")
        print("6. Hospital Bill(hbill)\n")
        print("7. Add to queue(add)\n")
        print("8. View queue(view)\n")
        print("9. Logout\n")
        ans = input("Enter the action you want to perform : ")
        if ans.lower() == "schedule":
            doctor_id = input("Enter the Doctor Id : ")
            doctor_service.schedule(doctor_id)
        elif ans.lower() == "appointments":
            doctor_id = input("Enter the Doctor Id : ")
            appointment_service.appointment(doctor_id)
        elif ans.lower() == "createapp":
            appointment_service.createapp()
        elif ans.lower() == "reg":
            patient_service.newpatient()
        elif ans.lower() == "opdbill":
            billing_service.opdbill(userid)
        elif ans.lower() == "hbill":
            billing_service.hbill(userid)
        elif ans.lower() == "add":
            doctorid = input("Enter Doctor Id : ")
            patientid = input("Enter patient Id : ")
            queue_service.add_to_queue(doctorid, patientid)
        elif ans.lower() == "view":
            docid = input("Enter the Doctor Id : ")
            queue_service.display_schedule(docid)
        elif ans.lower() == "logout":
            print("Have a nice day ahead!")
            break
        else:
            print("Kindly enter a valid choice")
