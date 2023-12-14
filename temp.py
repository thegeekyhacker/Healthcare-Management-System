from datetime import datetime, date

def calculate_age(birthdate_str):
    # Parse the input string into a datetime.date object
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()

    # Get the current date
    current_date = date.today()

    # Calculate the age
    age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    return age

# Example usage:
birthdate_str = "2001-12-18"
age = calculate_age(birthdate_str)
print(f"The age is: {age} years")
