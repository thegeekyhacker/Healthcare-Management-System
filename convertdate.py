from datetime import datetime

def convert_date_format(date_string):
    # Parse the input string to a datetime object
    date_object = datetime.strptime(date_string, '%Y %m %d')

    # Convert the datetime object to the desired format
    formatted_date = date_object.strftime('%d %B %Y')  # %B gives the full month name

    return formatted_date

