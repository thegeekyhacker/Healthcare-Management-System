import json
import sys
import re

DEFAULT_PORT = 3000
with open("log.json", "r") as f:
    logs = json.load(f)["log"]

while True:
    key = input("Enter the key to search for: ")
    regex = input(f"Enter the regex for key '{key}' to search: ")

    filtered_logs = [
        log for log in logs if key in log and re.search(regex, str(log[key]))
    ]

    print(f"\nLogs with '{key}'='{regex}':")
    print()
    for log in filtered_logs:
        for l in log:
            print(l, " : ", log[l], "\n")

    port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if port != DEFAULT_PORT:
        port = DEFAULT_PORT
    print("Do you want another filter ?")
    print("Enter '1' for yes or '0' for no : ")
    choice = int(input())
    if choice == 0:
        exit(0)
    elif choice == 1:
        key = input("Enter the key to search for: ")
        regex = input(f"Enter the regex for key '{key}' to search: ")
        filtered_logs = [
            log
            for log in filtered_logs
            if key in log and re.search(regex, str(log[key]))
        ]
        print(f"\nLogs with '{key}'='{regex}':")
        print()
        for log in filtered_logs:
            for l in log:
                print(l, " : ", log[l], "\n")
        choice = int(
            input("Do you want another filter?\nEnter '1' for yes or '0' for no : ")
        )
        if choice == 0:
            exit(0)
    else:
        print("Kindly enter either '0' or '1'")
