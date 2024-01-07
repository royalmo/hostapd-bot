import sys, os, re, time

# Thanks https://stackoverflow.com/q/1432924/9643618
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import hostapd
import telepot
from telepot.loop import MessageLoop

hostapd.set_dummy_mode(False)
if not hostapd.can_run():
    sys.exit("\nOnly root can run this script when Dummy mode if Off\n")

# Getting bot token from `hostapd_token.txt`.
token_file = open('hostapd_token.txt', 'r')
BOT_TOKEN = token_file.read().strip()
token_file.close()

bot = telepot.Bot(BOT_TOKEN)

def check_MAC(MAC):
    regex_mac = "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    mac = ''.join(c.lower() for c in MAC if not c.isspace())
    return re.match(regex_mac, mac)

def check_MAC_Interval(args):
    result = args.split()
    try:
        if check_MAC(result[1]):
            for interval in list(result[2].split(",")):
                if 0 < int(interval) and int(interval) > 23:
                    return False
            return True
        else:
            return False
    except:
        return False

def print_help(message, chat_id):
    bot.sendMessage(chat_id, "Here are a list of the commands and it's function:")
    bot.sendMessage(chat_id, "- /start: Welcome message.\n- /help: Display the list of commands.\n- /create: Give access to a new MAC into an interval; you need to provide a MAC and a list of CSV numbers 0-23 (representing hours) (/create XX:XX:XX:XX:XX:XX MM).\n- /update: Update the intervals of an existing MAC; you need to provide a MAC and a list of CSV numbers 0-23 (representing hours) (/update XX:XX:XX:XX:XX:XX MM).\n- /revoke: Revoke permissions to an existing MAC access to the selected interval; you need to provide a MAC (/revoke XX:XX:XX:XX:XX:XX).\n- /active: List active MAC's.\n- /enabled: List MAC's enable to connect now.\n- /all: List all the MAC's that are able to connect among the day.\n- /newadmin: Creates a new admin, you need to provide an user id.\n- /deladmin: Deletes an existing admin, you need to provide an user id.\n- /listadmins: List all admins.\n- /sub: Activates notifications for an specific admin when a MAC connects.\n- /unsub: Desactivate notifications for an specific admin when a MAC connects.\n- /listsubs: List admins who are subscribed to notifications.")


def create_new_user(message, chat_id):
    if check_MAC_Interval(message):
        bot.sendMessage(chat_id, "Updating MAC")
        hostapd.mac_manager.update_mac(str(message.split()[1]), [int(x) for x in message.split()[2].split(',')])
    else:
        bot.sendMessage(chat_id, "Wrong MAC format or interval out of range, please try again!")
    

def revoke_mac(message, chat_id):
    try: 
        if check_MAC(message.split()[1]):
            bot.sendMessage(chat_id,"Deleting MAC") 
            hostapd.mac_manager.delete_mac(message.split()[1])
            
        else:
            bot.sendMessage(chat_id,"Wrong MAC format, please try again!")
    except:
        bot.sendMessage(chat_id,"Wrong MAC format, please try again!")
        
    
def list_actives(message, chat_id):
    actives = hostapd.mac_manager.list_connected()
    if len(actives) > 0:
        bot.sendMessage(chat_id, 'Active:\n- ' + ('\n- '.join(actives)))
    else:
        bot.sendMessage(chat_id, "There are no MAC's connected right now!")
        
    
def list_enabled(message, chat_id):
    enabled = hostapd.mac_manager.list_enabled()
    if len(enabled) > 0:
        bot.sendMessage(chat_id, 'Enabled:\n- ' + ('\n- '.join(enabled)))
    else:
        bot.sendMessage(chat_id, "There are no MAC's available to connect right now, try to add one!")
    

def list_everything(message, chat_id):
    macs = hostapd.mac_manager.list_all()
    if len(macs) > 0:
        bot.sendMessage(chat_id, 'All MACs:\n- ' + ('\n- '.join(macs)))
    else:
        bot.sendMessage(chat_id, "There are no MAC's available to connect, try to add one!")

def add_new_admin(message, chat_id):
    try:
        admin = message.split()[1]
        if not hostapd.user_manager.is_admin(admin):
            hostapd.user_manager.add_admin(admin)
            bot.sendMessage(chat_id, "User " + admin + " added successfully!")
        else:
            bot.sendMessage(chat_id, admin + " is already an admin!")

    except:
        bot.sendMessage(chat_id, "Provide a valid Telegram User id please.")
    
def delete_admin(message, chat_id):
    try:
        admin = message.split()[1]
        if hostapd.user_manager.is_admin(admin):
            hostapd.user_manager.del_admin(admin)
            bot.sendMessage(chat_id, "User " + admin + " deleted successfully!")
        else:
            bot.sendMessage(chat_id, admin + " is not an admin!")
        
    except:
        bot.sendMessage(chat_id, "Provide a valid Telegram User id please.")
        

def list_all_admins(message, chat_id):
    admins = hostapd.user_manager.list_admins()
    if len(admins) > 0:
        bot.sendMessage(chat_id, "Admins:\n - " + ('\n- '.join(admins)))
    else:
        bot.sendMessage(chat_id, "There are no admins, try to add one!")
        

def sub(message, chat_id):
    try:
        admin = message.split()[1]
        if hostapd.user_manager.is_admin(admin) and not hostapd.user_manager.is_subscribed(admin):
            hostapd.user_manager.subscribe(admin)
            bot.sendMessage(chat_id, "user " + admin + " subscribed successfully!")
        else:
            bot.sendMessage(chat_id,admin + " is not an admin or is already subscribed!")

    except:
        bot.sendMessage(chat_id, "Provide a valid Telegram User id please.")

def unsub(message, chat_id):
    try:
        admin = message.split()[1]
        if hostapd.user_manager.is_admin(admin) and hostapd.user_manager.is_subscribed(admin):
            hostapd.user_manager.unsubscribe(admin)
            bot.sendMessage(chat_id, "user " + admin + " unsubscribed successfully!")
        else:
            bot.sendMessage(chat_id,admin + " is not an admin or is already unsubscribed!")
        
    except:
        bot.sendMessage(chat_id,"Provide a valid Telegram User id please.")


def list_all_subs(message, chat_id):
    subscribed = hostapd.user_manager.list_subscribed()
    if len(subscribed) > 0:
        bot.sendMessage(chat_id, "Subscribed:\n - " + ('\n- '.join(subscribed)))
    else:
        bot.sendMessage(chat_id, "There are no subscribed users, try to add one!")


COMMANDS = {
    'help': print_help,
    'create': create_new_user,
    'update': create_new_user,
    'revoke': revoke_mac,
    'active': list_actives,
    'enabled': list_enabled,
    'all': list_everything,
    'newadmin': add_new_admin,
    'deladmin': delete_admin,
    'listadmins': list_all_admins,
    'sub': sub,
    'unsub': unsub,
    'listsubs': list_all_subs
}
    
def handle(msg):
    content_type, _, chat_id = telepot.glance(msg)
    print(f"[INFO] Got message from chat_id {chat_id}.")

    if content_type != 'text':
        return
    
    message = msg['text']
    print(f"[INFO] Message text: {message}")

    if message == '/start':
        bot.sendMessage(chat_id, 'Hello! Type /help to know the list of messages.')
        return

    if not hostapd.user_manager.is_admin(chat_id):
        print("User is not an ADMIN. Aborting.")
        return

    for command, func in COMMANDS.items():
        if message.startswith(f"/{command}"):
            func(message, chat_id)
            return
    
    bot.sendMessage(chat_id, 'Unknown command. /help')


MessageLoop(bot, handle).run_as_thread()
print('[INFO] HostAPd Manager Telegram Bot Started successfully.')

# Keep the program running while polling new notifications
while 1:
    time.sleep(10)

    if hostapd.notifier.check_new_notifications():
        notifications = hostapd.notifier.get_new_notifications()
        subscribed = hostapd.user_manager.list_subscribed()
        for to_send in notifications:
            for admin in subscribed:
                bot.sendMessage(admin, to_send)
