---
layout: post
title: Sub-threshold Conduction in MOSFETs
date: 2013-02-06 22:07:05.000000000 -05:00
description: Subthreshold research paper for a graduate university class
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - university project
  - theory
  - device physics
use_math: false
project: true
feature: false
---

For a recent class I was taking, entitled "Advanced Field-Effect Devices", we were tasked with choosing a specific topic pertaining to MOSFET theory, performing an extensive literature search, and then writing a paper on our findings.  My topic, as evidenced by the title of this post, was on [sub-threshold conduction]({{ site.url }}{{ site.doc_path }}/Analysis_of_Subthreshold_Conduction_in_MOSFETs_Fronczak.pdf). I would consider myself an "analog guy", so I was kind of drawn to sub-threshold conduction from the start.  It's a really interesting topic because, classically, the device is off... but realistically, it's not.  There is a certain amount of leakage and, as it turns out, it's actually a really efficient operating region for analog circuits since the ratio of transconductance to current is very high. In my paper, which [you can download to read here (pdf warning)]({{ site.url }}{{ site.doc_path }}/Analysis_of_Subthreshold_Conduction_in_MOSFETs_Fronczak.pdf),  I covered threshold voltage shifting, drain-induced barrier lowering, and multi-gate devices.  There are a _lot_ of areas I ignored just for the sake of time, but otherwise the paper would easily have reached triple its current length.  Still, if you're interested in this subject I highly recommend at least skipping to the list of references in my paper ([linked here, again]({{ site.url }}{{ site.doc_path }}/Analysis_of_Subthreshold_Conduction_in_MOSFETs_Fronczak.pdf)) as they were the ones (of about the 30 or so I read) that I felt really presented the material well to allow for a solid understanding of various sub-threshold mechanisms. Below is a copy-paste of my Abstract, for convenience.  If you do read my paper, I hope you enjoy it!

## **Abstract**

Sub-threshold conduction is an important consideration when dealing with modern devices, especially due to the trend towards increasingly smaller device sizes. Shorter channels have adverse effects on sub-threshold swing, affecting device operation in this region. Analog designers would like a smooth and accurate model in order to properly utilize this highly efficient operating region, while digital designers would prefer to understand methods to minimize channel conduction when a device is sub-threshold. This paper will review previously published works that discuss analytic models for different sub-threshold concerns, including short-channel effects and the effects due to barrier-lowering. Experimental data is also presented which verifies some of these selected models. Finally, areas for further research into this operating region will be presented.  

[Analysis of Sub-Threshold Conduction in MOSFETs - Kevin Fronczak - 2013]({{ site.url }}{{ site.doc_path }}/Analysis_of_Subthreshold_Conduction_in_MOSFETs_Fronczak.pdf)