---
layout: post
title: Get Out of a Speeding Ticket
date: 2012-02-21 06:00
description: Method claimed by student to get out of a speeding ticket (I highly doubt it)
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - theory
  - fun
  - noise
use_math: true
project: false
feature: false
---
First of all, this post **does not** condone speeding.  Don't do it, it's stupid and puts other peoples lives in danger.  That said, there is a neat noise problem that may be able to get you out of a ticket were you to ever find yourself in such a bind.  I have never tried this myself (nor am I planning to) but a student in the class this problem was introduced claimed he had used a slightly modified version to successfully get out of a speeding ticket.  Laughs were had (mainly because no one thought it could actually be a good defense) but it's still an interesting problem and I'll reproduce it here! This problem makes use of [Best Linear Unbiased Estimators (BLUEs)](http://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem).

First, for the sake of completeness, I'll derive the important equations.  The first thing we know is that we have two Random Variables: $X$ and $Y$.  Now we need to define a linear estimation of $Y$.  We'll call this estimator $\hat{Y}$ and define it as $\hat{Y} = aX + b$.  Of course, if $Y$ is not linear, we are going to have some error present in our estimation.  We'll define this error as $e = Y- \hat{Y}$. Obviously, we want zero error for our estimator so we can perfectly predict our random variable's value given out estimation equation.  That means we want the mean of the error equal to zero so:

++E(e) = 0 \therefore E(Y-\hat{Y}) = 0  \\
\therefore E(Y - ax - b) = 0 \\
\therefore E(Y) - aE(X) - b = 0 \\
\therefore b = \mu_Y - a\mu_X++

Now we know we want to minimize the variance and since our ideal mean is zero we know that $\sigma_e^2 = E(e^2)$  so
++ E(e^2) = E(e\cdot e) = E(e (Y - ax - b)) \\
= E(eY) - aE(eX) - bE(e) = E(eY) - aE(eX) \\
=E(Y(Y - aX-b)) - aE(X(Y-aX-b)) \\
= E(Y^2) - aE(XY) - bE(Y) - aE(XY) - a^2E(X^2) - abE(X)++

* Note: $r$ is the correlation coefficient which is equal to $\frac{E(XY)-\mu_X\mu_Y}{\sigma_X\sigma_Y}$

++=(\sigma_Y^2 + \mu_Y^2) - 2a(r\sigma_X\sigma_Y+\mu_X\mu_Y) - b\mu_Y - a^2(\sigma_X^2+\mu_X)-ab\mu_X \\
=\sigma_Y^2+\mu_Y^2-2ar\sigma_X\sigma_Y-2a\mu_x\mu_Y-b\mu_Y+a^2\sigma_X^2+a^2\mu_X+ab\mu_X++

Plugging in for the value of $b$ found earlier yields:

++ =  \sigma_Y^2+  \mu_Y^2-2ar \sigma_X  \sigma_Y-2a \mu_x \mu_Y+a^2 \sigma_X^2+a^2 \mu_X+(a \mu_X- \mu_Y)( \mu_Y-a \mu_X)  \\
= \sigma_Y^2+ \mu_Y^2-2ar \sigma_X \sigma_Y-2a \mu_x \mu_Y+a^2 \sigma_X^2+a^2 \mu_X- \mu_Y^2-a^2 \mu_X^2+2a \mu_X \mu_Y  \\
E(e^2) = \sigma_Y^2 + a^2 \sigma_X^2 - 2ar \sigma_X \sigma_Y  \\
++

Now we need to minimize the variance by taking the derivative with respect to $a$ and setting that equal to zero:

++\frac{dE(e^2)}{da} = 1a\sigma_X^2 - 2r\sigma_X\sigma_Y = 0 \\
a\sigma_X^2 = r\sigma_X\sigma_Y \therefore a = r\frac{\sigma_Y}{\sigma_X}++

Solving for the variance with the new value for $a$

++\sigma_e^2=\sigma_Y^2+a^2\sigma_X^2-2ar\sigma_X\sigma_Y \\
=\sigma_Y^2+r^2\sigma_X^2\frac{\sigma_Y^2}{\sigma_X^2}-2r\frac{\sigma)Y}{\sigma_X}\sigma_X\sigma_Y \\
=\sigma_Y^2 - r^2\sigma_Y^2 = (1-r^2)\sigma_Y^2++

So now we know a bunch of very useful parameters for our Best Linear Unbiased Estimator:

*   $\hat{Y} = aX+b $
*   $a = r\frac{\sigma_Y}{\sigma_X}$
*   $b = \mu_Y-a\mu_X$
*   $\sigma_e^2 = (1-r^2)\sigma_Y^2$

Enough of the derivation, how do I get out of a speeding ticket?!  Well, we need to make some assumptions. First, let's pick the speed limit on the road you're driving on.  How about 55 mph?  Ok, now we need to figure out the distribution of your speed.  For simplicity, let's say your speed can be uniformly distributed across 45 mph to 65 mph.  This is not likely to be the case in the real-world- I'd actually imagine most people have a normal velocity distribution with a mean around 5 mph over the speed limit but again, I'm just giving you an example, not a solid speeding ticket defense!  Next, let's say that the police officer clocked you at a velocity of 63 mph with his radar gun.  We will call this measurement $X$ and say that $X = V + N$ where $V$ is your true speed and $N$ is the noise of the radar measurement.  Obviously there is a lot of environmental noise, especially on a busy highway, so noise will definitely have an impact on a radar reading.  To keep things simple, again, let's say that the noise introduces a uniformly distributed error of $\pm 5 mph$.  This gives the noise a mean of zero since it is uniformly distributed and centered at zero.  Essentially this is just white noise (though, obviously, not TRUE white noise because it is limited to certain values). Now, let's define an estimator equation for your velocity: $\hat{V} = aX+b$. Since $V$ is uniformly distributed between 45 mph and 65 mph, we know that $\mu_V = 55$.  Again, since the velocity is uniformly distributed, we can find the variance quite easily:

++\sigma_V^2 = \frac{l^2}{12} = \frac{(65-45)^2}{12} = \frac{100}{3}++

Using the same principle, we can find the variance of the noise:

++\sigma_N^2 = \frac{l^2}{12} = \frac{10^2}{12} = \frac{100}{12}++

Now we need to find the mean of our radar measurement $X$

++X=V+N \therefore \mu_X=\mu_V+\mu_N=55+0 \therefore \mu_X=55++

Easy enough.  Now let's find the variance of that reading:

++\sigma_X^2 = \sigma_V^2+\sigma_N^2 = \frac{100}{3}+\frac{100}{12} = \frac{500}{12}++

Now, in order to use our derived BLUE parameters (that just sounds silly, doesn't it?  It _is_ the acronym, though!) we need to get $\sigma_X$ so all we need to do is:

++\sigma_X=\sqrt{\frac{500}{12}}=5\frac{\sqrt{5}}{\sqrt{3}}++

Now let's find the correlation coefficient between your true speed and the police officer's radar reading.  First we need to know what $E(VX)$ is:

++E(VX) = E(V^2)+E(VN) = E(V^2)+E(V)E(N) = E(V^2) = \sigma_V^2+\mu_V^2 = \frac{100}{3} + 55^2++

Now we can find the correlation coefficient:

++r_{VX} = \frac{E(VX)-\mu_V\mu_X}{\sigma_V\sigma_X} = \frac{\frac{100}{3}+55^2-55^2}{\frac{10}{\sqrt{3}}5\frac{\sqrt{5}}{\sqrt{3}}}=\frac{\frac{100}{3}}{\frac{50\sqrt{5}}{3}} = \frac{100}{50\sqrt{5}} = \frac{2}{\sqrt{5}}++

Now we just need to "plug-n-chug" with our [BLUE parameters](http://www.youtube.com/watch?v=BznwsT6r_tM):

++a=r\frac{\sigma_Y}{\sigma_X}=\frac{2}{\sqrt{5}}(\frac{\sigma_V}{\sigma_X}) = \frac{2}{\sqrt{5}}(\frac{10/\sqrt{3}}{5\sqrt{5}/\sqrt{3}}) = \frac{20}{25} \therefore a=0.8++
++b=\mu_V-a\mu_X = 55-0.8(55) = 0.2(55) ++
++therefore b =11++ 
++\hat{V} = 0.8X+11++

Now that we have the equation for our linear estimator, all we need to do is plug the officer's radar reading into $X$ and we will get your true speed taking into account your driving habits (uniformly distributed velocity) and the noise present in the environment that will negatively impact radar readings.  Your true speed?  61.4 mph or a 2.5% difference from what the officer clocked you at.  If you increase the variance of the noise, you will decrease your true speed estimation!   Again, I do not condone speeding.  This information presented here is specifically for your academic edification and not meant to be any legal advice pertaining to a speeding ticket.  Hope it was interesting!  Maybe if I get around to it I'll see what happens when you have a normal distribution of speed rather than uniform.  Might be neat!
