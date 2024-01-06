# Project installation

This document contains all the required steps to install this application
in a **Raspberry Pi 4**. It should be compatible with most Raspberry Pi models
and Debian systems, and it may also work with other GNU/Linux distributions.

## Requirements

You need a system with:

- A WiFi antenna. Ours is `wlan0` (replace with yours in the commands below).
- Another device that can provide internet to your system. For example, an
  Ethernet port or another WiFi antenna. In our case we used `eth0`.
- You will create a new private network, so you need to choose a range of IP
  addresses (prefix and submask) that aren't in use. In this project I've
  used `192.168.4.0/24`, where `192.168.4.1` is the gateway (the Raspberry
  itself).

## Installation

We will start by installing the required packages:

```sh
sudo apt install dnsmasq hostapd -y
sudo python3 -m pip install telepot
```

Then, we will **append** to `/etc/dhcpcd.conf` (`sudo nano /etc/dhcpcd.conf`):

```
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant 
```

And we will restart dhcpd:

```sh
sudo systemctl restart dhcpcd
```

Next up we will set the DHCP server for our new network, so new devices don't
need to set up their IP address manually. We will create the
configuration from zero, so we first moved the default config file.

```sh
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf 
```

In that file we will write:

```
interface=wlan0
  dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h 
```

**Important!** Note the two spaces before the `dhcp-range` line. These are very
important, because without the spaces this line will affect only the default
interface (eth0).

Once this set, we can restart dnsmasq.

```sh
sudo systemctl reload dnsmasq
```

Finally, we arrive at the WiFi AP settings. We will create a file at
`/etc/hostapd/hostapd.conf` with the following contents
(`sudo nano /etc/hostapd/hostapd.conf`):

```
interface=wlan0
driver=nl80211
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=1
accept_mac_file=/etc/hostapd/accept.conf
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0

ssid=WIFI_AP_SSID
wpa_passphrase=WIFI_AP_KEY
```

Change the last two settings (ssid and key) to your desired network name
and password.

Now we need to tell hostAPd where this file is located.
Edit `/etc/default/hostapd` (`sudo nano /etc/default/hostapd`) and add (or
replace) the `DAEMON_CONF` setting with
`DAEMON_CONF="/etc/hostapd/hostapd.conf"`.
Do the same process for `DAEMON_OPTS`

We're arriving at the end. These commands will start hostapd and setup
a NAT router between `wlan0` and `eth0`:

```
sudo touch /etc/hostapd/accept.conf
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

## Set up crons

Last but not least, you need to set up periodic tasks to be executed. Our
project needs to update the HostAPd whitelist every hour, so instead on relying
on Python's logic, we will set up a cron task.

Run:

```
sudo crontab -e
```

If this is the first time you run this command, crontab will ask you which
text editor would you like to use. I am a nano lover, but that's up to you!

Then, at the end of the file, write:

```
0 * * * * /usr/bin/python3 /home/pi/path/to/repository/src/update_whitelist.py
```

## Telegram Bot setup

You will need to create a Telegram Bot. Talk to `@botfather` and follow its
steps. You will end with a **Telegram Token**. Store it in a file in the
`/src` directory called `hostapd_token.txt`

```
echo "123456789:aabbcccddeeffgghhiijjkkmmnnooppqq" > hostapd_token.txt
sudo python3 telegram_bot.py
```

You will then be able to run the main program.

## Add an admin manually

You can send `/start` to the Telegram bot `@userinfobot` to know your user ID.
Once you got it, you can execute this command to add yourself as an admin.

```
sudo python3 add_admin.py 123456789
```

Replace 123456789 in the command above for your userID.

## Start the project automatically after a reboot

Finally, we will want our project to restart after a system reboot.

We just need to add to `/etc/rc.local` (the script that is executed after
the Raspberry Pi has booted itself) the following line **before** the
`exit 0` line.

```
iptables-restore < /etc/iptables.ipv4.nat
/usr/bin/python3 /home/pi/path/to/repository/src/telegram_bot.py
```
