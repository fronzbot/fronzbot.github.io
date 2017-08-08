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
I like knowing what's happening on my home network, especially with how many things I have that I rely on ([PiHole](https://pi-hole.net/), [Home-Assistant](https://home-assistant.io), etc).  One thing I've been missing is the ability to check for unwanted visitors.  I want to know if someone is trying to get into my network, log their ip, and ban them.  Ultimately, there are two areas I want to prevent traffic:
- Home Assistant frontend
- SSH

Lukily, both of these tasks can be solved by using [fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page)

# Setting Up fail2ban for SSH
First we will want to install the service:
```bash
$ sudo apt-get install fail2ban
```

Next, we need to create the `/etc/fail2ban/fail2ban.local` file with the following contents:

```
[Definition]
logtarget = SYSLOG
```

After that, we need to create the `/etc/fail2ban/jail.local` file whose contents should be:

```
[ssh]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
```

At this point, once we start the fail2ban service, we should be set and fail2ban will auto-ban IPs for us on failed SSH login attempts.  But I also want to be able to ban IPs trying to log into my Home Assistant front-end...

# Setting up fail2ban with Home Assistant
I mostly took these instructions from [this page](https://home-assistant.io/cookbook/fail2ban/) with a couple small mofications.

First, we need a filter to parse the home-assistant log and check for aunthorized login attempts.  This is done by creating the `/etc/fail2ban/filter.d/hass.local` file with the following contents:

```
[INCLUDES]
before = common.conf

[Definition]
failregex = ^%(__prefix_line)s.*Login attempt or request with invalid authentication from <HOST>.*$

ignoreregex =

[Init]
datepattern = ^%%y-%%m-%%d %%H:%%M:%%S
```

The next step is to edit the `/etc/fail2bain/jail.local` file we created earlier and add the following:
```
...
[hass-iptables]
enabled = true
filter = hass
action = iptables-allports[name=HASS]
logpath = /home/hass/.homeassistant/home-assistant.log
maxrety = 5
```

You'll need to replaced the `logpath` with the location of you log within your home-assistant installation.

Now we can enable and start fail2ban:

```bash
$ sudo systemctl enable fail2ban
$ sudo systemctl start fail2ban
```

# Integrate into Home Assistant
Right now, fail2ban operates in the background and logs any failed attempts to `/var/log/syslog`.  We can see failed Home Assistant attempts by looking that the log, but ssh attempts are transparent.  We can change this though.

What I want is a sensor that I can display on my frontend showing any failed SSH or Hass attempts and also receive a notification with a timestamp when this happens.  I do this via a combination of the [command line sensor](https://home-assistant.io/components/sensor.command_line/), [file sensor](https://home-assistant.io/components/sensor.file/), and [notify](https://home-assistant.io/components/notify/) service.  Really, you could eliminate the file sensor altogether and do all of this within the command line sensor, but I found it to be more managable running a command, generating a json file, and using the file sensor to display the results.

## Command-Line Sensor
The first thing I want to do is parse the syslog file and only operate on the parts I care about.  I can do all of this in a python script (which we'll need to generate the json file used in the `sensor.file` component) but I opted for a bash script.

To start, create a file under `.homeassistant/bin` called `gen_ban_list.sh`.

First, we need to find all the `fail2ban` entries in syslog and only dump the Ban/Unban events to a file:

### Parse syslog

```bash
more /var/log/syslog | grep fail2ban | grep WARNING > /home/hass/.homeassistant/ip_ban_list.log
```

Right now, a 'ban' entry will loog something like:
```bash
Aug  8 12:34:26 raspberrypi fail2ban.action[6341]: WARNING [ssh] Ban 111.222.12.100
Aug  8 12:34:26 raspberrypi fail2ban.action[6341]: WARNING [hass-iptables] Ban 111.222.12.100
```

Those entries have a lot of useless information, so we need to strip this out.  I use `sed` with some regular expressions.

### Prepare File for Processing

First, let's get rid of the string starting from `raspberrypi` all the way through `WARNING`:
```bash
sed -i 's/raspberrypi fail2ban\.actions\[[^]]*\]: WARNING//g' <FILE>
```

If you're unfamiliar with regular expressions, the format is simple: `s/FIND/REPLACE/g` which in plain English would translate to something like:

> Search the file and globally replace entries matching 'FIND' with 'REPLACE'

Any time you see `\` in front of a character, it indicates the character is being escaped (which means we're literally looking for it within the string).  The `\[[^]]*\]` sequence is saying replace anything inbetween brackets `[ ]` including the brackets.

Now our strings should look like this: 
```bash
Aug  8 12:34:26 [ssh] Ban 111.222.12.100
Aug  8 12:34:26 [hass-iptables] Ban 111.222.12.100
```

Next thing we can do is get rid of the brackets around the ban identifiers `ssh` and `hass-iptables`:

```bash
sed -i 's/\[//g;s/\]//g' <FILE>
```

The final thing is removing any pesky double-spaces via `sed -i 's/  / /g'`.  The reason for this will become clear when we get to the python step.  Ultimately, we can combine the above steps into a one-line expression:
```bash
sed -i 's/raspberrypi fail2ban\.actions\[[^]]*\]: WARNING//g;s/\[//g;s/\]//g;s/  / /g' /home/hass/.homeassistant/ip_ban_list.log
```

### Convert File to json

Now we can use a small python script to take that log file and turn it into a json file that can be used with the file sensor in Home Assistant.  Create a file called `read_ban_list.py` in your `.homeassistant/bin` directory.  In it, paste the following code:

```python
'''
Author: Kevin Fronczak
https://kevinfronczak.com

Reads a ban list assuming the following structure:
[Month] [Day] [HH:MM:SS] [iptable] [Type=Ban/Unban] [ipAddress]
'''
import sys
import json

FILE = sys.argv[1]
JSON_FILE = sys.argv[2]

DATA = {'ssh': [], 'hassiptables': []}

''' Read file '''
with open(FILE) as fh:
  banlist = fh.readlines()

''' Get Banned IPs '''
for line in banlist:
  line_split = line.split(' ')
  ban_type = ''.join(line_split[3].split('-'))
  ban_ip = line_split[5].strip()
  if ban_type not in DATA.keys() and line_split[4] == 'Ban':
    DATA[ban_type] = list()
  if ban_ip in DATA[ban_type] and line_split[4] == 'Unban':
    DATA[ban_type].remove(ban_ip)
  else:
    DATA[ban_type].append(ban_ip)

''' Replace empty ban list with "None" '''
for key, value in DATA.items():
    if not value:
        DATA[key] = "None"
    else:
        DATA[key] = ','.join(value)

''' Write to JSON file for HASS processing '''
with open(JSON_FILE, 'w') as fp:
    json.dump(DATA, fp)
```

Now, back in your `gen_ban_list.sh` script, add the following entry:

```bash
python3 /home/hass/.homeassistant/bin/read_ban_list.py '/home/hass/.homeassistant/ip_ban_list.log' '/home/hass/.homeassistant/ip_ban_list.json'
```

Finally, we need to remove the `ip_ban_list.log` file:

```bash
rm /home/hass/.homeassistant/ip_ban_list.log
```

### Putting it All Together

Your final `gen_ban_list.sh` script should look like the following:

```bash
more /var/log/syslog | grep fail2ban | grep WARNING > /home/hass/.homeassistant/ip_ban_list.log
sed -i 's/raspberrypi fail2ban\.actions\[[^]]*\]: WARNING//g;s/\[//g;s/\]//g;s/  / /g' /home/hass/.homeassistant/ip_ban_list.log
python3 /home/hass/.homeassistant/bin/read_ban_list.py '/home/hass/.homeassistant/ip_ban_list.log' '/home/hass/.homeassistant/ip_ban_list.json'
rm /home/hass/.homeassistant/ip_ban_list.log
```

### Creating the Command Line sensor

Now that we have our command, we can create the command-line sensor.  In your homeassistant `configuration.yaml` you need to add the following entry:

```yaml
sensor:
  - platform: command_line
    name: ip_ban
    command: bash /home/hass/.homeassistant/bin/gen_ban_list.sh
    scan_interval: 120
```

This will run the `gen_ban_list.sh` script every two minutes.

## File Sensor

The reason we went through all of the trouble in processing the `syslog` file and dumping to json, was to make this step very easy (and very scalable).  The way everything has been set up allows for an arbitrary number of file sensor entries that every command and script will be able to use (i.e. this method is not exclusive to SSH and hass-iptable bans!).

Add the following entries to your `configuration.yaml` to create `sensor.ssh_bans` and `sensor.hass_bans`:

```yaml
sensor:
  - platform: file
    file_path: /home/hass/.homeassistant/ip_ban_list.json
    name: SSH Bans
    value_template: '{{ value_json.ssh }}'
  - platform: file
    file_path: /home/hass/.homeassistant/ip_ban_list.json
    name: Hass Bans
    value_template: '{{ value_json.hassiptables }}'
```

## Notifications

Finally, to receive a notification whenever an IP has been banned, you can add the following automation which will tell you the type of ban (ssh/hass) as well as the IP or IPs that were banned and the timestamp.

```yaml
alias: Notify on Failed Login
trigger:
  - platform: state
    entity_id: sensor.ssh_bans
  - platform: state
    entity_id: sensor.hass_bans
condition:
  condition: or
  conditions:
    - condition: template
      value_template: '{{ states.sensor.ssh_bans.state != "None" }}'
    - condition: template
      value_template: '{{ states.sensor.hass_bans.state != "None" }}'
action:
  - service: notify.notify
    data_template:
      message: >
      Failed Login! {{ now().strftime("%h %d, %Y at %H:%M:%S") }}
      {% if states.sensor.ssh_bans.state != "None" %}
        SSH Attempt(s) from {{states.sensor.ssh_bans.state}}
      {% endif %}
      {% if states.sensor.hass_bans.state != "None" %}
        Web Attempt(s) from {{states.sensor.hass_bans.state}}
      {% endif %}
```

# Final Thoughts

Perhaps there's a cleaner way to implement this (such as using the command line sensor only) but this is working reliably for me and is relatively easy to maintain.  My actual implementation differs somewhat from what I've listed, but you can check it out on my [GitHub Page](https://github.com/fronzbot/githass) where I have my whole Home Assistant configuration.





