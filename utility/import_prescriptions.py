"""
Script to import existing prescription text files into the database.
Parses prescription files from the prescriptions/ folder and inserts them into the prescription table.
"""

import os
import re
from utility.sql_util import execute_query, commit_transaction, fetch_all


def parse_prescription_file(filepath):
    """Parse a prescription text file and extract data."""
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Extract metadata using regex
    date_match = re.search(r'Prescription Date: (.+)', content)
    doctor_match = re.search(r'Doctor ID: (.+)', content)
    patient_match = re.search(r'Patient ID: (.+)', content)
    appointment_match = re.search(r'Appointment ID: (.+)', content)
    
    date = date_match.group(1).strip() if date_match else None
    doctor_id = doctor_match.group(1).strip() if doctor_match else None
    patient_id = patient_match.group(1).strip() if patient_match else None
    appointment_id = appointment_match.group(1).strip() if appointment_match else None
    
    # Extract prescription details
    prescription_section = content.split('Prescription:')[1] if 'Prescription:' in content else ''
    
    medications = []
    instructions = []
    dosages = []
    
    # Parse medicine entries
    lines = prescription_section.strip().split('\n')
    current_medicine = None
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('Instruction'):
            # This is a medicine name (ends with :)
            if line.endswith(':'):
                current_medicine = line[:-1].strip()
                if current_medicine:  # Only add non-empty medicines
                    medications.append(current_medicine)
        elif line.startswith('Instruction') and current_medicine:
            # Parse instruction line
            # Format: "Instruction Before meal Eat During Lunch"
            parts = line.replace('Instruction ', '').split(' Eat During ')
            if len(parts) == 2:
                instruction = parts[0].strip()
                timing = parts[1].strip()
                instructions.append(f"{current_medicine}: {instruction} - {timing}")
                dosages.append(f"{current_medicine}: {instruction}")
    
    return {
        'date': date,
        'doctor_id': doctor_id,
        'patient_id': patient_id,
        'appointment_id': appointment_id,
        'medications': ', '.join(medications),
        'instructions': '; '.join(instructions),
        'dosage': '; '.join(dosages)
    }


def get_next_prescription_id():
    """Get the next prescription ID in the PS1, PS2, PS3... format."""
    last_id_query = "SELECT Prescription_ID FROM prescription ORDER BY Prescription_ID DESC LIMIT 1"
    last_id_result = fetch_all(last_id_query)
    
    if last_id_result and last_id_result[0][0]:
        last_id = last_id_result[0][0]
        last_num = int(last_id.replace('PS', ''))
        return f"PS{last_num + 1}"
    else:
        return "PS1"


def import_prescriptions():
    """Import all prescription files from the prescriptions/ folder."""
    prescriptions_folder = 'prescriptions'
    
    if not os.path.exists(prescriptions_folder):
        print(f"Folder '{prescriptions_folder}' not found.")
        return
    
    # Get all .txt files
    files = [f for f in os.listdir(prescriptions_folder) if f.endswith('.txt')]
    
    if not files:
        print("No prescription files found.")
        return
    
    print(f"Found {len(files)} prescription file(s) to import.\n")
    
    imported_count = 0
    skipped_count = 0
    
    for filename in files:
        filepath = os.path.join(prescriptions_folder, filename)
        print(f"Processing: {filename}")
        
        try:
            data = parse_prescription_file(filepath)
            
            # Skip if essential data is missing
            if not data['date'] or not data['doctor_id'] or not data['patient_id']:
                print(f"  ⚠ Skipped: Missing essential data")
                skipped_count += 1
                continue
            
            # Check if this prescription already exists (by date, patient, doctor)
            check_query = """
                SELECT Prescription_ID FROM prescription 
                WHERE Date = %s AND Patient_ID = %s AND Doctor_ID = %s
            """
            existing = fetch_all(check_query, (data['date'], data['patient_id'], data['doctor_id']))
            
            if existing:
                print(f"  ⚠ Skipped: Already exists in database")
                skipped_count += 1
                continue
            
            # Get next prescription ID
            prescription_id = get_next_prescription_id()
            
            # Truncate data to fit database column limits
            medications = data['medications'][:100] if len(data['medications']) > 100 else data['medications']
            instructions = data['instructions'][:100] if len(data['instructions']) > 100 else data['instructions']
            dosage = data['dosage'][:20] if len(data['dosage']) > 20 else data['dosage']
            
            # Insert into database
            insert_query = """
                INSERT INTO prescription
                (Prescription_ID, Date, Medications, Instructions, Dosage, Doctor_ID, Patient_ID, Appointment_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            execute_query(insert_query, (
                prescription_id,
                data['date'],
                medications,
                instructions,
                dosage,
                data['doctor_id'],
                data['patient_id'],
                data['appointment_id']
            ))
            
            commit_transaction()
            print(f"  ✓ Imported as {prescription_id}")
            imported_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            skipped_count += 1
    
    print(f"\n{'='*50}")
    print(f"Import complete!")
    print(f"Imported: {imported_count}")
    print(f"Skipped: {skipped_count}")
    print(f"{'='*50}")


if __name__ == "__main__":
    import_prescriptions()

# Made with Bob
