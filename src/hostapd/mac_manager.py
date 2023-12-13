from ._utils import ACT_AS_DUMMY, current_hour
from . import _file_manager, whitelist_updater

import random, subprocess

def list_connected():
    if ACT_AS_DUMMY:
        # Choose random devices
        enabled = list_enabled()
        sample_size = random.randint(0, len(enabled))
        return random.sample(enabled, sample_size)

    temp = subprocess.Popen(['bash', "-c \"iw dev wlan0 station dump | grep Station | cut -f 2 -s -d' '\""], stdout = subprocess.PIPE) 
    return str(temp.communicate()).split('\n')

def list_enabled():
    data = _file_manager.get_json_data()
    return data['hour-ranges'][current_hour()]

def list_all():
    data = _file_manager.get_json_data()
    flattened_data = [item for sublist in data['hour-ranges'] for item in sublist]
    # Remove duplicates and return
    return list(set(flattened_data))

def ranges_for_mac(mac_address):
    result = []
    data = _file_manager.get_json_data()
    for hour_start in range(24):
        macs_for_hour = data['hour-ranges'][hour_start]
        if mac_address in macs_for_hour:
            result.append(hour_start)
    return result

def update_mac(mac_address, hour_ranges):
    previous_enabled_macs = list_enabled()
    data = _file_manager.get_json_data()
    for hour in range(24):
        if hour in hour_ranges and mac_address not in data['hour-ranges'][hour]:
            data['hour-ranges'][hour].append(mac_address)
        if hour not in hour_ranges and mac_address in data['hour-ranges'][hour]:
            data['hour-ranges'][hour].remove(mac_address)

    _file_manager.write_json_data(data)
    current_enabled_macs = list_enabled()

    if ACT_AS_DUMMY or previous_enabled_macs == current_enabled_macs: return

    # If we get here we need to reload hostAPd whitelist.
    whitelist_updater.update_whitelist()

def delete_mac(mac_address):
    # This specific implementation makes removing the same as
    # not having any hour range
    update_mac(mac_address, [])
