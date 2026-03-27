"""
PDF Utility Module
Provides reusable functions for generating hospital bills in PDF format.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def create_bill_pdf(
    bill_id,
    date,
    time,
    patient_name,
    doctor_name,
    admin_name,
    test_names,
    test_costs,
    visit_charge,
    total_test_cost,
    total_cost,
    bill_type="opd",
    room_type=None,
    room_cost=None,
    payment_status=None,
):
    """
    Create a hospital bill PDF (OPD or Hospital/Inpatient).

    Args:
        bill_id (str): Unique bill identifier
        date (str): Bill date
        time (str): Bill time
        patient_name (str): Patient's full name
        doctor_name (str): Doctor's name
        admin_name (str): Admin staff name
        test_names (list): List of test names
        test_costs (dict): Dictionary mapping test names to costs
        visit_charge (float): Doctor's visitation charge
        total_test_cost (float): Total cost of all tests
        total_cost (float): Total bill amount
        bill_type (str): Type of bill - 'opd' or 'hospital' (default: 'opd')
        room_type (str, optional): Type of room (Single/Double/Suite) - for hospital bills
        room_cost (float, optional): Cost of the room - for hospital bills
        payment_status (str, optional): Payment status (Paid/Pending/etc.) - for hospital bills

    Returns:
        str: Path to the generated PDF file
    """
    # Determine bill type and folder
    if bill_type.lower() == "hospital":
        pdf_folder = "bills/hbill"
        bill_title = "Hospital Bill"
    else:
        pdf_folder = "bills/opdbill"
        bill_title = "Hospital OPD Bill"

    # Creating PDF folder
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    pdf_file = f"{pdf_folder}/{bill_id}_bill.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Add background image
    background_image = "background.png"
    if os.path.exists(background_image):
        c.drawImage(ImageReader(background_image), 0, 0, width=600, height=800)

    # Set font and size for the bill
    c.setFont("Helvetica", 12)

    # Write bill details to the PDF
    # Centre align bill title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 780, bill_title)

    # Left-align Date
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Date: {date}")

    # Right-align Time
    c.drawRightString(550, 750, f"Time: {time}")

    # Below Date
    c.drawString(50, 730, f"Patient Name: {patient_name}")

    # Below Time
    c.drawRightString(550, 730, f"Doctor Name: {doctor_name}")

    # Below Patient ID
    c.drawString(50, 710, f"Bill ID: {bill_id}")

    # Below Doctor ID
    c.drawRightString(550, 710, f"Admin Name: {admin_name}")

    # Current Y position for dynamic content
    current_y = 680

    # Add room information for hospital bills
    if bill_type.lower() == "hospital" and room_type and room_cost is not None:
        c.drawString(50, current_y, f"Room Type: {room_type}")
        c.drawRightString(550, current_y, f"Room Cost: {room_cost}")
        current_y -= 20

    # Write test details and costs in a table-like structure
    c.drawString(50, current_y, "Tests")
    c.drawRightString(550, current_y, "Cost")
    current_y -= 20

    for i, testname in enumerate(test_names):
        if bill_type.lower() == "opd":
            c.drawString(50, current_y, f"Test: {testname}")
        else:
            c.drawString(50, current_y, f"{testname}")
        c.drawRightString(550, current_y, f"{test_costs[testname]}")
        current_y -= 20

    # Add some spacing before totals
    current_y -= 20

    # Write total cost
    if bill_type.lower() == "opd":
        c.drawString(50, current_y, f"Visitation Charge: {visit_charge}")
        c.drawRightString(550, current_y, f"Total Test Cost: {total_test_cost}")
        current_y -= 20
        c.drawString(50, current_y, f"Total Cost: {total_cost}")
    else:
        c.drawString(50, current_y, f"Doctor Charge: {visit_charge}")
        c.drawRightString(550, current_y, f"Total Test Cost: {total_test_cost}")
        current_y -= 20
        c.drawRightString(550, current_y, f"Total Cost: {total_cost}")
        if payment_status:
            c.drawString(50, current_y, f"Payment Status: {payment_status}")

    # Save the PDF
    c.save()

    return pdf_file
