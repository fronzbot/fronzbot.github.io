---
layout: post
title: Determining if a System is Linear
date: 2012-02-23 06:00
description: Way to determine if a system is actually linear
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - theory
  - systems
use_math: true
project: false
feature: false
---
After getting a few projects done today I had a bit a free time and for some reason remembered a story my Linear Systems professor told my class about a year ago.  Here's the gist: he was listening to a Master's thesis defense that involved some sort of system.  The master's candidate had, for the entirety of the thesis research, assumed that his/her system was linear.  They based this assumption on the fact that it could be modeled close to something like $$y=ax+b$$.  My professor quickly pointed out that it is not, in fact, a linear system but the candidate vehmently argued that the equation was linear therefore the system was linear.  It ended in the person not actually getting a Master's degree but the point of the story is: 

**just because a system can be represented by a linear equation does NOT make it linear!** 

Why is this important?  Many equations and theories rely on the assumption that a system is linear.  If the system you're working on _isn't_ linear, your life just became a bit more complicated and the techniques you used to use in school may not actually apply.  Being able to recognize if a system is linear or not is a fairly useful tool to have so I'll go over the above example where you have a system whose output is defined as $$ ax + b$$ where $$x$$ is the input to the system. As a note, I take all derivation here from the textbook **Signals and Systems** by Alan V. Oppenheim and Alan S. Willsky.  It is the second edition book and the section that deals with this begins on page 53.

In order for a system to be linear, it must obey the property of superposition.  That is, if I have the input to a system as the sum of two signal, $$ X_{1} + X_{2}$$, the output will be $$Y = Y_{1} + Y_{2}$$.  Easy, right? Personally, I learn best by examples so I will offer the first one where I have a system whose input and output is related by $$ Y = aX $$.  First, let's say we have two inputs $$ X_{1}$$ and $$X_{2}$$ so that we have $$Y_1 = aX_1$$ and $$Y_2 = aX_2$$. Now, let's define a third signal that is a linear combination of our two inputs $$X_1$$ and $$X_2$$: $$X_3 = bX_1 + cX_2$$. (b and c are arbitrary scaling constants). Finally we simply need to check if the system is linear.

If we have an input $$X_3$$ we know that the system's output and input will be related like so: $$Y_3 = aX_3$$.  Let's plug in for $$X_3$$ to see if the system is linear: 

$$Y_3 = a(bX_1 + cX_2) \\
Y_3 = abX_1 + acX_2 \\
Y_3 = b(aX_1) + c(aX_2) \\
Y_3 = bY_1 + cY_2$$

Excellent!  Superposition holds true so we know that the system must be linear!   Now, let's try that for a linear equation $$Y = aX + b$$. Let's define the output for two different signals: $$Y_1 = aX_1 + b$$ and $$Y_2 = aX_2 + b$$.  And let's also define a third signal as the sum of the first two inputs: $$X_3 = mX_1 + nX_2$$.  (Like before, m and n are arbitrary constants). So for an input of $$X_3$$ we should expect $$Y_3 = aX_3 + b$$.  Plugging in for X_3 yields:

$$Y_3 = a(mX_1 + nX_2) + b$$

Now here I'm going to do something a bit different than the first example.  I'm going to solve for $$X_1$$ and $$X_2$$ and plug them into the previous equation.

$$Y_3 = a(m\frac{Y_1-b}{a} + n\frac{Y_2-b}{a}) + b \\
Y_3 = m(Y_1-b) + n(Y_2-b) + b \\
Y_3 = mY_1-mb + nY_2-nb + b \\
Y_3 = mY_1 + nY_2 + b(1-m-n)$$ 

As can be seen: $$mY_1 + nY_2 + b(1-m-n) eq mY_1 + nY_2$$ So this system is not linear despite the fact that the system is a linear equation! A pretty important concept (and sure to be a test question on an "Intro to Signals"-type test)!
