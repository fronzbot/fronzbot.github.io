---
layout: post
title: Stability Analysis of Boost Converters for ICs
date: 2013-09-12 10:10
description: Summary of my Master's thesis
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - university project
  - analog
  - theory
use_math: false
---

I recently completed my Master's Thesis entitled<a href="http://kevinfronczak.com/documents/Fronczak_Thesis.pdf"> "Stability Analysis of Switched DC-DC Boost Converters for Integrated Circuit" (August 2013)</a>. My defense slides can be found <a href="http://kevinfronczak.com/documents/Fronczak_Thesis_Defense.pdf">here</a>.
Here is the abstract:
<blockquote>Boost converters are very important circuits for modern devices, especially battery-operated integrated circuits. This type of converter allows for small voltages, such as those provided by a battery, to be converted into larger voltages more suitable for driving integrated circuits.
Two regions of operation are explored known as Continuous Conduction Mode and Discontinuous Conduction Mode. Each region is analyzed in terms of DC and small-signal performance. Control issues with each are compared and various error amplifier architectures explored. A method to optimize these amplifier architectures is also explored by means of Genetic Algorithms and Particle Swarm Optimization.
Finally, stability measurement techniques for boost converters are explored and compared in order to gauge the viability of each method. The Middlebrook Method for measuring stability and cross-correlation are explored here.</blockquote>
<a href="http://kevinfronczak.com/documents/Fronczak_Thesis.pdf">Thesis [PDF]</a>
<a href="http://kevinfronczak.com/documents/Fronczak_Thesis_Defense.pdf">Thesis Defense Slides [PDF]</a>
I will be writing another post on the Genetic Algorithm and PSO-based converter controller optimization techniques as I find it really interesting. I have that specific work on <a href="http://github.com/fronzbot/aidc">github</a> if you would like to browse the code in the meantime.
