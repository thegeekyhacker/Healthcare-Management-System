import json

queue_file_path = 'queue/queue_data.json'
queue_data = {}
def add_to_queue(doctor_id, patient_id):
    with open(queue_file_path, 'r') as file:
        queue_data = json.load(file)

    if doctor_id not in queue_data:
        queue_data[doctor_id] = []

    queue_data[doctor_id].append(patient_id)

    with open(queue_file_path, 'w') as file:
        json.dump(queue_data, file)

def remove_from_queue(doctor_id):
    with open(queue_file_path, 'r') as file:
        queue_data = json.load(file)

    if doctor_id not in queue_data or not queue_data[doctor_id]:
        return None

    removed_patient = queue_data[doctor_id].pop(0)

    with open(queue_file_path, 'w') as file:
        json.dump(queue_data, file)

    return removed_patient

def display_schedule(doctor_id):
    with open(queue_file_path, 'r') as file:
        queue_data = json.load(file)

    if doctor_id not in queue_data or not queue_data[doctor_id]:
        print(f"No patients in the queue for doctor {doctor_id}.")
    else:
        print(f"Queue for doctor {doctor_id}: {queue_data[doctor_id]}")

shared_queue = queue_data