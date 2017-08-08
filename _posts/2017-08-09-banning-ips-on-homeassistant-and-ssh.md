---
layout: post
title: 'Banning IPs from Home Assistant and SSH'
date: 2017-08-09 09:00
description: How I ban unathorized logins to Home Assistant and SSH
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - home automation
  - scripts
use_math: false
project: false
feature: false
---
https://home-assistant.io/cookbook/fail2ban/

```
sudo apt-get install fail2ban
sudo touch /etc/fail2ban/fail2ban.local
sudo touch /etc/fail2ban/filter.d/hass.local
sudo touch /etc/fail2ban/jail.local
```

First, `/etc/fail2ban/fail2ban.local`:
```
[Definition]
logtarget = SYSLOG
```

Next `/etc/fail2ban/filter.d/hass.local`:
```
[INCLUDES]
before = common.conf

[Definition]
failregex = ^%(__prefix_line)s.*Login attempt or request with invalid authentication from <HOST>.*$

ignoreregex =

[Init]
datepattern = ^%%y-%%m-%%d %%H:%%M:%%S
```

Last, `/etc/fail2ban/jail.local` (note, `logpath` should point to your home-assistant directory):
```
[hass-iptables]
enabled = true
filter = hass
action = iptables-allports[name=HASS]
logpath = /home/hass/.homeassistant/home-assistant.log
maxrety = 5

[ssh]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
```

Now we can start fail2ban:

```
sudo systemctl restart fail2ban
```

# Integrate into Home Assistant

