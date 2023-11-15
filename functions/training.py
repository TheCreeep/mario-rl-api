import datetime

def generate_filename():
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H.%M.%S")
    return filename