---
layout: post
title: 'Using an UnRaid Share as Your Linux Home Directory'
date: 2018-10-10 12:17
description: How to change your linux home directory to map to an UnRaid share
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - unraid
  - server
  - linux
use_math: false   # Does this page have LaTeX elements?
project: false    # Is this a project post?
feature: false    # If a project, should this be featured at the top of the project page?
---

One of my favorite parts about [UnRaid](https://unraid.net) is the seamless ability to create virtual machines.  I like to do most of my work on Linux and having a VM allows me to try different distros and easily manage resource use.  In order to easily do this, though, I need to have my `/home` directory persist across multiple installs.  To manage this, I create a share on UnRaid which is then mounted at boot as my home directory within a VM.  Here is my process.

# Move your `home` directory to a share

Assuming you have already created an UnRaid user share where you're going to store your home directory (and I *highly* recommend using your cache drive for this share), you need to first move any files on your linux install to the server.  If you're installing linux for the first time (ie. nothing important exists in your `home` directory, you can skip this step).

First, we'll create a temporary mounting point for the share (make sure the `cifs-utils` package is installed.  With a Debian-based distro you can use the command `sudo apt-get install cifs-utils`).  We'll assume the username is `john` and the share you created is called `john_home`.

```bash
sudo mkdir /mnt/tmp
sudo mount -t cifs -o guest //servername/john_home /mnt/tmp
```

> If you get an error with the previous command, you can use your server's IP address in place of `servername` or edit your `/etc/hosts` file.  I prefer doing the latter, and all you need to do is add an entry to `/etc/hosts` with the format `<ip address> <name>` (editing the file with `sudo`).  So if my server was called `servername` and had an IP address of `192.168.0.77` I'd add the following to `/etc/hosts`:
> 
> ```bash
> 192.168.0.77   servername
> ```
> 
> Now you can re-run the previous `mount` command

We can then copy our home directory over to this temporary mount point and, once it completes, ensure that our files are actually there.

```bash
sudo rsync -avx /home/john /mnt/tmp
ls -lah /mnt/tmp
```

Finally, we can unmount the share with

```bash
sudo umount /mnt/tmp
```

# Test mount user share as home directory

Before we permanently mount a share as our home directory, we should back up our current home and test it out.  We'll first move our home directoy to a backup location and then mount the share as our home and verify everything is there and working.

```bash
sudo mv /home/john /home/john_bak
sudo mkdir /home/john
sudo mount -t cifs -o guest,uid=$(id -u),gid=$(id -g),mfsymlinks //servername/john_home /home/john
ls -lah /home/john
```
Assuming everything is working properly, we can move on to editing the `fstab` entry to make this change permanent.

> **Note:** if you have any git repos in your home directory, you'll want to push any changes in them to a remote repo prior to performing the next step.  In my experience, the git history gets all messed up and thinks the existing files are all new.  I just pushed any changed to a github branch and then re-cloned after I was finished.

# Permanently mount share as linux home

Finally we can permanently make the unraid share our linux home by editing `fstab`.  Use whatever editor you like (I prefer `vim` to make the change as `sudo`):

```bash
sudo vim /etc/fstab
``` 

And then append the following line:

```bash
//servername/john_home  /home/john  cifs  guest,uid=john,gid=john,mfsymlinks   0   0
```

You can now restart your VM and you home directory should automatically mount.

# Future linux installs

If you ever want to install a new VM, you can use the following commands to quickly map your home directory without performing any tests in the future:

```bash
sudo vim /etc/hosts
  # Inside /etc/hosts
  <ip-address>  servername
sudo apt-get install cifs-utils
sudo mv /home/username /home/username_bak
sudo vim /etc/fstab
  # Inside /etc/fstab
  //servername/usershare /home/username  cifs  guest,uid=username,gid-username,mfsymlinks  0 0
sudo reboot
```

# Why bother?
One major reason I want to do this is so I can minimize the vdisk size for my VMs since a bulk of space is spent in my home directory.  This way I can use as much space as I want AND back my home directory up with a tool like [Duplicati](https://duplicati.com).  It also allows me to easily migrate between different linux distros, which is nice.

Anyways, I hope this helped someone else out there!
 
