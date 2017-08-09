---
layout: post
title: 'MySQL with Home Assistant'
date: 2017-08-10 09:00
description: Using MySQL with Home Assitant and fixing things
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - home automation
use_math: false
project: false
feature: false
---

Recently I decided to mess around with my [Home Assistant ](https://home-assistant.io) setup and accidentally borked my MySQL installation on my Raspberry Pi 3.  Getting it up and running again was a bit of a pain, so I decided to write a post on the exact steps I took in the hopes that someone will find it useful.

# Why MySQL?
By default, the database created by Home Assistant is an SQLite database.  For most people this is probably ok, but [my Home Assistant configuration](https://github.com/fronzbot/githass) began to grow and I found that the SQLite database just wasn't cutting it (too slow, for starters).  So I opted for MySQL.

# Deleting an old MySQL installation

If you're starting fresh on a new Pi, you can skip these steps.  However, if you're like me and messed up your MySQL installation, here's how you can fix it (note, this *will* delete any old databases, so use this method with caution).

First, let's make sure Home Assistant isn't running and stop any mysql processes:

```bash
$ sudo systemctl stop home-assistant.service
$ sudo service mysql stop
$ sudo killall -9 mysql
$ sudo killall -9 mysqld
```

Now, we need to completely remove mysql via the following steps.  First, run `sudo dpkg --purge mysql` and hit tab; there should be multiple entries.  Run that command for each `mysql-*` entry (I ran into a few that errored and was able to safely skip them).

```bash
$ sudo apt-get remove --purge mysql-server mysql-client mysql-common
$ sudo apt-get autoremove
$ sudo apt-get autoclean
$ sudo deluser mysql
```

I also found that I needed to get rid of the following directories which contain the database, so use with caution:

```bash
$ sudo rm -rf /var/lib/mysql
$ sudo rm -rf /etc/mysql
```

Now, let's make sure it's really dead by running `which mysql`.  It should return nothing if the removal was successful.  The last command we need to run is:

```bash
$ sudo dpkg --configure -a
```

Which will regenerate the dpkg info.

# Installing MySQL on Raspberry Pi

These instructions were originally found [here](https://community.home-assistant.io/t/large-homeassistant-database-files/4201/71).  I'm reproducing them for the sake of completeness.

First, let's make sure everything is up to date by running:

```bash
$ sudo apt-get update
```

Now we can install:

```bash
$ sudo apt-get install libmysqlclient-dev
$ sudo apt-get install python-dev python3-dev
```

# Create MySQL Database for Home Assistant

Now we can create our MySQL database for Home Assistant.  Open mysql via the `mysql -u root -p` command.  Then run the following commands within mysql:

```
mysql> CREATE DATABASE hass_db;
mysql> CREATE USER 'hassuser'@'localhost' IDENTIFIED BY '<YOURPASSWORD>';
mysql> GRANT ALL PRIVILEGES ON hass_db.* TO 'hassuser'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> quit
```

Next, assuming you're using a virtual-env, we need to switch to our venv and make sure mysqlclient is up-to-date:

```bash
$ sudo su -s /bin/bash hass
$ source /srv/hass/hass_venv/bin/activate
$ pip3 install --upgrade mysqlclient
$ deactivate
```

Hit Ctrl+d to return to your default user.

# Change Home Assistant Recorder to use MySQL

The last step is to add the `recorder` component into our `configuration.yaml` file so that Home Assistant knows it should be using the MySQL database instead of SQLite:

```yaml
recorder:
  db_url: mysql://hassuser:<YOURPASSWORD>@localhost/hass_db
```

And now it's safe to restart Home Assistant via `sudo systemctl restart home-assistant.service`

And that's it!  That's how you can use MySQL with Home Assistant and fix any mishaps that might happen with your installation if you start wildly screwing around with it.
