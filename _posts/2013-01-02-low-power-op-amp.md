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
<ul>
<li>Open-loop gain of at least 3000 V/V</li>
<li>Unity-gain Bandwidth of at least 20 MHz</li>
<li>Phase Margin of at least 50°<b>
</b></li>
<li>Slew-rate of at least 3 V/us</li>
<li>Output voltage swing within 500mV of each rail</li>
<li>ICMR that include one of the rails</li>
<li>PSRR of -60dB at 60Hz and -40dB at 1 MHz</li>
</ul>
In addition, each student had to select an optional specification.  I chose low quiescent power whose specification was to be below 200 uW.  Each spec had to be run over corners which varied the supply voltages, MOSFET process, and temperature.  In all there were 45 different corners.
My final paper can be found <a href="http://kevinfronczak.com/documents/EE610/Fronczak_EE610_Final_Paper.pdf" target="_blank">here</a>.  The physical layout was just a  quick overview of the floorplan and not a final design.
Overall, the opamp performed fairly well.  The only spec that I completely missed was the unity-gain bandwidth (as the compliance table below shows).  This is due to the nature of the architecture in that by using a Folded-Cascode, I decrease the pole location with a decrease in current (since the output impedance is inversely related to current).  Since I needed a low-quiescent design and couldn't <em>quite</em> get any dynamic biasing scheme working, I had to keep the current very low to achieve a balance between power, gain, and phase margin.  This required me to sacrifice bandwidth, unfortunately.  Other than that, any other spec I missed was just by a small margin and could easily be rectified with a bit more tuning.  Eventually I just got to the point where I needed to stop tuning and start recording results (since it is quite time consuming to fiddle with a parameter, run corners simulation, and analyze results over and over again).  I was happy with what my amplifier produced so I stuck with it.
Below are various plot corresponding to each spec as well as my architecture.  In the compliance table, specs in red text indicate that it missed the target.
<table width="420" border="1" cellspacing="0" cellpadding="0" align="right">
<tbody>
<tr>
<td valign="top" width="68"><b>Param</b></td>
<td valign="top" width="158">
<p align="center"><b>Spec</b>
</td>
<td valign="top" width="122">
<p align="center"><b>Value</b>
</td>
<td valign="top" width="74">
<p align="center"><b>Corner</b>
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>Gain</b>
</td>
<td valign="top" width="158">
<p align="center">70 dB
</td>
<td valign="top" width="122">
<p align="center">70.2 dB
</td>
<td valign="top" width="74">
<p align="center">NPtv
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>UGB</b>
</td>
<td valign="top" width="158">
<p align="center">20 MHz
</td>
<td valign="top" width="122">
<p align="center"><span style="color: #ff0000;">500 kHz</span>
</td>
<td valign="top" width="74">
<p align="center"><span style="color: #ff0000;">npTv</span>
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>PM</b>
</td>
<td valign="top" width="158">
<p align="center">50°
</td>
<td valign="top" width="122">
<p align="center">55.3°
</td>
<td valign="top" width="74">
<p align="center">NPtV
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>SR</b>
</td>
<td valign="top" width="158">
<p align="center">3 V/µs
</td>
<td valign="top" width="122">
<p align="center"><span style="color: #ff0000;">2.27 V/µs (+)</span>
<p align="center">3.00 V/µs (-)
</td>
<td valign="top" width="74">
<p align="center"><span style="color: #ff0000;">npTv</span>
<p align="center">NPtV
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>Swing</b>
</td>
<td valign="top" width="158">
<p align="center">500mV from VDD
<p align="center">500mV from VSS
</td>
<td valign="top" width="122">
<p align="center">314 mV
<p align="center"><span style="color: #ff0000;">554 mV</span>
</td>
<td valign="top" width="74">
<p align="center">NPTv
<p align="center"><span style="color: #ff0000;">abTV</span>
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>PSRR</b>
</td>
<td valign="top" width="158">
<p align="center">-60 dB at 60 Hz
<p align="center">-40 dB at 1 MHz
</td>
<td valign="top" width="122">
<p align="center"><span style="color: #ff0000;">-50.5 dB</span>
<p align="center">-40.35 dB
</td>
<td valign="top" width="74">
<p align="center"><span style="color: #ff0000;">NPcV</span>
<p align="center">nPTV
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>CMIR</b>
</td>
<td valign="top" width="158">
<p align="center">0-VDD or VSS-0
</td>
<td valign="top" width="122">
<p align="center">0 to VDD
</td>
<td valign="top" width="74">
<p align="center">-
</td>
</tr>
<tr>
<td valign="top" width="68">
<p align="center"><b>Power</b>
</td>
<td valign="top" width="158">
<p align="center">200 µW
</td>
<td valign="top" width="122">
<p align="center"><span style="color: #ff0000;">209 µW</span>
</td>
<td valign="top" width="74">
<p align="center"><span style="color: #ff0000;">NPTV</span>
</td>
</tr>
</tbody>
</table>
&nbsp;
&nbsp;
<a href="http://kevinfronczak.com/documents/EE610/circuit.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/circuit.png" /></a>
Opamp Architecture
<a href="http://kevinfronczak.com/documents/EE610/open_loop_gain_BW.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/open_loop_gain_BW.png" /></a>
Open Loop Gain and Bandwidth
<a href="http://kevinfronczak.com/documents/EE610/open_loop_phase_margin.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/open_loop_phase_margin.png" /></a>
Open Loop Phase Margin
<a href="http://kevinfronczak.com/documents/EE610/power_consumption.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/power_consumption.png" /></a>
Power Consumption
<a href="http://kevinfronczak.com/documents/EE610/PSRR_VCC.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/PSRR_VCC.png" /></a>
PSRR on VCC
<a href="http://kevinfronczak.com/documents/EE610/PSRR_VSS.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/PSRR_VSS.png" /></a>
PSRR on VSS
<a href="http://kevinfronczak.com/documents/EE610slew_rate.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/slew_rate.png" /></a>
Slew Rate
<a href="http://kevinfronczak.com/documents/EE610/voltage_swing.png"><img alt="{{site.baseurl}}" src="{{ site.baseurl }}/assets/voltage_swing.png" /></a>
Large Signal Voltage Swing
