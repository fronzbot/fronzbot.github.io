---
layout: post
title: Low-Power Op-Amp
date: 2013-01-02 21:51
description: Low Power Operation Amplifier design for a graduate-level university class
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - university project
  - theory
  - circuits
use_math: false
project: true
feature: false
---
For my Analog Design class, each student was tasked with designing an OpAmp in 0.5um technology with the following specifications:

*   Open-loop gain of at least 3000 V/V
*   Unity-gain Bandwidth of at least 20 MHz
*   Phase Margin of at least 50°
*   Slew-rate of at least 3 V/us
*   Output voltage swing within 500mV of each rail
*   ICMR that include one of the rails
*   PSRR of -60dB at 60Hz and -40dB at 1 MHz

In addition, each student had to select an optional specification.  I chose low quiescent power whose specification was to be below 200 uW.  Each spec had to be run over corners which varied the supply voltages, MOSFET process, and temperature.  In all there were 45 different corners. My final paper can be found [here]({{ site.url }}{{ site.doc_path }}/Fronczak_EE610_Final_Paper.pdf).  The physical layout was just a  quick overview of the floorplan and not a final design. Overall, the opamp performed fairly well.  The only spec that I completely missed was the unity-gain bandwidth (as the compliance table below shows).  This is due to the nature of the architecture in that by using a Folded-Cascode, I decrease the pole location with a decrease in current (since the output impedance is inversely related to current).  Since I needed a low-quiescent design and couldn't _quite_ get any dynamic biasing scheme working, I had to keep the current very low to achieve a balance between power, gain, and phase margin.  This required me to sacrifice bandwidth, unfortunately.  Other than that, any other spec I missed was just by a small margin and could easily be rectified with a bit more tuning.  Eventually I just got to the point where I needed to stop tuning and start recording results (since it is quite time consuming to fiddle with a parameter, run corners simulation, and analyze results over and over again).  I was happy with what my amplifier produced so I stuck with it. Below are various plot corresponding to each spec.

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/circuit.png)]({{ site.url }}{{ site.image_path }}/circuit.png) Opamp Architecture 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/open_loop_gain_BW.png)]({{ site.url }}{{ site.image_path }}/open_loop_gain_BW.png) Open Loop Gain and Bandwidth 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/open_loop_phase_margin.png)]({{ site.url }}{{ site.image_path }}/EE610/open_loop_phase_margin.png) Open Loop Phase Margin 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/power_consumption.png)]({{ site.url }}{{ site.image_path }}/power_consumption.png) Power Consumption 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/PSRR_VCC.png)]({{ site.url }}{{ site.image_path }}/PSRR_VCC.png) PSRR on VCC 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/PSRR_VSS.png)]({{ site.url }}{{ site.image_path }}/PSRR_VSS.png) PSRR on VSS 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/slew_rate.png)]({{ site.url }}{{ site.image_path }}/slew_rate.png) Slew Rate 

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/voltage_swing.png)]({{ site.url }}{{ site.image_path }}/voltage_swing.png) Large Signal Voltage Swing