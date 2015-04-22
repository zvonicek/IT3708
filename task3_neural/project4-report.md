# IT3708: Project 4 – Evolving Neural Networks for a Minimally-Cognitive Agent
### Author: Eva Tesarova, Petr Zvonicek

## a) Implementation

### Genotype / Phenotype representations

TBD Petr

### CTRNN

CTRNN description: TBD

The input is given as binary quintuple, 1 means that the sensor detected object, 0 that no object was detected.

The motor output is formed by two neurons, which gives output in the range from 0 to 1. The tracker direction is decided by the neuron which gives higher value (i.e. one represent *right* direction, one *left* direction. The speed of the tracker is then computed from the value of the "winning" neuron. By multiply this value by 5 we scale its output to the 4 possible speeds. 

With pull extension we gave to output layer one more neuron. It has the same properties as the others in this layer, i.e. it is connected to bias and also it to every neuron in this layer (self included). We interpret its output (which is again in range $(0,1)$) as make a pull action if it is higher than the value $0.5$.

## b) Performance

### Standard scenario

In the standard scenario, agent always choose at the beginning one direction which then hold for all the simulation. Its behaviour under the objects is various, depending on run of our EA. Two main approaches can be seen:

- It is going fast and first run through the world it "scans" the object and in the second it stops under if it is small object.

- It is going slower and when it is under object it tries to catch it at the end part. If it sees that object is big, it just pass without stop under it.

Our trackers has problems with catching objects while they appear immediately above them after they caught something. Usually they just continue with the rest and don't try to avoid/catch object. 


### Pull scenario
With the pull scenario agent behaves similarly as in the standard case. When it just stopped in the standard case and waited for the object, now he use pull action to get the object faster. Sometimes immediately after it takes the pull action it use it also for bigger object.  


### No-Wrap scenario

TBD

## c) CTRNN Analysis

We use the same topology as was in the assignment. Lets mark neuron from the input layer as $i_1, \dots, i_5$, neurons from the hidden layer as $h_1, h_2$, neurons from the motor output layer as $o_1, o_2$ and the bias neuron as $b$. One of the evolved ANN weights are followed:

|to\from| $i_1$ | $i_2$ | $i_3$ | $i_4$ | $i_5$ | $h_1$ | $h_2$ | $o_1$ | $o_2$ |  $b$  |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| $h_1$ |  5.0  |-4.647 |-4.058 |-1.274 |  5.0  | 2.019 | 2.294 |       |       |-1.019 |
| $h_2$ |-3.862 | 0.098 | 3.980 |-2.960 |  5.0  | 1.352 | 3.0   |       |       |-0.352 |
| $o_1$ |       |       |       |       |       | 2.176 | -1.0  |  1.0  | -3.0  |-0.705 |
| $o_2$ |       |       |       |       |       |  -3.0 | 4.294 |  1.0  |  5.0  |-9.019 | 

|              | $h_1$ | $h_2$ | $o_1$ | $o_2$ |
|--------------|-------|-------|-------|-------|
|gains         | 4.921 | 3.996 | 2.003 | 2.992 |
|time constants| 1.0   | 1.250 | 1.003 | 2.0   |