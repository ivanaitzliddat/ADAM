# About ADAM (in development phase)
Auxillary Dynamic Alert Monitor (ADAM) is a user-customisable alert monitoring system that takes in display inputs from connected systems, analyses their screen content, and alerts the user if configured word triggers are detected. ADAM is designed to function completely offline and to not interact with/control the connected systems in any way (all it does is "see"). ADAM is useful in environments where Internet connectivity is not available, and where the systems to be monitored are not able to connect to typical monitoring systems and devices.

More details will be updated once the project is completed.

## Introduction
We utilise a series of hardware components to help pipe all the screens that we are monitoring into one desktop, where a series of software 
will process these screens and based on the keywords provided by the user, an alert will pop up. This helps to reduce the strain on the monitoring crew which is required to constantly look at the whole set of screens.

## Overview
The overall set up is as shown in the image below.

![Overview](./Images/Overall(new).png)

### Hardware Component
In this project, our main hardware components consist of the USB-HDMI Capture Card and a Central Computer, also known as ADAM PC.

## Quick Start

### Option 1: Using .exe file (hassle-free)

Our team will be working on releasing a .exe file so that users can run the software without any prior programming knowledge.

### Option 2: Setting Up on your local machine

This requires users to have some knowledge on setting up python system. The benefit is that users will be able to tweak any part of the code for their needs.

Detailed Steps:
1. Clone the repo onto your local machine.
1. Ensure python and pip are installed.
1. Install the libraries using `pip install -r requirements.txt`
1. Run the python file using `python ./Actual/main.py`
