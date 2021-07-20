from datetime import datetime

def getMonth():
    current_month = datetime.now().strftime('%m')
    return current_month

def getYear():
    current_year_full = datetime.now().strftime('%Y')
    return current_year_full
