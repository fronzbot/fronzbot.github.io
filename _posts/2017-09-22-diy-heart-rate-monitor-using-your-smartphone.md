---
layout: post
title: 'DIY Heart Rate Monitor Using Your Smartphone'
date: 2017-09-21 09:00
description: Use flash and camera on smartphone as a PPG sensor to determine heartrate
author: Kevin Fronczak
email: kfronczak@gmail.com
tags:
  - systems
  - python
  - signals
  - projects
use_math: true
project: true
feature: true
---

Recently I've been quite interested in biomedical sensors, namely PPG sensors.  PPG is an initialism for for Photoplethysmogram and is generally associated with the use of a pulse oximeter.  Essentially, the skin (usually the finger for clinical devices) is illuminated by some source light and the response recorded by some photo-detector.  This same concept is used for heart-rate monitors in smart watches but relies on reflecting light off the skin rather than transmissive absorption.

## Background

In order to understand why this experiment works, we should look into a bit of the background of PPGs first.  As previously mentioned, heart-rate monitors on smart watches rely on reflecting light off of the skin and observing the response on a photo-detector.  Now, why can this measure heart-rate?  Well as the heart pumps blood through to the extremities (wrist, finger, etc) the volume of blood being moved ends up changing.  The change in blood volume ends up changing the way the skin absorbs and reflects light.  By measuring this change in light absorption, we can extract a measure of how quickly the volume of blood is changing and, thus, extract our heart-rate.

So ultimately we need a way to transmit light (ideally at a wavelength that our skin is good at reflecting) and then a way to measure this reflected light.  Luckily, everyone with a camera on their phone (and a flash!) already has this capability!

## Prerequisites

* Phone with Camera and Flash (I'm using a Nexus 5X, for reference)
* Python 3+ with the following packages:
    * numpy
    * imageio
    * matplotlib
* [ffmpeg](https://ffmpeg.org)

Note, I recommend installing [Anaconda](https://anaconda.com) as it's really awesome and contains most packages you'll need.  You'll still need to install the `imageio` PyPi package as well as an `ffmpeg` install which can be performed with the following command:

```
conda install ffmpeg -c conda-forge
```

## Recording the Heart-rate

Before we can extract the heart-rate, we must record it.  This is the easy part.
1. Open your camera app on your phone and prepare to record video (don't start the recording yet, though).
2. Turn on the flash.
3. Place your finger such that it covers both the flash AND the camera, like the image below.  Note that you need to adjust this based on your flash/camera layout.  Just make sure your finger covers both.
4. Record a video.  Duration is up to you, but I found that 20-30s videos work the best.
5. Save video to computer where you will be post-processing.

{: .center}
![Phone PPG Diagram]({{site.url}}{{site.image_path}}/ppg/phone_ppg_diagram.jpg)

## Extracting Heart-rate from Video

Now for the fun part: post-processing.  I'll post each step of the code with some explanation, and at the end of the post I'll give the full code.

# Read in Video

Step 1 is easy, we just need to read in the video.  This will use the aforementioned `ffmpeg` library to read through the video and store the red, green, and blue pixel data for every pixel in every frame.  Depending on the length of the video, this step can take a while to complete.  In my case, I had a 30s video recorded at 1920x1080 at 30 FPS which results in an uncompressed 5.6 GB of data (orders of magnitude smaller with mpeg compression, but you get my point: be patient).

```python
import numpy as np
import imageio

video = imageio.get_reader('your_video.mp4', 'ffmpeg')
```

# Extract Red/Green/Blue Channels

This next part does a few very important things.  First, we iterate over the video frame by frame and, at each frame, we average every single pixel in the frame together.  Why?  Well, ultimately, we don't care about the intensity of individual pixels.  What we care about is the total light change over the whole finger, so we get much better data when we average each pixel as we remove the variation of small localized areas and have a much larger area to work with.  Basically, we're using our expensive CMOS image sensor as a photodiode.  Talk about overkill...

Once we create our single massive pixel, we need to extract the RGB channels so we can process them independently.  The code below specifically saves each color, but I only end up using the red channel.  This is because skin is really good at reflecting red light, so the intensity of the red channel is far superior to that of blue or green.  Due to this fact, the red light will undoubtedly provide us with the best information.

```python
colors = {'red': [], 'green': [], 'blue': []}
for frame in video:
    # Average all pixels
    lumped_pixel = np.mean(frame, axis(0,1))
    colors['red'].append(lumped_pixel[0])
    colors['green'].append(lumped_pixel[1])
    colors['blue'].append(lumped_pixel[2])
```

Another step we can take (but is not necessary) is to normalize the channels to full-scale, or 255:

```python
for key in colors:
    colors[key] = np.divide(colors[key], 255)
```

# Plot Time-Series Data


# Examples
