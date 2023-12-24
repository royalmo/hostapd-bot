# HostAPd Bot

*A Telegram Bot to manage a hostapd whitelist and notify events.*

## Features

Your setup is a Raspberry Pi connected to the network with its ethernet port.
You will then use the device's antenna to start an Access Point with *hostapd*.

You want your AP to:
- Only accept certain MAC addresses.
- Each MAC address will only be accepted between the desired time slots.
- You will be notified when a device connects or disconnects to the network.
- The MAC list and time slots should be easily accessed.
- You will want to choose who can change these settings and receive notifations.

HostAPd bot is a Telegram Bot that will manage all of it.

## How To

Look at **docs/installation.md** for instructions to install everything on a
new Raspberry Pi.

Then, look at **docs/tutorial.md** to see how you can interact with the
Telegram Bot.

## Contribute

This project is Open Source and is part of the EPSEM's Communication Systems
course projects plan. More information on (itic.cat)[https://itic.cat].

To contribute just post a issue or a pull request. Please use similar codebase
structure to the one already used.

## Liscense

This project is under the MIT Liscense. See more information in the LICENSE
file of this repository.
