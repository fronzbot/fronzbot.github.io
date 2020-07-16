---
layout: page
title: Resume
permalink: "/resume/"
navbar: true
---

Analog circuit designer with experience implementing low-noise and low-power sensor designs.
{: .resumeAlignCenter}

[Download PDF Version]({{ site.url }}/assets/docs/Fronczak_Resume.pdf "Resume")
{: .resumeAlignRight}

-----

# **PROFESSIONAL**

-----
**Staff Mixed Signal IC Design Engineer** <span style="color: gray">at</span> **Sony Electronics** <span style="color: gray">in</span> Rochester, NY <span style="color: gray">from</span> July 2018 to Present

- Involved in the Dynamic Frequency and Voltage Scaling (DFVS) power management architecture for next-gen stacked-chip CMOS image sensors in 40nm which involves frequent communication with worldwide cross-functional teams

- Led effort to introduce and implement a new low-jitter 600 MHz oscillator architecture with 8x power saving over existing PLL-based implementations, and also eliminating the need for external oscillator references

- Performed architecture study on potential LDO designs to use for next-generation ULP CMOS imaging products

- Architected and designed a 5-uW unconditionally-stable capacitorless-LDO supporting up to 10mA of load current

- Implemented an innovative scheme to handle undershoot during voltage-domain crossover

- Responsible for evaluating external delta-sigma-based temperature sensor IP for propagation within other business units

- Responsible for the design of circuits to interface with a pixel array for a stacked-chip low-power CMOS imaging product in 40nm. This work required generation of an accurate pixel model to gauge sensitivity to adjacent column coupling, as well as transient performance during image capture

- Used unique multiplexing scheme to be able to intelligently bin adjacent columns for power reduction during motion detection capture

- Specified testing scheme to ensure each multiplexer per column was void of defects with negligible contribution to total test time

-  Involved in the power management architecture for next generaon ultra low power image sensors, including
the design of a sub-uW LDO capable of supporng loads 1000x the quiescent current

- Responsible for the design of circuits to interface with a pixel array on a low-power CMOS imaging product. This work also involved generating detailed pixel models for simulations, as well as the study of power and area reduction techniques to improve product marketability and cost.


**Sr. Mixed Signal IC Design Engineer** <span style="color: gray">at</span> **Synaptics Inc** <span style="color: gray">in</span> Rochester, NY <span style="color: gray">from</span> Feb 2014 to July 2018
<br>

- Worked on architecture, design, and bring-up of a low-area, noise optimized continuous-time delta-sigma based AFE for capacitive fingerprint sensing in 55nm achieving 50% cost reduction over existing solutions

- Designed and implemented a a low-noise current conveyor with innovative mixing topology meant to improve SNR with minimal overhead

- Performed interference susceptibility analysis on existing and proposed architectures and designed an innovative a mitigation technique that took advantage of existing system design for improved performance

- Responsible for initial prototyping of fingerprint AFE architecture in silicon, prior to introduction into a part and led the effort to evaluate, track, and debug A0 silicon to enable rapid evaluation of needs for metal or all-layer spins

- Designed a noise-optimized discrete-time demodulator and filter for first market introduction of Touch and Display Driver Integrated Circuits (TDDI). Initial prototypes in 130nm, mass-produced parts in 55nm.

- Designed an innovative bandgap topology to enable a more efficient power management strategy for TDDI chips

- Led the introduction of a new 1Gbps MIPI DSI receiver architecture to the, utilizing continuous-time linear equalization, to replace existing solution and proposed an integrated offset calibration scheme

- Proposed, architected, and implemented a prototype sub-uW power management architecture for next-generation fingerprint sensors to aid in >30% power reduction over existing solutions. This involved brand-new designs for bias generation circuits, oscillators, and long sample-and-hold bandgap references (>1ms hold time)

- Designed a nW-level time-to-digital (TDC) temperature sensor capable of sub-1℃ resolution as measured in silicon

- Designed an innovative adaptive bias mechanism for POR circuits to enable fast reaction time while only taking up a few nW of total power budget

### Fingerprint Sensing
- Designed a small area, noise-optimized current-mode front-end which helped reduce die cost by nearly 50%
- Designed an innovative multi-level mixing topology to improve SNR
- Drove circuit and system implementation of a small area current-mode front-end in order to prove ability of the new technology to sense a fingerprint (stepping-stone for fingerprint sensor cost reduction)
- Led efforts to evaluate, track, and debug new silicon for any potential issues that could require a metal or all-layer revision, allowing for efficient evaluation of benefits/risks of a potential spin
- Designed a capacitive background cancellation circuit with sub-femtofarad resolution

### Touch Sensing
- Designed a small-area current-mode baseline correction circuit for TDDI (Touch and Display Driver IC) in order to reduce die cost and maintain competitive edge in TDDI market
- Designed switched capacitor demodulator and sample-and-hold circuitry for TDDI analog front-ends

### Low Power and Reference Circuits
- Architected and led the implementation of an experimental small area, nano-Amp reference architecture (current mirrors, oscillators, etc) with the goal of reducing standby power without sacrificing performance
- Designed a sub 1-V bandgap reference with innovative base-cancellation circuit for TDDI chips
- Aided in development of a top-level mixed-signal verification flow for capacitive fingerprint sensors, allowing teams to efficiently catch system-level bugs before tapeout

### Display Drivers
- Experience with MIPI DSI from transistor-level design through top-level verification and production test
- Experience designing high-voltage gate-line drivers

### General
- Experience working closely and effectively with multidisciplinary teams to ensure smooth silicon design and bring-up all the way through to production
- Have designed circuits in 130nm and 55nm technologies
- Very familiar and comfortable with Cadence design flow for IC design
- Experience using MATLAB for both system design and for testing of ASICs
- Focus on fundamental understanding of circuits for architectural comparisons is a strength (i.e. pencil-and-paper analysis)
- Attended a week-long Continuous-Time Delta Sigma Converter course held by MEAD (taught by Drs. Pavan, Schreier, and Hanumolu).

**Silicon Validation Contractor** <span style="color: gray">at</span> **Synaptics Inc** <span style="color: gray">in</span> Rochester, NY <span style="color: gray">from</span> Jun 2013 to Feb 2014
<br>
- Performed extensive validation on LDOs, VCOM drivers, LCD level shifters, and high-speed MIPI D-PHY architecture

**Analog Design Co-op** <span style="color: gray">at</span> **Intel Corporation** <span style="color: gray">in</span> Hudson, MA <span style="color: gray">from</span> Mar 2012 to Aug 2012
<br>
- Implemented a tool to extract on-chip decoupling capacitors to minimize off-chip capacitor size
- Implemented a tool to rapidly compare pad layout revisions to minimize errors due to manual inspection

-----

# **EDUCATION**

-----

**Rochester Institute of Technology** <span style="color: gray">in</span> Rochester, NY <span style="color: gray">from</span> Sep 2008 to Aug 2013
<br>
**Master of Science** and Bachelor of Science in **Electrical Engineering** <span style="color: gray">with a graduate</span> GPA <span style="color: gray">of</span> 4.0

Thesis: ***Stability Analysis of Switched DC-DC Boost Converters for Integrated Circuits***
- Investigated small-signal modeling and stability requirements for boost converters, as well as a variety of OTA-based controller topologies, in order to aid in the design and measurement of boost converter stability on an ASIC.  Also investigated use of genetic algorithms as a way to optimize controller design.

-----

# **PATENTS/PUBLICATIONS**

-----
- US 9,780,736 - Temperature compensated offset cancellation for high-speed amplifiers - Grant Oct. 3, 2017
- US 9,817,428 - Current-mode Bandgap Reference with Proportional to Absolute Temperature Current and Zero Temperature Current -Generation - Grant Nov. 14, 2017
- US 10,394,386 - Interference Detection - Grant Aug. 27, 2019
- US 15/685,937 - Mixer Circuit - Application February 28, 2019
- US 15/885,769 - Oscillator Temperature Coefficient Adjustment - Pending Jan. 31, 2018
