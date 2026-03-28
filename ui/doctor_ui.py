import webbrowser

from utility.greeting import greeting

from services import appointment_service, doctor_service, patient_service, queue_service
from utility import text_to_speech


def doctor(userid):
    dname = doctor_service.get_doctor_display_name(userid) or ""
    greet = greeting()
    greet = greet + ' ' + dname
    print(greet)
    while True:
        print("1. Check your schedule(schedule)\n")
        print("2. Check your appointments(appointments)\n")
        print("3. Check patient details(details)\n")
        print("4. Prescribe medicines(prescribe)\n")
        print("5. Call next patient(call)\n")
        print("6. Video call patient(video)\n")
        print("7. Logout\n")
        ans = input("Enter the action you want to perform : ")
        if ans.lower() == 'schedule':
            doctor_service.schedule(userid)
        elif ans.lower() == 'appointments':
            appointment_service.appointment(userid)
        elif ans.lower() == 'details':
            patientid = input("Enter the Patient Id : ")
            patient_service.details(patientid)
        elif ans.lower() == 'prescribe':
            patientid = input("Enter the Patient Id : ")
            appointmentid = input("Enter the Appointment Id : ")
            doctor_service.prescribe(userid, patientid, appointmentid)
        elif ans.lower() == 'view':
            doctorid = input("Enter the doctor id : ")
            queue_service.display_schedule(doctorid)
        elif ans.lower() == 'call':
            removed_patient = queue_service.remove_from_queue("D1")
            if removed_patient:
                print(f"Patient {removed_patient} please come in.")
                text_to_speech(
                    f"Patient {removed_patient} please come in.")
            else:
                print("No patients in the queue for this doctor.")
        elif ans.lower() == 'video':
            patientid = input("Enter the Patient Id : ")
            phone_number = patient_service.get_patient_phone(patientid)
            if phone_number is None:
                print("Patient not found.")
                continue
            phone_number = phone_number.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            if not phone_number.startswith("+"):
                phone_number = "+" + phone_number
            telegram_url = f"https://t.me/{phone_number}"
            print(f"Opening Telegram for patient {patientid} at {phone_number}...")
            webbrowser.open(telegram_url)
        elif ans.lower() == 'logout':
            print("Have a nice day ahead!")
            break
        else:
            print("Kindly enter a valid choice")
