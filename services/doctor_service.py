import datetime
import os

import speech_recognition as sr

from utility.sql_util import fetch_all, execute_query, commit_transaction


def get_doctor_display_name(doctor_id):
    rows = fetch_all(
        f"SELECT doctor_name from doctors where doctor_id = '{doctor_id}'")
    if not rows:
        return None
    return rows[0][0]


def schedule(userid):
    data = fetch_all(
        f"select day,type_of_work,time from doctorschedules where doctor_id = '{userid}'")
    result = fetch_all(
        f"SELECT doctor_name from doctors where doctor_id = '{userid}'")
    for i in data:
        text = f"{result[0][0]} has {i[1]} on {i[0]} from {i[2]}."
        print(text)


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said :- {query}\n")
        return query.lower()
    except Exception as e:
        print(e)
        print("Say that Again please....")
        return "None"


def get_medicines():
    medicines = []
    while True:
        print("Please provide the medicine:")
        medicine = takecommand()
        if medicine.lower() == "stop":
            break
        elif medicine.lower() != "none":
            medicines.append(medicine)

    return medicines


def get_instructions():
    print("Please provide instructions/timings for the medicine (type 'stop' when done):")
    instructions = []
    while True:
        print("1. Before meal")
        print("2. After meal")
        print("3. With meal")
        print("4. Stop")
        instruction_mapping = {"1": "Before meal", "2": "After meal", "3": "With meal", "4": "Stop"}
        instruction_input = input("Enter the corresponding number for instructions: ")
        if instruction_input == "4":
            break
        instruction = instruction_mapping.get(instruction_input, "Invalid choice")
        print(f"Selected instruction: {instruction}")
        instructions.append(instruction)

    return instructions


def get_meal_timing():
    print("Please provide when to eat the medicine (type 'stop' when done):")
    timings = []
    while True:
        print("1. Breakfast")
        print("2. Lunch")
        print("3. Dinner")
        print("4. As advised by Doctor")
        print("5. Stop")
        timing_mapping = {"1": "Breakfast", "2": "Lunch", "3": "Dinner", "4": "As advised by Doctor", "5": "Stop"}
        timing_input = input("Enter the corresponding number for meal timing: ")
        if timing_input == "5":
            break
        timing = timing_mapping.get(timing_input, "Invalid choice")
        print(f"Selected meal timing: {timing}")
        timings.append(timing)

    return timings


def prescribe(doctorid, patientid, appointmentid):
    medicines_list = get_medicines()

    instructions_dict = {}

    print("List of Inputed Medicines:")
    for idx, medicine in enumerate(medicines_list, start=1):
        print(f"{idx}. {medicine}")

    changes_list = []

    print("\nDo you want to edit the medicines? (say 'Change' or 'No'):")
    edit_choice = takecommand()
    if "change" in edit_choice:
        while True:
            print("Which medicine number do you want to modify? (say the number)")
            idx_to_modify = input("Enter the number or type S to exit: ")
            if idx_to_modify.lower() == "s":
                break
            try:
                idx_to_modify = int(idx_to_modify) - 1
                if 0 <= idx_to_modify < len(medicines_list):
                    print(f"Current medicine at position {idx_to_modify + 1}: {medicines_list[idx_to_modify]}")
                    print("Please provide the modified medicine:")
                    modified_medicine = input()
                    changes_list.append((medicines_list[idx_to_modify], modified_medicine))
                    medicines_list[idx_to_modify] = modified_medicine
                else:
                    print("Invalid input. Please say the correct number.")
            except ValueError:
                print("Invalid input. Please say a number.")

    for idx, medicine in enumerate(medicines_list, start=1):
        print(f"{idx}. {medicine}")
        while True:
            instruction = get_instructions()
            timing = get_meal_timing()
            if len(instruction) != len(timing):
                print("Number of instructions and meal timings don't match. Please provide them again.")
            else:
                instructions_dict[medicine] = {"instructions": instruction, "timings": timing}
                break

    print("\nFinal List of Medicines with Instructions:")
    for idx, medicine in enumerate(medicines_list, start=1):
        print(f"{idx}. {medicine}")

    print("\nInstructions for each medicine:")
    for medicine, info in instructions_dict.items():
        ins = ','.join(info['instructions'])
        innlist = ins.split(',')
        eat = ','.join(info['timings'])
        eatlist = eat.split(',')
        temp = ""
        temp = temp + f"{medicine}" + " : \n"
        for i in range(len(innlist)):
            temp += f"Instruction {innlist[i]} Eat During {eatlist[i]}\n"
        print(temp)

    folder_name = "prescriptions"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(folder_name, f"{patientid}_{current_date}.txt")

    with open(filename, 'w') as file:
        file.write(f"Prescription Date: {current_date}\n")
        file.write(f"Doctor ID: {doctorid}\n")
        file.write(f"Patient ID: {patientid}\n")
        file.write(f"Appointment ID: {appointmentid}\n\n")
        file.write("Prescription:\n\n")

        for medicine, info in instructions_dict.items():
            file.write(f"{medicine}:\n")
            for i in range(len(info['instructions'])):
                file.write(f"   Instruction {info['instructions'][i]} Eat During {info['timings'][i]}\n")

    print(f"\nPrescription has been written to {filename}")

    # Save prescription to database
    try:
        # Generate prescription ID by getting the last ID and incrementing
        last_id_query = "SELECT Prescription_ID FROM prescription ORDER BY Prescription_ID DESC LIMIT 1"
        last_id_result = fetch_all(last_id_query)
        
        if last_id_result and last_id_result[0][0]:
            # Extract number from last ID (e.g., "PS5" -> 5)
            last_id = last_id_result[0][0]
            last_num = int(last_id.replace('PS', ''))
            new_num = last_num + 1
        else:
            # No prescriptions exist yet, start with 1
            new_num = 1
        
        prescription_id = f"PS{new_num}"
        
        # Format medications as comma-separated list (max 100 chars)
        medications = ', '.join(medicines_list)
        if len(medications) > 100:
            medications = medications[:97] + '...'
        
        # Format instructions and dosage
        instructions_text = []
        dosage_text = []
        for medicine, info in instructions_dict.items():
            for i in range(len(info['instructions'])):
                instructions_text.append(f"{medicine}: {info['instructions'][i]} - {info['timings'][i]}")
                dosage_text.append(f"{medicine}: {info['instructions'][i]}")
        
        # Truncate to fit database limits
        instructions_str = '; '.join(instructions_text)
        if len(instructions_str) > 100:
            instructions_str = instructions_str[:97] + '...'
        
        dosage_str = '; '.join(dosage_text)
        if len(dosage_str) > 20:
            dosage_str = dosage_str[:17] + '...'
        
        # Insert into prescription table
        insert_query = """
            INSERT INTO prescription
            (Prescription_ID, Date, Medications, Instructions, Dosage, Doctor_ID, Patient_ID, Appointment_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_query(insert_query, (
            prescription_id,
            current_date,
            medications,
            instructions_str,
            dosage_str,
            doctorid,
            patientid,
            str(appointmentid)
        ))
        
        commit_transaction()
        print(f"Prescription saved to database with ID: {prescription_id}")
        
    except Exception as e:
        print(f"Error saving prescription to database: {e}")
        print("Prescription file was created successfully, but database entry failed.")
