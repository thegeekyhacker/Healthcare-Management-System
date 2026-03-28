from datetime import datetime
from utility.sql_util import (
    fetch_all,
    execute_query,
    commit_transaction,
    close_db_connection,
)
from utility import create_bill_pdf, send_bill_email


def opdbill(adminid):
    data = fetch_all("select * from opdbill")
    oid = 'O' + str(len(data) + 1)
    doctorid = input("Enter the Doctor Id : ")
    patientid = input("Enter the Patient Id : ")
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    data = fetch_all(
        f"select visitation_charge from doctors where doctor_id = '{doctorid}'")
    visit_charge = data[0][0]
    amt = 0
    test_names = []
    test_costs = {}
    data = fetch_all(
        f"select doctor_name from doctors where doctor_id = '{doctorid}'")
    dname = data[0][0]
    data = fetch_all(
        f"select first_name,middle_name,last_name from patients where patient_id = '{patientid}'")
    pname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]
    data = fetch_all(
        f"select first_name,middle_name,last_name from administrativestaff where admin_id = '{adminid}'")
    aname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]

    while True:
        testname = input("Enter the name of the test taken (N/A to exit) : ")
        if testname.lower() == "n/a":
            break
        else:
            data = fetch_all(
                f"select test_cost from testexpenses where test = '{testname}'")
            if len(data) == 0:
                print("No such test exists.")
                print("Kindly enter a valid test name")
                continue
            amt += data[0][0]
            test_names.append(testname)
            test_costs[testname] = data[0][0]

    total_cost = visit_charge + amt
    execute_query(
        f"insert into opdbill values ('{date}','{time}','{patientid}','{doctorid}','{oid}','{adminid}',{total_cost})")
    commit_transaction()

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
    data = fetch_all(
        f"select email_id from patients where patient_id = '{patientid}'")
    receive = data[0][0]
    fname = oid + '_bill'
    send_bill_email(receive, fname, 'opd')
    close_db_connection()


# Example usage
# opdbill('A1')  To test only this file/feature
