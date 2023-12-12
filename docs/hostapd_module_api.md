# Python HostAPd Module API

This document defines the methods that our module provides. We've built the
Telegram Bot on top of it, but it's been created to be able to hold
any type of application.

## Basic Conventions

All mac addresses will be given and provided in **lowercase**:
`'aa:bb:cc:dd:ee:ff'`.

Hour ranges will be represented with integers. The integer `2` represents the
hour range from `02:00` to `03:00`.

## Method definitions

### Master file

The master file provides information about the version and enables the user
to change the JSON file location (where the data is stored).

If there is no JSON file at the specified location, a new file with the
correct format will be created.

### mac_manager.py

This file contains all the mac-related methods.

```py
list_connected() -> list(str)
```

Returns a list of strings as MAC addresses that are currently connected to the
Access Point.

```py
list_enabled() -> list(str)
```

Returns a list of strings as MAC addresses that can connect (in the current
hour range) in the Access Point.

```py
list_all() -> list(str)
```

Returns a list of strings as MAC addresses that can connect (in **any**
hour range) in the Access Point.

```py
ranges_for_mac(mac_address : str) -> list
```

Returns the list of hour ranges that this MAC address can connect. An example
output could be: `[20, 21, 22]`.

```py
update_mac(mac_address : str, hour_ranges : list) -> None
```

Creates or overrides the hour_ranges enabled for a mac_address with the hour
ranges of the parameter. The format is the same as the above method. Kicks the
device if it is currently connected and should not have access.

```py
delete_mac(mac_address : str) -> None
```

Deletes all hour_ranges of a given mac_address. Kicks the device if it is
currently connected.

### user_manager.py

This file works with Telegram UserIDs (integers). However, if you are
planning to use this API with another service, any integer number should
work.

```py
add_admin(telegram_user_id : int) -> None
```

Adds an "admin" to the application. Only admins can talk with the bot. The
first admin should be created through the console, and the others with the bot.

```py
del_admin(telegram_user_id : int) -> None
```

Deletes an "admin" from the application.

```py
is_admin(telegram_user_id : int) -> bool
```

Returns wether a user_id is "admin" of the application.

```py
list_admins() -> list(int)
```

Returns the list of "admin" user Telegram IDs.

```py
subscribe(telegram_user_id : int) -> None
```

Subscribes a user_id to receive notifications from the application.
The bot will notify this user when devices connect and disconnect from the AP.

```py
unsubscribe(telegram_user_id : int) -> None
```

Deletes a user from the subscribed list.

```py
is_subscribed(telegram_user_id : int) -> bool
```

Returns wether a user_id is subscribed to notification from the application.

```py
list_subscribed() -> list(int)
```

Returns the list of subscribed user Telegram IDs.

### notifier.py

This file contains only one function that should be called regularly:

```py
get_new_notifications() -> list(str)
```

Returns the list of notifications to send to each subscribed user.
Each item of the list is the pretty message itself, so it doesn't need any
more formatting.

Once this function is called the buffer will be cleared, so new calls of
this method will not return already sent notifications.

An example output is:

```py
[
    'The device with MAC aa:bb:cc:dd:ee:ff just connected to the AP',
    'The device with MAC ff:ee:dd:cc:bb:aa just disconnected to the AP'
]
```

## Example usage

```py
>>> from hostapd import mac_manager
>>> mac_manager.delete_mac('aa:bb:cc:dd:ee:ff')
```

## License

See the LICENSE file at the root of this repository.
