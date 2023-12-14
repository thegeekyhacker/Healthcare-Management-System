import datetime

def greeting():
    hour = int(datetime.datetime.now().hour)
    if hour>=5 and hour < 12:   
        return "Good morning!" 
    elif hour >= 12 and hour < 16 :  
        return "Good afternoon!"
    elif hour >= 16 and hour < 20:    
        return "Good evening!"
    elif hour > 20 or hour<5:
        return "Good night!"