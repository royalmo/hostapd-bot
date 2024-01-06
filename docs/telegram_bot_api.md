# Telegram bot API

This document defines the commands and capabilities of our bot. 
It's been created to be able to hold any type of application.

## Basic Conventions

All mac addresses will be given and provided in any form, but always following the next format:
`'aa:bb:cc:dd:ee:ff'` or `'aa-bb-cc-dd-ee-ff'`.

Hour ranges will be represented with integers. The integer `2` represents the
hour range from `02:00` to `03:00`. These ranges must go between 1-24, otherwise they will be 
rejected.

## Commands definitions

### /help

Provides a list of all commands and a brief explanation of how it works and what 
must be the input from the user for the command to work.

```py
/help
```

### /create

Creates a new access of an specific MAC adress into an specific time interval.

```py
/create aa:bb:cc:dd:ee:ff 1,2,5,12
```

### /update

Updates an existing MAC adress intervals, adding or deleting the old ones.

```py
/update aa:bb:cc:dd:ee:ff 1,3,5,12,22,20
```

### /revoke

Revokes all the access to an specific MAC address.

```py
/revoke aa:bb:cc:dd:ee:ff
```

### /active

Lists all the active MAC's in the actual interval.

```py
/active
```

### /enabled

Lists all the MAC's that are available to connect right now.

```py
/active
```

### /enabled

Lists all the MAC's that are available to connect among all the intervals.

```py
/all
```

### newadmin

Adds a new admin to the system, these admin must be provided as a telegram
user id, it is not enough with the @. Make sure you type it correctly!!

```py
/newadmin XXXXXXXXX
```

### /deladmin

Deletes an existing admin of the system by typing his telegram user id.

```py
/deladmin XXXXXXXXX
```

### /listadmins

List all existing admins.

```py
/listadmins
```

### /sub

Subscribe an existing admin to recieving notifications every time a new MAC connects.
(To actually recieve the notification, the admin subscribed **MUST** have already 
send a message to the bot in first instance).

```py
/sub XXXXXXXXX
```

### /unsub

Unsuscribe an already subscribed admin to recieving any notifications every
time a new MAC connects.

```py
/unsub XXXXXXXXX
```

### /listsubs

List all existing admins subscribed.

```py
/lisubs
```

## License

See the LICENSE file at the root of this repository.
