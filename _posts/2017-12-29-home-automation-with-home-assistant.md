---
layout: post
title: 'Home Automation with Home Assistant'
date: 2017-12-29 09:00
description: How I automate my house using home assistant
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - home automation
  - server
  - projects
use_math: false   # Does this page have LaTeX elements?
project: true     # Is this a project post?
feature: true    # If a project, should this be featured at the top of the project page?
feature_image: /assets/images/feature/hass.png   # Used if this is a feature project
---

Ever since my wife and I purchased our first home in 2014, I've been obsessed with home automation.  I started with a few GE Link lightbulbs connected to a [Wink Hub](https://wink.com) and pre-ordered an Amazon Echo with the hunch that they would eventually add in functionality to control my Wink Hub vias voice (they did!).  But I wasn't satisfied.  I could control my lights remotely and with my voice, I could even set up basic automation routines with Wink... but it was _slow_.  Each action had to be communicated to Wink's servers and then back to my lights.  On top of that, I was at the mercy of both my internet as well as Wink's servers: I had at least one run-in where my house was no longer automated because of a server problem on Wink's end.

This was _no bueno_.

So I started searching for alternatives.  My primary goals were the following:

- Local control (no external server communication)
- Some sort of presence detection for automations
- Low entry cost

Eventually, I found that solution in [Home Assistant](https://home-assistant.io).  Before I dive into everything, I should mention that I keep my home assistant configuration up-to-date on [my github page](https://github.com/fronzbot/githass) if you're interested in checking it out.

## Starting with Home Assistant

My first working configuration for home assistant was in July of 2016 with version 0.24.  Here I still had all of my lights routed through Wink, so I had not yet gotten to local control, but my automations were set up.  I installed [Home Assistant](https://home-assistant.io) on a Raspberry Pi 3 and had it hard-wired to my router.  Given that I already owned one, the entry cost for this setup was **$0.00**, not including the time I had to set it up.  Regardless, this met my "Low entry cost" criteria.

One of the first things I included was [nmap](https://home-assistant.io/components/device_tracker.nmap_tracker/)-based presence detection to check if either my wife or myself were home and turned lights on/off based on that.  Given that my old configurations are...well...old, I'm not going to post the raw `yaml` here since it likely does not apply to current versions of Home Assistant.  Instead, I'll show you my pseudo-code.  Below is an early automation example for turning my lights off when we leave for work:

```python
if group.all_devices is 'not_home':
    if time between '7:30:00' and '10:00:00' and day is not weekend:
        service.turn_off_all_lights()
```

Pretty straight-forward and easy to implement (not so easy with Wink at the time).  So this met my second criteria of "Presence-based automation".  Great!  Now only thing I'm missing is local control, which Home Assistant will allow me, provided I have the correct equipment.

## Phillips Hue with Home Assistant

Now, here my cost increased.  I purchased a [Phillips Hue](https://www2.meethue.com) hub and three 2nd-generation color bulbs which ran me around **$140** thanks to a sale.  However, I viewed this as a win since the Hue hub did not require a server connection to work which would help me eliminate the Wink hub from my setup and achieve my goal of local-only control.  Plus, with the color lights, I could do cool stuff during the holidays like this:

{: .center}
![Hue Christmas Lights]({{site.url}}{{site.image_path}}/hass/hue-xmas-pano.jpg)

There was another cool thing I could do with the Phillips Hue lights: color temperature modulation similar to the computer program [f.lux](https://justgetflux.com).  During the day I can set the Hue bulbs to a whitish-blue color to simulate daylight and then, during night, I can make the color more warm to help maintain my family's [Circadian Rhythm](https://en.wikipedia.org/wiki/Circadian_rhythm).  Originally, I used the the built-in [flux](https://home-assistant.io/components/switch.flux/) component for Home Assistant, but ran into a few problems.  Some of these issues may not exist anymore, but they did _at the time_ and I needed to fix it:

- Simple linear interpolation from sunrise to sunset is a poor approximation
- Lights turned on after midnight were daytime color (yikes)
- Updated way too frequently and caused some race conditions (turning light off during an update would prevent me from turning them off)

Ultimately, I could refactor the flux component myself, or implement something on my own.  I chose the latter by using [AppDaemon](https://github.com/home-assistant/appdaemon).  The logic is pretty simple, and my implementation can be [found here](https://github.com/fronzbot/githass/blob/master/apps/flux.py).  I have a time-lapse showing it working below.  Every hue light in my house utilizes this component, and I have flux "zones" so I can do different things with different lights without affecting certain rooms (I'll get to that in a bit).

{: .center}
![Flux Lights]({{site.url}}{{site.image_path}}/hass/flux-lights.gif)

## Media

In addition to flux lights, I also wanted to change lights depending on media.  My initial implementation was simple: using the [Emulated Hue](https://home-assistant.io/components/emulated_hue) component, I could simply say:

> Alexa/Hey Google, turn on Movie Mode

which would then activate my scene called "Movie Mode", defined below.

```yaml
name: Movie Mode
entities:
  input_boolean.flux_living_room:
    state: off
  light.couch_left:
    state: on
    color_temp: 500
    brightness: 50
  light.couch_right:
    state: on
    color_temp: 500
    brightness: 50
  light.corner:
    state: on
    color_temp: 500
    brightness: 50
```

This simply turns off the flux component and then dims the lights (see the example below).  Now, I mentioned that I had different flux groups and here's why: if I'm watching a movie in my basement (like in the gif below) I don't want to stop updating the color temperature elsewhere in the house.  So here, I am able to turn off flux _for only the lights I'm dimming_ which means the rest of my house is unaffected.  This has been very useful.

{: .center}
![Movie Mode]({{site.url}}{{site.image_path}}/hass/movie-mode.gif)

# Automating Movie Mode

Now, I already had [Plex](https://plex.tv) in Home Assistant so I could monitor various things that were playing. This allowed me to add an automation to check if a movie is playng via Plex on my [NVidia Shield TV](https://nvidia.com/en-us/shield/) and then automatically activate my "Movie Mode" scene.  The first step I took (although, technically it is unneccesary) was to create a template sensor called **media** that I could use within my automation:

```yaml
- platform: template
  sensors:
    media_type:
      value_template: >
        {% if states.media_player.shield_android_tv.attributes %}
          {{ states.media_player.shield_android_tv.attributes.media_library_name }}
        {% else %}
          None
        {% endif %}
    media_title:
      value_template: >
        {% if states.media_player.shield_android_tv.attributes %}
          {{ states.media_player.shield_android_tv.attributes.media_title }}
        {% else %}
          None
        {% endif %}
    media_state:
      value_template: >
        {% if states.media_player.shield_android_tv.state %}
          {{ states.media_player.shield_android_tv.state }}
        {% else %}
          None
        {% endif %}
```  

Now, this provided me with the following information:

- `sensor.media_type` tells me which library I'm playing my Media from (TV Shows, Movies, etc)
- `sensor.media_state` tells me if the media is `playing` or `paused`
- `sensor.media_title` tells me the title of the media... this will be handy in a bit

Next, I needed an automation to trigger some script (using Home Assistant's [python scripts](https://home-assistant.io/components/python_script/)).  Essentially, I wanted to call this script whenever the media changes from `playing` to `paused` and vice versa.  I also wanted to make sure it only changed when we were home (in case we have a babysitter... don't want to freak them out with color changing lights).  I settled on the following automation:

```yaml
alias: Movie Colors
trigger:
  - platform: state
    entity_id: sensor.media_state
condition:
  condition: and
  conditions:
    - condition: state
      entity_id: sensor.occupancy
      state: 'home'
action:
  - service: python_script.media_engine
```  

So now it was time to create the script that acts on this information.  As mentioned, I decided to use Home Assistant's [python scripts](https://home-assistant.io/components/python_script/) which allows me to use much cleaner syntax than `yaml` would provide.  The gist is that when a movie is playing, I want to turn on my Movie Mode, but when the media is paused, I should re-enable flux.

Easy enough.

But what I also realized would be _cool_ was to check exactly _what_ movie was playing and change the color based on that.  There are many implementations out there that change colors _while_ the movie is playing, but I just wanted a nice static color (specifically for kids movies for my daugther's sake).  So I created [a bunch of scenes](https://github.com/fronzbot/githass/tree/master/scenes) for different colors.  Inside my python script, I have a simple dictionary of movie titles and colors I want to display when the movie is playing.  For example, below is what happens when I play [Finding Nemo](https://imdb.com/title/tt0266543/).

{: .center}
![Finding Nemo]({{site.url}}{{site.image_path}}/hass/finding-nemo.jpg)

And, the brains of the script:

```python
# Set color in living room based on what's playing on Plex

movie_color_mapping = {
    'Beauty and the Beast (1992)': 'yellow',
    'A Christmas Story (1983)': 'christmas',
    'Finding Nemo (2003)': 'blue',
    'Frozen (2013)': 'cyan',
    'Halloweentown (1998)': 'orange',
    'The Lion King (1994)': 'orange',
    'The Martian (2015)': 'orange',
    'Monsters, Inc. (2001)': 'purple',
    'Tangled (2010)': 'green',
    'Up (2009)': 'pink',
    'Moana (2016)': 'cyan',
    'WALL-E (2008)': 'orange'
}

media_title = hass.states.get('sensor.media_title').state 
media_type = hass.states.get('sensor.media_type').state
media_status = hass.states.get('sensor.media_state').state

if media_type == 'Movies' and media_status == 'playing':
    hass.services.call('input_boolean', 'turn_off', {'entity_id': 'input_boolean.flux_living_room'})
    if media_title in movie_color_mapping.keys():
        color = movie_color_mapping[media_title]
        logger.warn('Using color {}'.format(color))
        hass.services.call('scene', 'turn_on', {'entity_id': 'scene.{}'.format(color)})
    else:
        hass.services.call('scene', 'turn_on', {'entity_id': 'scene.movie_mode'})
elif media_type == 'Movies' and media_status == 'paused':
    hass.services.call('input_boolean', 'turn_on', {'entity_id': 'input_boolean.flux_living_room'})
    hass.services.call('scene', 'turn_on', {'entity_id': 'scene.night'})
elif media_status == 'idle':
    hass.services.call('input_boolean', 'turn_on', {'entity_id': 'input_boolean.flux_living_room'})

```

Kid movies definitely feel the most appropriate for color changing, whereas the grown-up films are more suited for the light-dimming.  Though having our living room bathed in a reddish-orange glow when [The Martian](https://imdb.com/title/tt3659388/) is playing is pretty awesome.

# Next Title



