from sys import argv
from hostapd import user_manager

if len(argv)==2:
    user_manager.add_admin(argv[1])
else:
    print("Wrong number of arguments. Usage: python3 add_admin.py <USER_ID>")
