# M@r5 3xpl0r3r

## Introduction

This is a project consisting of creating a front-end and a simple AI back-end for a Mars Rover.

The Mars Rover mission consists of collecting multiple rocks. However due to the extreme conditions in Mars, explorers are needed to collect the rocks. As we all know, these explorers are simple programmable objects that YOU can modify.

The Mars Rover Explorer object has 1 simple objective. Collect rocks and take it to the Command Center!

As easy as this may seem, Mars has obstacles that explorers have to avoid at all costs and not only that, a Mars Rover Explorer may only have 1 rock at a time. (For now...)

Due to this limitation, a multi-agent system was developed! A Mars Rover Explorer utilizes a **high-end-multi-functional-amazing-message-queue**.
*What does this mean?* This means that an explorer may communicate with its **team** using this message_queue.

THATS RIGHT. Did I forget to mention that there is a single and double mode where there are 2 different command centers and explorers from different teams working with their team to collect rocks?

## Usage

Firstly, I think reading the code itself would be the best documentation. Especially given a small project such as this one.

However, here are some of the flags, and a simple way to run this.

```shell
# Main focus of homework...
# For multi-agent system in a MULTIVERSE.
./main.py --multi_agent

# For single-agent system in a MICROVERSE.
./main.py --mode='single'

# Custom multi-agent system in a MULTIVERSE.
./main.py --obstacles=50 --rocks=70 --explorers=30 --multi_agent
```


## Requirements

Please don't forget to use Python3...
You shouldn't be using a lot of Python2 anyways...
hopefully...?