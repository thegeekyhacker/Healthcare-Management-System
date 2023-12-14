import speech_recognition as sr
import datetime
import os 


def takecommand():
    # It takes microphone input from the user and returns string output
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
        return query.lower()  # Returning lowercase for uniform comparison
    except Exception as e:
        print(e)
        print("Say that Again please....")
        return "None"

def get_medicines():
    medicines = []
    while True:
        print("Please provide the medicine:")
        medicine = takecommand()  # Use voice input to get medicine
        if medicine.lower() == "stop":  # Assuming "stop" indicates the end of medicine input
            break
        elif medicine.lower() != "none":  # Ignore if the medicine name is "None"
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

# Main execution
def prescribe(doctorid,patientid,appointmentid):
    medicines_list = get_medicines()

    # Dictionary to store instructions for each medicine
    instructions_dict = {}

    # Print the list of inputted medicines
    print("List of Inputted Medicines:")
    for idx, medicine in enumerate(medicines_list, start=1):
        print(f"{idx}. {medicine}")

    # List to store changes in medicines
    changes_list = []

    # Provide an option for the doctor to edit the medicines list
    print("\nDo you want to edit the medicines? (say 'Change' or 'No'):")
    edit_choice = takecommand()
    if "change" in edit_choice:
        while True:
            print("Which medicine number do you want to modify? (say the number)")
            idx_to_modify = input("Enter the number or type S to exit: ")
            if idx_to_modify.lower() == "s":
                break
            try:
                idx_to_modify = int(idx_to_modify) - 1  # Doctor says the number to modify
                if 0 <= idx_to_modify < len(medicines_list):
                    print(f"Current medicine at position {idx_to_modify + 1}: {medicines_list[idx_to_modify]}")
                    print("Please provide the modified medicine:")
                    modified_medicine = input()  # Allow typing the modified medicine
                    changes_list.append((medicines_list[idx_to_modify], modified_medicine))
                    medicines_list[idx_to_modify] = modified_medicine
                else:
                    print("Invalid input. Please say the correct number.")
            except ValueError:
                print("Invalid input. Please say a number.")

    # Doctor's option to provide instructions for each medicine
    for idx, medicine in enumerate(medicines_list, start=1):
        print(f"{idx}. {medicine}")
        instruction_count = 0
        while True:
            instruction = get_instructions()
            timing = get_meal_timing()
            if len(instruction) != len(timing):
                print("Number of instructions and meal timings don't match. Please provide them again.")
            else:
                instructions_dict[medicine] = {"instructions": instruction, "timings": timing}
                break

    # Updated list of medicines with instructions
    print("\nFinal List of Medicines with Instructions:")
    for idx, medicine in enumerate(medicines_list, start=1):
        print(f"{idx}. {medicine}")

    # Print all instructions for each medicine
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

    # Writing prescription to a .txt file within the "prescriptions" folder
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


# prescribe('D1','P1','A1')