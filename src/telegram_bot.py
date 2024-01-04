    import hostapd, sys
    import os
    import telebot
    import threading
    import re
    from telebot import types
    from parse import *



    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    bot = telebot.TeleBot('6331494696:AAHChyiRaTdc94F9SQ13uLqCryJZY476TpM', parse_mode=None)


    hostapd.set_dummy_mode(True)
    if not hostapd.can_run():
        sys.exit("\nOnly root can run this script when Dummy mode if Off\n")


    def schedule_function():
        print("hello")  
        threading.Timer(10.0, schedule_function).start()  # Schedule the function to run again in X seconds


    def check_MAC(MAC):
        
        regex_mac ="[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" 
        mac = ''.join(c.lower() for c in MAC if not c.isspace())
        return re.match(regex_mac, MAC) 


    def check_MAC_Interval(args):
        
        result = args.split()
        print(result)
        try:
            if check_MAC(result[1]):
                mac_list = hostapd.mac_manager.ranges_for_mac(result[1])
                print(mac_list)
            
                for interval in list(result[2].split(",")):
                    print(interval)
                    if 1 <= int(interval) and int(interval) >= 24:
                        return False
                    # TODO
                    # elif interval not in mac_list: 
                    #     return False
                return True
            else:
                return False   
        except:
            return False

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("/start")
        item2 = types.KeyboardButton("/help")
        item3 = types.KeyboardButton("/create")
        item4 = types.KeyboardButton("/update")
        item5 = types.KeyboardButton("/revoke")
        item6 = types.KeyboardButton("/active")
        markup.add(item1, item2, item3, item4, item5, item6)
        
        bot.reply_to(message, "Howdy, how are you doing? Please choose an option:", reply_markup=markup)
        
        
    @bot.message_handler(commands=['help'])
    def print_help(message):
        reply = bot.reply_to(message, "Here are a list of the commands and it's function:")
        bot.send_message(message.chat.id, "- /start: Welcome message.\n- /help: Display the list of commands.\n- /create: Give acces to a new MAC into an interval; you need to provide a MAC and select an interval between 1-12 (/create XX:XX:XX:XX:XX:XX MM).\n- /revoke: Revoke permissions to an existing MAC acces to the selected interval; you need to provide a MAC and select an interval between 1-12 (/revoke XX:XX:XX:XX:XX:XX MM).\n- /active: List active MAC's.")
        
        
    @bot.message_handler(commands=['create', 'update'])
    def create_new_user(message):
        if check_MAC_Interval(message.text):
            bot.reply_to(message, "CORRECT!!!") 
            hostapd.mac_manager.update_mac(message.text.split()[1], message.text.split()[2])
            # Crida funcio eric
            
        else:
            bot.reply_to(message, "Wrong MAC format or interval out of range, please try again!")
        
        
    @bot.message_handler(commands=['revoke'])
    def send_welcome(message):
        try: 
            if check_MAC(message.text.split()[1]):
                bot.reply_to(message, "CORRECT!!!") 
                hostapd.mac_manager.delete_mac(message.text.split()[1])
                # Crida funcio eric
                
            else:
                bot.reply_to(message, "Wrong MAC format or interval out of range, please try again!")
        except:
            bot.reply_to(message, "Wrong MAC format or interval out of range, please try again!")
            
        
    @bot.message_handler(commands=['active'])
    def list_actives(message):
        print(hostapd.mac_manager.list_connected())
        bot.reply_to(message, hostapd.mac_manager.list_connected())
        
    @bot.message_handler(commands=['enabled'])
    def list_enabled(message):
        print(hostapd.mac_manager.list_enabled())
        try:
            bot.reply_to(message, hostapd.mac_manager.list_enabled())
        except:
            bot.send_message(message.chat.id, "There are no MAC's available to connect right now, try to add one!")
        
    @bot.message_handler(commands=['all'])
    def list_everything(message):
        print(hostapd.mac_manager.list_all())
        try:
            bot.reply_to(message, hostapd.mac_manager.list_all())
        except:
            bot.send_message(message.chat.id, "There are no MAC's available to connect, try to add one!")

    @bot.message_handler(commands=['newadmin'])
    def add_new_admin(message):
        admin = message.text.split()[1]
        try:
            if not hostapd.user_manager.is_admin(admin):
                hostapd.user_manager.add_admin(admin)
                bot.send_message(message.chat.id, "user " + admin + " added succesfully!")
            else:
                bot.reply_to(message, admin + " is already an admin!")
            
        except:
            bot.reply_to(message, "Provide a valid Telegram User id please.")
        
    @bot.message_handler(commands=['deladmin'])
    def delete_admin(message):
        admin = message.text.split()[1]
        try:
            if hostapd.user_manager.is_admin(admin):
                hostapd.user_manager.del_admin(admin)
                bot.send_message(message.chat.id, "user " + admin + " deleted succesfully!")
            else:
                bot.reply_to(message, admin + " is not an admin!")
            
        except:
            bot.reply_to(message, "Provide a valid Telegram User id please.")
            
    @bot.message_handler(commands=['listadmins'])
    def list_all_admins(message):
        try:
            bot.reply_to(message, hostapd.user_manager.lit_admins())
        except:
            bot.send_message(message.chat.id, "There are no admins, try to add one!")
            
    @bot.message_handler(commands=['sub'])
    def sub(message):
        admin = message.text.split()[1]
        try:
            if hostapd.user_manager.is_admin(admin) and not hostapd.user_manager.is_subscribed(admin):
                hostapd.user_manager.subscribe(admin)
                bot.send_message(message.chat.id, "user " + admin + " suscribed succesfully!")
            else:
                bot.reply_to(message, admin + " is not an admin or is already subscribed!")
            
        except:
            bot.reply_to(message, "Provide a valid Telegram User id please.")
            
    @bot.message_handler(commands=['unsub'])
    def sub(message):
        admin = message.text.split()[1]
        try:
            if hostapd.user_manager.is_admin(admin) and hostapd.user_manager.is_subscribed(admin):
                hostapd.user_manager.unsubscribe(admin)
                bot.send_message(message.chat.id, "user " + admin + " unsuscribed succesfully!")
            else:
                bot.reply_to(message, admin + " is not an admin or is already unsubscribed!")
            
        except:
            bot.reply_to(message, "Provide a valid Telegram User id please.")


    @bot.message_handler(commands=['listsubs'])
    def list_all_admins(message):
        try:
            bot.reply_to(message, hostapd.user_manager.list_subscribed())
        except:
            bot.send_message(message.chat.id, "There are no admins subscribed, try to add one!")

    schedule_function()

    bot.infinity_polling()



    # print("Hostapd library basic testing")
    # print(f"Current MACs in the database: {hostapd.mac_manager.list_all()}")
    # print(f"Adding MAC aa:bb:cc:dd:ee:ff to 3 hour ranges.")
    # hostapd.mac_manager.update_mac('aa:bb:cc:dd:ee:ff', [1,2,3,4])
    # print(f"Ranges for this MAC now: {hostapd.mac_manager.ranges_for_mac('aa:bb:cc:dd:ee:ff')}")
    # print(f"Adding user 123 to admins.")
    # hostapd.user_manager.add_admin(123)
    # print(f"Is user 123 an admin? {hostapd.user_manager.is_admin(123)}")
    # print(f"Admin users: {hostapd.user_manager.list_admins()}")
    # print("Test ended.")
