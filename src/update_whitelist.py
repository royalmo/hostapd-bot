from hostapd import whitelist_updater, can_run, get_dummy_mode

if __name__=="__main__" and can_run() and not get_dummy_mode():
    whitelist_updater.update_whitelist()
