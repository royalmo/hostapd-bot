from . import _file_manager

def add_admin(telegram_user_id):
    data = _file_manager.get_json_data()
    if telegram_user_id in data['admins']: return
    data['admins'].append(telegram_user_id)
    _file_manager.write_json_data(data)

def del_admin(telegram_user_id):
    data = _file_manager.get_json_data()
    if telegram_user_id not in data['admins']: return
    data['admins'].remove(telegram_user_id)
    _file_manager.write_json_data(data)

def is_admin(telegram_user_id):
    return str(telegram_user_id) in list_admins()

def list_admins():
    data = _file_manager.get_json_data()
    return data['admins']

def subscribe(telegram_user_id):
    data = _file_manager.get_json_data()
    if telegram_user_id in data['subscribed']: return
    data['subscribed'].append(telegram_user_id)
    _file_manager.write_json_data(data)

def unsubscribe(telegram_user_id):
    data = _file_manager.get_json_data()
    if telegram_user_id not in data['subscribed']: return
    data['subscribed'].remove(telegram_user_id)
    _file_manager.write_json_data(data)

def is_subscribed(telegram_user_id):
    return telegram_user_id in list_subscribed()

def list_subscribed():
    data = _file_manager.get_json_data()
    return data['subscribed']

