from datetime import datetime
from connector import get_db_connection
from utility import create_bill_pdf, send_bill_email

con, cursor = get_db_connection()


def hbill(adminid):
    cursor.execute("select * from bill")
    data = cursor.fetchall()
    bid = 'B' + str(len(data) + 1)
    doctorid = input("Enter the Doctor Id: ")
    patientid = input("Enter the Patient Id: ")

    # Generate Bill_Id
    # oid = 'B' + str(len(data) + 1)

    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute(
        f"select visitation_charge from doctors where doctor_id = '{doctorid}'")
    data = cursor.fetchall()
    visit_charge = data[0][0]

    # Get Room Type and calculate Room Cost
    roomtype = input("Enter the Room Type (Double/Single/Suite): ")
    cursor.execute(
        f"select Room_Cost from roomexpenses where Room_Type = '{roomtype}'")
    data = cursor.fetchall()
    if not data:
        print("Invalid Room Type. Please enter a valid room type.")
        con.close()
        return

    room_cost = data[0][0]

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
        testname = input("Enter the name of the test taken (N/A to exit): ")
        if testname.lower() == "n/a":
            break
        else:
            cursor.execute(
                f"select test_cost from testexpenses where test = '{testname}'")
            data = cursor.fetchall()
            if not data:
                print("No such test exists.")
                print("Kindly enter a valid test name")
                continue
            amt += data[0][0]
            test_names.append(testname)
            test_costs[testname] = data[0][0]

    total_cost = visit_charge + amt + room_cost

    # Get Payment Status
    payment_status = input(
        "Enter the Payment Status (e.g., Paid, Pending, etc.): ")

    cursor.execute(
        f"insert into bill values ('{bid}','{date}',{total_cost},'{payment_status}','{time}','{patientid}','{adminid}','{doctorid}','{roomtype}','{','.join(test_names)}')"
    )
    con.commit()

    # Create PDF using utility function
    pdf_file = create_bill_pdf(
        bill_id=bid,
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
        bill_type='hospital',
        room_type=roomtype,
        room_cost=room_cost,
        payment_status=payment_status
    )
    cursor.execute(
        f"select email_id from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()
    receive = data[0][0]
    fname = bid + '_bill'
    send_bill_email(receive, fname, 'hospital')
    con.close()

# Example usage
# hbill('A1')  To test only this file/feature