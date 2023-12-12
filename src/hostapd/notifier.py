from . import _file_manager

def get_new_notifications():
    data = _file_manager.get_json_data()
    notifications = data['pending-notifications']
    data['pending-notifications'] = []
    _file_manager.write_json_data(data)
    return notifications
