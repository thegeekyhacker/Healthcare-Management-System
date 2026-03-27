from datetime import datetime
from connector import get_db_connection
from utility import create_bill_pdf, send_bill_email

con, cursor = get_db_connection()


def opdbill(adminid):
    cursor.execute("select * from opdbill")
    data = cursor.fetchall()
    oid = 'O' + str(len(data) + 1)
    doctorid = input("Enter the Doctor Id : ")
    patientid = input("Enter the Patient Id : ")
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute(
        f"select visitation_charge from doctors where doctor_id = '{doctorid}'")
    data = cursor.fetchall()
    visit_charge = data[0][0]
    amt = 0
    test_names = []
    test_costs = {}
    cursor.execute(
        f"select doctor_name from doctors where doctor_id = '{doctorid}'")
    data = cursor.fetchall()
    dname = data[0][0]
    cursor.execute(
        f"select first_name,middle_name,last_name from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()
    pname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]
    cursor.execute(
        f"select first_name,middle_name,last_name from administrativestaff where admin_id = '{adminid}'")
    data = cursor.fetchall()
    aname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]

    while True:
        testname = input("Enter the name of the test taken (N/A to exit) : ")
        if testname.lower() == "n/a":
            break
        else:
            cursor.execute(
                f"select test_cost from testexpenses where test = '{testname}'")
            data = cursor.fetchall()
            if len(data) == 0:
                print("No such test exists.")
                print("Kindly enter a valid test name")
                continue
            amt += data[0][0]
            test_names.append(testname)
            test_costs[testname] = data[0][0]

    total_cost = visit_charge + amt
    cursor.execute(
        f"insert into opdbill values ('{date}','{time}','{patientid}','{doctorid}','{oid}','{adminid}',{total_cost})")
    con.commit()

    # Create PDF using utility function
    pdf_file = create_bill_pdf(
        bill_id=oid,
        date=date,
        time=time,
        patient_name=pname,
        doctor_name=dname,
        admin_name=aname,
        test_names=test_names,
        test_costs=test_costs,
        visit_charge=visit_charge,
        total_test_cost=amt,
        total_cost=total_cost,
        bill_type='opd'
    )
    cursor.execute(
        f"select email_id from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()
    receive = data[0][0]
    fname = oid + '_bill'
    send_bill_email(receive, fname, 'opd')
    con.close()


# Example usage
# opdbill('A1')  To test only this file/feature
