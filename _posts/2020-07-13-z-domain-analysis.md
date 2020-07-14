---
layout: post
title: 'Z-Domain Analysis'
date: 2020-07-13 09:00
description: Intuitively approaching Z-domain system analysis
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - analog
  - systems
  - theory
  - signals
  - digital
use_math: true
project: false
feature: false
---

One thing I really feel was lacking in my education was a good treatment of Z-domain circuits and analysis. Although, maybe it wasn't lacking and I just didn't appreciate the applications of it. Either way, over time in my career I've had to develop my skills at Z-domain analysis and learn various tips and tricks to help approach the analysis in an intuitive way. It's one thing to know how to apply an equation, but another to understand _why_ you are applying the equation. My goal with this post is to highlight some of the important topics I think are useful for any Z-domain circuit and system analysis.

**Tabe of Contents**
* TOC
{:toc}

## Z-Domain Basics

Continuous time signals can be converted into a complex frequency domain by means of the Laplace Transform. For analog engineers, this is our domain of choice. Working in the s-domain provides deeper insights into circuit operation than time domain allows. This concept can be extended to discrete-time (aka sampled time) signals by means of the Z-Transform.

In my mind, the most intuitive way to compare the s-domain to the Z-domain is to think about an integrator. We know that in the s-domain this is represented simply as $$\frac{1}{s}$$ and know that for a constant input, the output will ramp up indefinitely. We are, of course, integrating.  But what does this look like in the z-domain? What does it mean to integrate a sampled signal?

The conversion from the time domain and sampled-time domain requires us to re-frame how we think of time. In continuous time (which is the world we live in), time is always increasing and can be reduced to arbitrary levels of accuracy. Continuous time is uncountably infinite. Sampled-time, on the otherhand, has a strict step-size dictated by some periodic sampling signal. Each step-size, therefore, is well-definied meaning sampled-time is _countably_ infinite.

Now, if we chop up or constant input into small discrete points instead of having an input that looks like $$x(t) = 1$$ in the time domain, we'd have $$x[n] = 1$$. This may look the same, but there is a subtle difference: $$n$$ is discrete. The next value of $$n$$ will be a pre-determined distance away from the previous value. The $$M^{th}$$ value of $$n$$ will be M-times that pre-determined step size from your starting value. And so-on. Now think about that in the context of integration. That step size is analogous to our $$dx$$ in the continuous-time equation $$y(t) = \int x(t) dx$$. So if we know the step size, to integrate we just need to add the current value of $$x[n]$$ to the previous value of $$y[n]$$.  In otherwords, at any sampled-time value we know that the current integration value can be defined as $$y[n] = x[n] + y[n-1]$$. Extending that to arbitrary sizes, we can say:

$$y[N] = \sum_{n=0}^{N} x[n]$$

The key takeaway here is that since the interval is well-defined in sample-space, a sum performs the same function that integration does in the time-domain.

Now we have to look at this in the z-domain. We know that integration in the time-domain is represented as $$\frac{1}{s}$$, as mentioned earlier, so how can we transform the sampled-time version into a Z-domain expression?

Let's start with the generic equation

$$y[n] = x[n] + y[n-1]$$

We want to find an expression $$Y(z)$$ for an input $$X(z)$$. That means we must convert those discrete time signals into Z-domain expressions. Two very simple relations are all we need for this (going any deeper than this is well beyond the scope of this post):

$$\delta[n] \rightarrow 1$$

$$\delta[n-a] \rightarrow z^{-a}$$

That yields:

$$Y(z) = X(z) + Y(z)\cdot x^{-1}$$

$$\frac{Y(z)}{X(z)} = \frac{1}{1-z^{-1}}$$

This result is equivalent to integration.

### Conversion to Frequency Domain

Converting to the frequency domain requires a relation between the variable $$z$$ and frequency. Much like how the Laplace transform maps time to a complex frequency plane, the Z-Transform does something similar. Instead of a complex plane, however, it maps to a unit circle. I could go into more detail here, but suffice to say that when we map to a unit circle the outcome is that:

$$z = e^{j\omega T}$$

Where $$T$$ in this context is the sampling period. In general, analyzing a system with $$T=1s$$ simplifies things a bit without losing information.

So, using our integration example above let's convert to the frequency domain:

$$H(j\omega) = \frac{1}{1-e^{-j\omega}} = \frac{e^{j\omega}}{e^{j\omega} - 1}$$

$$H(j\omega) = \frac{\cos(\omega) + j\cdot \sin(\omega)}{\cos(\omega) - 1 + j\cdot \sin(\omega)} $$

Now we want to get the magnitude response so we will first multiple the numerator and denomonator by the complex conjugate of the denomonator.

$$H(j\omega) = \frac{1}{4}\frac{1-\cos(\omega)-j\cdot \sin(\omega)}{\sin^2(\frac{\omega}{2})}$$

To get the magnitude response we need to square the real an imaginary parts, sum them, and take the square root:

$$H(\omega) = \frac{1}{2}\csc(\frac{\omega}{2})$$

Obviously, getting the frequency response is a bit more labor-intensive than we'd like (I talk about an easier approach later). However we can now plot the response to see that it looks like it's integrating (infinite gain at DC with a decreasing gain as frequency increases).

[img]/zdomain/integrator.jpg

{: .center}
[![{{site.url}}]({{ site.url }}{{ site.image_path }}/zdomain/integrator.jpg)]({{ site.url }}{{ site.image_path }}/zdomain/integrator.jpg)

But that's not quite true, is it? At every integer multiple of the sample frequency, the waveform again has infinite gain. This is an artifact of sampling. An intuitve way to thing about this is recall that we're mapping the z-domain to a unit circle so unique values can only exist as we traverse the circumference of the circle once. We will see the same thing on the second revolution that we did on the first.  Hence, every integer multiple of the sample frequency just means we've gone back to our starting point on the unit circle.

### Simple Example

Let's take a look at a simple example. See the diagram below. We have a signal that splits into two paths, one has a delay and the other does not. These lines are then summed before being output. As a sidenote, this example is actually part of an interview question I've been asked before and now ask when I'm interviewing. I think it's a really good one that helps to figure out whether a candidate is comfortable with sampled systems (and if they're not, it's a really good way to see how they think about a problem and learn. Interview questions are somewhat useless if the candidate already knows the answer!).

[img]/zdomain/delayline.jpg

## Switched Capacitor Circuits

Content

### Passive Filter

Content

### Demodulator

[US9817502B2](https://patents.google.com/patent/US9817502B2/en)

### Parasitic Insensitive Integrator (with finite gain)

Content

### First-order Delta Sigma Modulator

Content

## Poles and Zeros

Content

### Estimating Frequency Response

Content

### 2-tap FIR Filter

Content

### 4-tap FIR Filter

Content

### Simple example (revisted)

Content

### Second-order Delta Sigma Modulator with Non-ideal Quantizer

Content

## Afterword

Content
