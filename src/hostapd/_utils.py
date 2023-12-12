from datetime import datetime

ACT_AS_DUMMY = False

def current_hour():
    return datetime.now().hour

def get_dummy_mode():
    return ACT_AS_DUMMY

def set_dummy_mode(val):
    global ACT_AS_DUMMY
    ACT_AS_DUMMY = val
