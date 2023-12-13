from . import _file_manager, get_dummy_mode
from time import strftime, localtime

def _get_new_logs():
    if get_dummy_mode(): return []
    with open('/var/log/hostapd.log', 'r+') as f:
        new_logs = f.readlines()
        f.write('')
    return new_logs

def get_new_notifications():
    data = _file_manager.get_json_data()
    notifications = data['pending-notifications']
    data['pending-notifications'] = []
    _file_manager.write_json_data(data)
    return notifications

def check_new_notifications():
    if get_dummy_mode(): return

    new_logs = _get_new_logs()
    parsed_notifications = []

    for log_line in new_logs:
        if "not allowed to connect" in log_line:
            # Example log line:
            # 1702465738.308627: STA 20:34:fb:b9:6e:37 not allowed to connect
            epoch_timestamp = int(log_line.split('.')[0])
            mac_address = log_line.split(' ')[2]
            formatted_time = strftime('%Y/%m/%d %H:%M:%S', localtime(epoch_timestamp))
            parsed_notifications.append(f"Denied connection to device with MAC address {mac_address} at {formatted_time}")
        if "AP-STA-CONNECTED" in log_line:
            # Example log line:
            # 1702465771.784862: wlan0: AP-STA-CONNECTED 20:34:fb:b9:6e:37
            epoch_timestamp = int(log_line.split('.')[0])
            mac_address = log_line.split(' ')[3]
            formatted_time = strftime('%Y/%m/%d %H:%M:%S', localtime(epoch_timestamp))
            parsed_notifications.append(f"Device with MAC address {mac_address} connected at {formatted_time}")
        if "AP-STA-DISCONNECTED" in log_line:
            # Example log line:
            # 1702465795.780074: wlan0: AP-STA-DISCONNECTED 20:34:fb:b9:6e:37
            epoch_timestamp = int(log_line.split('.')[0])
            mac_address = log_line.split(' ')[3]
            formatted_time = strftime('%Y/%m/%d %H:%M:%S', localtime(epoch_timestamp))
            parsed_notifications.append(f"Device with MAC address {mac_address} disconnected at {formatted_time}")

    if len(parsed_notifications): return

    data = _file_manager.get_json_data()
    data["pending-notifications"] += parsed_notifications
    _file_manager.write_json_data(data)
