import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import mysql.connector as sqltor
import sendmailh

con = sqltor.connect(host="localhost", user="root", passwd="admin", database="hcm")
cursor = con.cursor()

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
    cursor.execute(f"select visitation_charge from doctors where doctor_id = '{doctorid}'")
    data = cursor.fetchall()
    visit_charge = data[0][0]
    
    # Get Room Type and calculate Room Cost
    roomtype = input("Enter the Room Type (Double/Single/Suite): ")
    cursor.execute(f"select Room_Cost from roomexpenses where Room_Type = '{roomtype}'")
    data = cursor.fetchall()
    if not data:
        print("Invalid Room Type. Please enter a valid room type.")
        con.close()
        return
    
    room_cost = data[0][0]
    
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
        testname = input("Enter the name of the test taken (N/A to exit): ")
        if testname.lower() == "n/a":
            break
        else:
            cursor.execute(f"select test_cost from testexpenses where test = '{testname}'")
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
    payment_status = input("Enter the Payment Status (e.g., Paid, Pending, etc.): ")

    cursor.execute(
        f"insert into bill values ('{bid}','{date}',{total_cost},'{payment_status}','{time}','{patientid}','{adminid}','{doctorid}','{roomtype}','{','.join(test_names)}')"
    )
    con.commit()

    # Creating PDF
    pdf_folder = "bills/hbill"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    pdf_file = f"{pdf_folder}/{bid}_bill.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Add background image
    background_image = "background.png"
    c.drawImage(ImageReader(background_image), 0, 0, width=600, height=800)

    # Set font and size for the bill
    c.setFont("Helvetica", 12)

    # Write bill details to the PDF
    # Centre align "Hospital OPD Bill"
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 780, "Hospital Bill")

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
    c.drawString(50, 710, f"Bill ID: {bid}")

    # Below Doctor ID
    c.drawRightString(550, 710, f"Admin Name: {aname}")

    # Write Room Type and Room Cost
    c.drawString(50, 660, f"Room Type: {roomtype}")
    c.drawRightString(550, 660, f"Room Cost: {room_cost}")

    # Write test details and costs in a table-like structure
    c.drawString(50, 640, "Tests")
    c.drawRightString(550, 640, "Cost")

    for i, testname in enumerate(test_names):
        y_position = 620 - i * 20
        c.drawString(50, y_position, f"{testname}")
        c.drawRightString(550, y_position, f"{test_costs[testname]}")

    # Write Payment Status

    # Write total cost
    c.drawString(50, 580, f"Doctor Charge: {visit_charge}")
    c.drawRightString(550, 580, f"Total Test Cost: {amt}")
    # c.drawString(50, 560, f"Total Room Cost: {room_cost}")
    c.drawRightString(550, 560, f"Total Cost: {total_cost}")
    c.drawString(50, 560, f"Payment Status: {payment_status}")

    # Save the PDF
    c.save()
    cursor.execute(f"select email_id from patients where patient_id = '{patientid}'")
    data = cursor.fetchall()
    receive = data[0][0]
    fname = bid + '_bill'
    sendmailh.email(receive, fname)
    con.close()

# Example usage
# hbill('A1')
