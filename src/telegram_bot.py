import hostapd, sys

hostapd.set_dummy_mode(True)
if not hostapd.can_run():
    sys.exit("\nOnly root can run this script when Dummy mode if Off\n")

print("Hostapd library basic testing")
print(f"Current MACs in the database: {hostapd.mac_manager.list_all()}")
print(f"Adding MAC aa:bb:cc:dd:ee:ff to 3 hour ranges.")
hostapd.mac_manager.update_mac('aa:bb:cc:dd:ee:ff', [1,2,3,4])
print(f"Ranges for this MAC now: {hostapd.mac_manager.ranges_for_mac('aa:bb:cc:dd:ee:ff')}")
print(f"Adding user 123 to admins.")
hostapd.user_manager.add_admin(123)
print(f"Is user 123 an admin? {hostapd.user_manager.is_admin(123)}")
print(f"Admin users: {hostapd.user_manager.list_admins()}")
print("Test ended.")
