---
layout: post
title: Levitation Clock
date: 2013-12-17 06:00
description: Senior Design project for University
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - university project
use_math: false
project: true
feature: true
feature_image: /assets/images/features/levitation-clock.jpg
---

I've been meaning to post this for awhile, but better late than never I guess. For my senior design project in college, myself and two buddies of mine, Trong and Holden, (all of us nearly done with our Master's degrees at the time) decided to build a clock... but no ordinary clock, no. We wanted to build a clock that used magnetic levitation to tell time. Our final implementation was VASTLY different from our original, but we were incredibly happy with how it turned out:
<a href="http://kevinfronczak.com/documents/seniordesign/clock_poster_small.pdf">Clock Poster</a>
<a href="http://kevinfronczak.com/documents/seniordesign/P13321_Technical_Paper.pdf">Final Paper</a>
<a href="http://kevinfronczak.com/documents/seniordesign/levclock_presentation.pdf">Final Presentation</a>
http://www.youtube.com/watch?v=4bEvRd7E-bg
<strong>Design</strong>
Each object is a "bit" and tells time in a binary way (sort of).  You can tell what hour it is by counting the number of lines on the cylinders currently levitating (or realize that if the first and third objects are levitating that it corresponds to a binary 1010 which means it's 10 o'clock!).  I'll talk about the design process in the next few sections (and include our eagle files and arduino sketches), but you can find some more information in the <a href="http://kevinfronczak.com/documents/seniordesign/P13321_Technical_Paper.pdf">Final Paper</a> and <a href="http://kevinfronczak.com/documents/seniordesign/levclock_presentation.pdf">Presentation</a> I've linked.
<strong>User Interface</strong>
This was a very simple block: it just had three buttons and four seven-segment displays so that the user could set the time on the clock.  The main control board handled all the timing and it was sent via a custom data cable to this daughter board.
Files:
<a href="http://kevinfronczak.com/documents/seniordesign/Eagle/UserInterfaceBoard.sch">Eagle Schematic</a>
<a href="http://kevinfronczak.com/documents/seniordesign/Eagle/UserInterfaceBoard.brd">Eagle PCB Layout</a>
<a href="http://kevinfronczak.com/documents/seniordesign/UserInterface_PCBA.pdf">PCBA Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/UserInterface_BOM.pdf">BOM</a>
<a href="http://kevinfronczak.com/documents/seniordesign/UserInterface_PowerCable.pdf">Power Cable Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/UserInterface_DataCable.pdf">Data Cable Drawing</a>
<strong>Main Controller</strong>
This block was the brains of the operation.  For simplicity, we opted to use an arduino for prototyping and then we just inserted the pre-programmed chip into a 28-pin socket on the board.  We could have added in programming pins but decided to save the effort since there wouldn't be much need to program more than once.
The bulk of this board consisted of the MOSFETs used to drive the solenoids (each of which could draw around 750mA of current when on), the microcontoller, Buck Regulator, and RGB LED used to tell minutes.  The primary concern was that of driving the solenoids.  Given that one solenoid could be on for four hours at a time and that all four would be encased in, essentially, a wooden oven, we needed to run some temperature tests and also make sure that our drivers could properly dissipate the required amount of heat.
First, we ran a test to see what resistance our solenoid would saturate at as a function of time (positive temperature coefficient so more time equals more heat which equals more resistance which implies less levitation height).  We also ran a test to see what amount of levitation height we could coax out of it as a function of current.  Based on the following plots, we settled on a ~6 Ohm coil with 750 mA current draw.  As the video at the beginning of this post shows, this gave us enough levitation height for it to be discernible from a <em>non</em>-levitating object and allowed us to minimize power consumption to some degree.
<a href="http://kevinfronczak.com/documents/seniordesign/Solenoid_Temperature_Test_1200_turns.png" target="_blank"><img class="aligncenter" alt="Solenoid Resistance" src="{{ site.baseurl }}/assets/Solenoid_Temperature_Test_1200_turns.png" height="350" /></a>
<a href="http://kevinfronczak.com/documents/seniordesign/Solenoid_Levitation_Height_Test_1200_turns.png" target="_blank"><img class="aligncenter" alt="Levitation Height" src="{{ site.baseurl }}/assets/Solenoid_Levitation_Height_Test_1200_turns.png" height="350" /></a>
Next, I ran a script in MATLAB in order to determine the required heatsink thermal resistance at varying ambient temps and voltage levels.  For our design, we needed a roughly $$latex 2\frac{^{\circ}C}{W} $$ heatsink.
<a href="http://kevinfronczak.com/documents/seniordesign/Thermal_Resistance_Required_for_Regulator.png" target="_blank"><img class="aligncenter" alt="Thermal Resistance" src="{{ site.baseurl }}/assets/Thermal_Resistance_Required_for_Regulator.png" height="350" /></a>
While we're on the subject of temperature, we also ran a test while we were presenting at <a href="http://www.rit.edu/imagine/">Imagine RIT</a> in order to gauge what our ambient temperatures looked like as a function of time.  Now, this is kind of a useless test since we were running in "demo" mode (as shown in the video above) where we speed up time by 60x so that one "minute" passes by as one second.  However, it does give us some very valuable information in that we would NEVER want this running in normal operation without some kind of fan circulating air internally.  We saw roughly a 10C rise when one coil would only be on for a maximum of four minutes... just imagine four hours.  Yikes.  Holden and I ended up testing it over a 24-hour period in "normal" with a little 60mm computer fan blowing air through the gap at the bottom of the frame and we never saw the ambient increase above 50C so we should have done a MUCH better job analyzing internal heat generation compensation.
<a href="http://kevinfronczak.com/documents/seniordesign/Clock_ambient_versus_time.png" target="_blank"><img class="aligncenter" alt="Clock Ambient Temperature" src="{{ site.baseurl }}/assets/Clock_ambient_versus_time.png" height="350" /></a>
Files:
<a href="http://kevinfronczak.com/documents/seniordesign/Eagle/MainControlBoard.sch">Eagle Schematic</a>
<a href="http://kevinfronczak.com/documents/seniordesign/Eagle/MainControlBoard.brd">Eagle PCB Layout</a>
<a href="http://kevinfronczak.com/documents/seniordesign/SystemDesign.ino">Arduino Sketch</a>
<a href="http://kevinfronczak.com/documents/seniordesign/MainBoard_PCBA.pdf">PCBA Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/MainControlBoard_BOM.pdf">BOM</a>
<a href="http://kevinfronczak.com/documents/seniordesign/PowerCable.pdf">Power Cable Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/solenoid.pdf">Solenoid Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/solenoid_cable.pdf">Solenoid Cable Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/levobject.pdf">Levitating Object Drawing</a>
<strong>Frame Design</strong>
Our frame was designed by an awesome Industrial Designer we brought into the project named James.  A week after bringing him on, he bombarded us with <a href="http://edge.rit.edu/edge/P13321/public/MSD%20I/Concept%20Design/Concept%20Drawings">LOADS OF CONCEPTS</a>.  This made us really think about implementation more which is how we converged on the "binary" version of this clock.  James ended up designing a beautiful frame that we ended up paying a friend of Holden's named <a href="http://byronconn.com/">Byron Conn</a> to make (he's an awesome wood-wooker).
We basically just wanted a really beautiful and aesthetically pleasing frame in order to tie the whole project together, and BOY did James and Byron deliver!
<a href="http://kevinfronczak.com/documents/seniordesign/Clock_Front.jpg" target="_blank"><img class="aligncenter" alt="Clock" src="{{ site.baseurl }}/assets/Clock_Front.jpg" height="300" /></a>
Files:
<a href="http://kevinfronczak.com/documents/seniordesign/full_bom.pdf">Full Clock BOM</a>
<a href="http://kevinfronczak.com/documents/seniordesign/full_clock.pdf">Full Clock Drawing</a>
<a href="http://kevinfronczak.com/documents/seniordesign/frame_assembly_drawing.pdf">Frame Assembly Drawing</a>
<strong>Final Thoughts</strong>
Overall the project was rather simple from an electronics standpoint, but the design process from product definition up through the final stages was a very interesting experience.  There are many, many, things I think all of us would do differently if we were to tackle this project again but it was very useful to make some of the mistakes we did (the biggest one being that we ignored how to properly handle the ambient heat from the solenoids).
Anyways, at the end of the day I'm still really proud of this thing even if it's ultimately useless. It's just... <em>cool</em> which is all we ever wanted from this project to begin with.
