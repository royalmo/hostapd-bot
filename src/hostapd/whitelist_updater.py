from . import get_dummy_mode, mac_manager
import subprocess, os

# Gets the enabled MAC addresses but from the hostapd_cli, so its 100% real.
def get_enabled_macs_hard():
    if get_dummy_mode(): return []

    temp = subprocess.Popen(['hostapd_cli', 'accept_acl SHOW'], stdout = subprocess.PIPE) 
    output = str(temp.communicate()).split('\n')
    enabled_macs = []
    if len(output) > 1:
        # First line is 'interface info' so we will ignore it
        output = output[1:]
        for line in output:
            # Line format is aa:bb:cc:dd:ee:ff VLAN=0, so we only want the MAC
            enabled_macs.append(line.split(' ')[0])

def update_whitelist():
    if get_dummy_mode(): return

    real_enabled_macs = get_enabled_macs_hard()
    json_enabled_macs = mac_manager.list_enabled()

    for current_mac in real_enabled_macs:
        if current_mac not in json_enabled_macs:
            # Removing from whitelist
            os.system(f"hostapd_cli accept_acl DEL_MAC {current_mac}")
            # Disconnecting (whitelist is only checked when connecting to AP)
            # This command would not be needed if the user is not connected,
            # but we throw it anyway for the sake of safety.
            os.system(f"hostapd_cli deauthenticate {current_mac}")

    for current_mac in json_enabled_macs:
        if current_mac not in real_enabled_macs:
            # Whitelist
            os.system(f"hostapd_cli accept_acl ADD_MAC {current_mac}")
