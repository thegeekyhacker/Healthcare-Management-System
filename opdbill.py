import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import mysql.connector as sqltor
import sendmail

con = sqltor.connect(host="localhost", user="root", passwd="admin", database="hcm")
cursor = con.cursor()


def opdbill(adminid):
    cursor.execute("select * from opdbill")
    data = cursor.fetchall()
    oid = 'O' + str(len(data) + 1)
    doctorid = input("Enter the Doctor Id : ")
    patientid = input("Enter the Patient Id : ")
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute(f"select visitation_charge from doctors where doctor_id = '{doctorid}'")
    data = cursor.fetchall()
    visit_charge = data[0][0]
    amt = 0
    test_names = []
    test_costs = {}
    cursor.execute(f"select doctor_name from doctors where doctor_id = '{doctorid}'")
    data = cursor.fetchall()
    dname = data[0][0]
    cursor.execute(f"select first_name,middle_name,last_name from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()
    pname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]
    cursor.execute(f"select first_name,middle_name,last_name from administrativestaff where admin_id = '{adminid}'")
    data = cursor.fetchall()
    aname = data[0][0] + ' ' + data[0][1] + ' ' + data[0][2]

    while True:
        testname = input("Enter the name of the test taken (N/A to exit) : ")
        if testname.lower() == "n/a":
            break
        else:
            cursor.execute(f"select test_cost from testexpenses where test = '{testname}'")
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

    # Creating PDF
    pdf_folder = "bills/opdbill"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    pdf_file = f"{pdf_folder}/{oid}_bill.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Add background image
    background_image = "background.png"
    c.drawImage(ImageReader(background_image), 0, 0, width=600, height=800)

    # Set font and size for the bill
    c.setFont("Helvetica", 12)

    # Write bill details to the PDF
    # Centre align "Hospital OPD Bill"
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 780, "Hospital OPD Bill")

    # Left-align Date
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Date: {date}")

    # Right-align Time
    c.drawRightString(550, 750, f"Time: {time}")

    # Below Date
    c.drawString(50, 730, f"Patient Name: {pname}")

    # Below Time
    c.drawRightString(550, 730, f"Doctor Name: {dname}")

    # Below Patient ID
    c.drawString(50, 710, f"Bill ID: {oid}")

    # Below Doctor ID
    c.drawRightString(550, 710, f"Admin Name: {aname}")

    # Write test details and costs in a table-like structure
    c.drawString(50, 680, "Tests")
    c.drawRightString(550, 680, "Cost")

    for i, testname in enumerate(test_names):
        y_position = 660 - i * 20
        c.drawString(50, y_position, f"Test: {testname}")
        c.drawRightString(550, y_position, f"Cost: {test_costs[testname]}")

    # Write total cost
    c.drawString(50, 600, f"Visitation Charge: {visit_charge}")
    c.drawRightString(550, 600, f"Total Test Cost: {amt}")
    c.drawString(50, 580, f"Total Cost: {total_cost}")

    # Save the PDF
    c.save()
    cursor.execute(f"select email_id from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()
    receive = data[0][0]
    fname = oid + '_bill'
    sendmail.email(receive,fname)
    con.close()


# Example usage
# opdbill('A1')
