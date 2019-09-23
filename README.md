# Requirements

Please don't forget to use Python3...

You shouldn't be using a lot of Python2 anyways...

hopefully...?

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

# A-*

## Introduction

This is a simple A* algorithm where we run the dijkstra with the following focus:

### **Search Space**:
The search space for each movement would depend on two factors:
    1. Which side the lamp is currently at.
    2. Who is at the side where the lamp is at.

### **Initial State**:
In the beginning we would have everyone on the left side and no one on the right side.
Since we will represent the people present with a bit flip when on, they are present, the initial state would be (31, 0).

### **Goal State**:
Since the goal state would be to have everyone on the right side of the bridge, the representation state would be (0, 31).

### **Rules**:
    - Only 2 people can be bit flipped at the same time where we take the max(cost1, cost2) as cost.
    - Cost can not exceed the hard limit of 30.

### **Cost Function**:
This is currently set to ```return 1```

### **Heuristic Function**:
This is also currently set to ```return 1```.

This is yet to be implemented.

### **Search Tree Generation**:
Output by matplotlib + networkx...

The following is an output using matplotlib + networkx for a simple run:

## Usage

Like the other projects, the best recommendations would be to read the code given its size and simplicity.

However, here are some of the flags, and a simple way to run this.

```shell
# Main focus of homework...
./main.py

# For variable max-cost.
./main.py --max-cost=30
```
