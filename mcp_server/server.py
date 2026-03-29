"""
MCP server for HMS — exposes read-only tools for Claude and other MCP clients.
Run from project root: python -m mcp_server.server
Requires: pip install mcp
Column names align with healthcare_management_structure.sql / hcm_database.sql.
"""

from __future__ import annotations

import glob
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# from utility.sql_util import fetch_all, fetch_one
from utility import fetch_all, fetch_one
from utility.mail_util import send_bill_email, send_generic_email

mcp = FastMCP("HMS")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_QUEUE_FILE = _PROJECT_ROOT / "queue" / "queue_data.json"
_PRESCRIPTIONS_DIR = _PROJECT_ROOT / "prescriptions"


@mcp.tool()
def get_patient_summary(patient_id: str) -> dict:
    """Get demographics, medical history and blood group for a patient by patient_id."""
    rows = fetch_all(
        "SELECT First_Name, Middle_Name, Last_Name, date_of_birth, "
        "Gender, Medical_History, Blood_Group, Email_Id, Phone_Number "
        "FROM patients WHERE Patient_ID = %s",
        (patient_id,),
    )
    if not rows:
        return {"error": f"No patient found with ID '{patient_id}'"}
    r = rows[0]
    return {
        "patient_id": patient_id,
        "name": f"{r[0]} {r[1]} {r[2]}".strip(),
        "date_of_birth": str(r[3]) if r[3] is not None else None,
        "gender": r[4],
        "medical_history": r[5],
        "blood_group": r[6],
        "email": r[7],
        "phone": r[8],
    }


@mcp.tool()
def get_doctor_schedule(doctor_id: str) -> list[dict]:
    """Get the weekly schedule for a doctor (day, type of work, time) from doctorschedules."""
    rows = fetch_all(
        "SELECT Day, Type_of_Work, Time FROM doctorschedules WHERE Doctor_ID = %s",
        (doctor_id,),
    )
    if not rows:
        return [{"error": f"No schedule found for doctor '{doctor_id}'"}]
    return [
        {"day": r[0], "type": r[1], "time": str(r[2]) if r[2] is not None else None}
        for r in rows
    ]


@mcp.tool()
def get_appointments(doctor_id: str) -> list[dict]:
    """Get all scheduled appointments for a doctor (Scheduled = 1)."""
    rows = fetch_all(
        "SELECT `Date`, `Time`, Patient_Name, Specialization "
        "FROM appointments WHERE doctor_id = %s AND Scheduled = 1",
        (doctor_id,),
    )
    if not rows:
        return [{"error": f"No appointments found for doctor '{doctor_id}'"}]
    return [
        {
            "date": str(r[0]) if r[0] is not None else None,
            "time": str(r[1]) if r[1] is not None else None,
            "patient": r[2],
            "specialization": r[3],
        }
        for r in rows
    ]


@mcp.tool()
def get_patient_bills(patient_id: str) -> list[dict]:
    """Get all hospital (inpatient) bills for a patient from the bill table."""
    rows = fetch_all(
        "SELECT Bill_Id, `Date`, total_amount, Payment_Status, Room_Type, Tests_Done "
        "FROM bill WHERE patient_id = %s",
        (patient_id,),
    )
    if not rows:
        return [{"error": f"No bills found for patient '{patient_id}'"}]
    return [
        {
            "bill_id": r[0],
            "date": str(r[1]) if r[1] is not None else None,
            "total_amount": float(r[2]) if r[2] is not None else None,
            "payment_status": r[3],
            "room_type": r[4],
            "tests_done": r[5],
        }
        for r in rows
    ]


@mcp.tool()
def get_queue_status(doctor_id: str) -> dict:
    """Get the current patient queue for a doctor from queue/queue_data.json."""
    if not _QUEUE_FILE.is_file():
        return {
            "error": "Queue file queue/queue_data.json not found",
            "doctor_id": doctor_id,
            "queue_length": 0,
            "patients": [],
        }
    with open(_QUEUE_FILE, encoding="utf-8") as f:
        data = json.load(f)
    queue = data.get(doctor_id, [])
    return {"doctor_id": doctor_id, "queue_length": len(queue), "patients": queue}


@mcp.tool()
def get_patient_prescriptions(patient_id: str) -> list[dict]:
    """Get all prescription records for a patient from the prescription table."""
    rows = fetch_all(
        "SELECT Prescription_ID, `Date`, Medications, Instructions, Dosage, "
        "Doctor_ID, Patient_ID, Appointment_ID "
        "FROM prescription WHERE Patient_ID = %s ORDER BY `Date` DESC",
        (patient_id,),
    )
    if not rows:
        return [{"error": f"No prescription records found for patient '{patient_id}'"}]
    return [
        {
            "prescription_id": r[0],
            "date": str(r[1]) if r[1] is not None else None,
            "medications": r[2],
            "instructions": r[3],
            "dosage": r[4],
            "doctor_id": r[5],
            "patient_id": r[6],
            "appointment_id": r[7],
        }
        for r in rows
    ]


@mcp.tool()
def get_patient_opd_bills(patient_id: str) -> list[dict]:
    """Get all OPD bills for a patient from the opdbill table."""
    rows = fetch_all(
        "SELECT OPD_Bill_ID, `Date`, `Time`, Patient_ID, Doctor_ID, Admin_ID, total_amount "
        "FROM opdbill WHERE Patient_ID = %s ORDER BY `Date` DESC, `Time` DESC",
        (patient_id,),
    )
    if not rows:
        return [{"error": f"No OPD bills found for patient '{patient_id}'"}]
    return [
        {
            "opd_bill_id": r[0],
            "date": str(r[1]) if r[1] is not None else None,
            "time": str(r[2]) if r[2] is not None else None,
            "patient_id": r[3],
            "doctor_id": r[4],
            "admin_id": r[5],
            "total_amount": float(r[6]) if r[6] is not None else None,
        }
        for r in rows
    ]


@mcp.tool()
def get_doctor_info(doctor_id: str) -> dict:
    """Get full doctor profile including specialization, department, visitation charge, and experience."""
    row = fetch_one(
        "SELECT Doctor_Id, Doctor_Name, Date_Of_Birth, Gender, Specialization, "
        "Department, Email_Id, Mobile_Number, Visitation_Charge, Experience "
        "FROM doctors WHERE Doctor_Id = %s",
        (doctor_id,),
    )
    if not row:
        return {"error": f"No doctor found with ID '{doctor_id}'"}
    return {
        "doctor_id": row[0],
        "doctor_name": row[1],
        "date_of_birth": str(row[2]) if row[2] is not None else None,
        "gender": row[3],
        "specialization": row[4],
        "department": row[5],
        "email_id": row[6],
        "mobile_number": row[7],
        "visitation_charge": float(row[8]) if row[8] is not None else None,
        "experience": row[9],
    }


@mcp.tool()
def get_all_doctors() -> list[dict]:
    """List all doctors with id, name, specialization, and department."""
    rows = fetch_all(
        "SELECT Doctor_Id, Doctor_Name, Specialization, Department FROM doctors ORDER BY Doctor_Id"
    )
    if not rows:
        return [{"error": "No doctors found in the database"}]
    return [
        {"doctor_id": r[0], "doctor_name": r[1], "specialization": r[2], "department": r[3]}
        for r in rows
    ]


@mcp.tool()
def get_all_patients() -> list[dict]:
    """List all patients with id, full name, blood group, and medical history."""
    rows = fetch_all(
        "SELECT Patient_ID, First_Name, Middle_Name, Last_Name, Blood_Group, Medical_History "
        "FROM patients ORDER BY Patient_ID"
    )
    if not rows:
        return [{"error": "No patients found in the database"}]
    return [
        {
            "patient_id": r[0],
            "name": f"{r[1]} {r[2]} {r[3]}".strip(),
            "blood_group": r[4],
            "medical_history": r[5],
        }
        for r in rows
    ]


@mcp.tool()
def get_patient_insurance(patient_id: str) -> dict:
    """Get insurance details by joining patients with insuranceinformation on Insurance_Id."""
    row = fetch_one(
        "SELECT p.Patient_ID, p.Insurance_Id, i.Company_Name, i.Coverage_Amount, "
        "i.Policy_Number, i.Patient_ID AS info_patient_id "
        "FROM patients p "
        "LEFT JOIN insuranceinformation i ON p.Insurance_Id = i.Insurance_Id "
        "WHERE p.Patient_ID = %s",
        (patient_id,),
    )
    if not row:
        return {"error": f"No patient found with ID '{patient_id}'"}
    return {
        "patient_id": row[0],
        "insurance_id": row[1],
        "company_name": row[2],
        "coverage_amount": float(row[3]) if row[3] is not None else None,
        "policy_number": row[4],
        "insurance_table_patient_id": row[5],
    }


@mcp.tool()
def get_prescription_files(patient_id: str) -> list[dict]:
    """Read plain-text prescription files from prescriptions/ ({patient_id}_{YYYY-MM-DD}.txt)."""
    if not _PRESCRIPTIONS_DIR.is_dir():
        return [{"error": f"Prescriptions directory not found at '{_PRESCRIPTIONS_DIR}'"}]
    pattern = str(_PRESCRIPTIONS_DIR / f"{patient_id}_*.txt")
    paths = sorted(glob.glob(pattern))
    if not paths:
        return [{"error": f"No prescription text files found for patient '{patient_id}'"}]
    out: list[dict] = []
    for path in paths:
        fname = os.path.basename(path)
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        stem = fname[:-4] if fname.lower().endswith(".txt") else fname
        parts = stem.split("_", 1)
        file_date = parts[1] if len(parts) == 2 else None
        out.append(
            {
                "filename": fname,
                "file_date": file_date,
                "content": content,
            }
        )
    return out


@mcp.tool()
def get_test_costs() -> list[dict]:
    """Return all diagnostic tests and their costs from testexpenses."""
    rows = fetch_all("SELECT test, test_cost FROM testexpenses ORDER BY test")
    if not rows:
        return [{"error": "No test pricing rows found in testexpenses"}]
    return [{"test": r[0], "test_cost": float(r[1]) if r[1] is not None else None} for r in rows]


@mcp.tool()
def get_room_costs() -> list[dict]:
    """Return all room types and costs from roomexpenses."""
    rows = fetch_all(
        "SELECT Room_Type, Room_Cost FROM roomexpenses ORDER BY Room_Type"
    )
    if not rows:
        return [{"error": "No room pricing rows found in roomexpenses"}]
    return [
        {"room_type": r[0], "room_cost": float(r[1]) if r[1] is not None else None}
        for r in rows
    ]


@mcp.tool()
def search_appointments_by_date(date: str) -> list[dict]:
    """Get all appointments on a specific date (YYYY-MM-DD) across all doctors."""
    rows = fetch_all(
        "SELECT Appointment_Id, `Date`, `Time`, Patient_Name, Patient_ID, doctor_id, "
        "Specialization, Department "
        "FROM appointments WHERE `Date` = %s ORDER BY `Time`, doctor_id",
        (date,),
    )
    if not rows:
        return [{"error": f"No appointments found on date '{date}'"}]
    return [
        {
            "appointment_id": r[0],
            "date": str(r[1]) if r[1] is not None else None,
            "time": str(r[2]) if r[2] is not None else None,
            "patient_name": r[3],
            "patient_id": r[4],
            "doctor_id": r[5],
            "specialization": r[6],
            "department": r[7],
        }
        for r in rows
    ]


@mcp.tool()
def get_admin_info(admin_id: str) -> dict:
    """Get full administrative staff profile from administrativestaff."""
    row = fetch_one(
        "SELECT Admin_Id, First_Name, Middle_Name, Last_Name, Position, Email_Id, Phone_Number "
        "FROM administrativestaff WHERE Admin_Id = %s",
        (admin_id,),
    )
    if not row:
        return {"error": f"No administrative staff found with ID '{admin_id}'"}
    return {
        "admin_id": row[0],
        "name": f"{row[1]} {row[2]} {row[3]}".strip(),
        "first_name": row[1],
        "middle_name": row[2],
        "last_name": row[3],
        "position": row[4],
        "email_id": row[5],
        "phone_number": row[6],
    }


@mcp.tool()
def send_hospital_bill_email(receiver_email: str, bill_id: str) -> dict:
    """
    Send a hospital (inpatient) bill PDF via email to a patient.
    The bill PDF must exist in bills/hbill/ folder with filename {bill_id}_bill.pdf.
    
    Args:
        receiver_email: Patient's email address
        bill_id: Hospital bill ID (e.g., 'B1', 'B2')
    
    Returns:
        Status dict with 'success' (bool) and 'message' (str)
    
    Example:
        send_hospital_bill_email('patient@example.com', 'B1')
    """
    result = send_bill_email(receiver_email, f"{bill_id}_bill", "hospital")
    return result


@mcp.tool()
def send_opd_bill_email(receiver_email: str, opd_bill_id: str) -> dict:
    """
    Send an OPD bill PDF via email to a patient.
    The bill PDF must exist in bills/opdbill/ folder with filename {opd_bill_id}_bill.pdf.
    
    Args:
        receiver_email: Patient's email address
        opd_bill_id: OPD bill ID (e.g., 'O1', 'O2')
    
    Returns:
        Status dict with 'success' (bool) and 'message' (str)
    
    Example:
        send_opd_bill_email('patient@example.com', 'O1')
    """
    result = send_bill_email(receiver_email, f"{opd_bill_id}_bill", "opd")
    return result


@mcp.tool()
def send_email(receiver_email: str, subject: str, body: str, attachment_path: str = None) -> dict:
    """
    Send a generic email with optional file attachment.
    Use this for appointment reminders, notifications, reports, or any informational emails.
    
    Args:
        receiver_email: Recipient's email address
        subject: Email subject line
        body: Email body text (plain text)
        attachment_path: Optional path to file to attach (e.g., 'reports/report.pdf')
    
    Returns:
        Status dict with 'success' (bool) and 'message' (str)
    
    Examples:
        send_email('patient@example.com', 'Appointment Reminder', 'Your appointment is tomorrow at 10 AM.')
        send_email('doctor@example.com', 'Lab Report', 'Please find the lab report attached.', 'reports/lab_report.pdf')
    """
    result = send_generic_email(receiver_email, subject, body, attachment_path)
    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")
