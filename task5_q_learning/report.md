# IT3708: Project 5 – Reinforcement Learning Using Q-Learning
### Author: Petr Zvonicek

## a) Implementation

### Architecture

The project consist of three fundamental components – Flatland, QLearning and GUI. Flatland is an abstraction of the world. It stores 

### Parameters

## b) Action selection

On each run there is selected either greedy (the best from all possible, exploitation) or random (exploration) action. Although I experimented with dynamic probability in Simulated Annealing manner (linear and exponencial scaling), the best results were allways provided by fixed probability of random run to 0.2, so I sticked with this.

My idea behind this is that we need some exploration in all computation phases. In early phase the exploration is dominant (despite having just 0.2 probability, the weights are 0 for all directions so there is randomly chosen one), but also in late phase some exploration is needed so as not to stay in local maximum.

## c) Backup scheme

I've experimented with the both TD(x) and TD(λ) schemes and TD(λ) seems to provide more reliable results. Therefore I used this one. However, even TD(λ) usually provided even worse results than not using any backup scheme at all. I spend a lot of time on tweaking the trace decay factor – λ and eventually the value λ = 1 did not negativelly influenced the results and perhaps slightly improved the performance. Apart from the standard TD(λ) formulas for Q-learning I'm also resetting all *e* values to 0 when exploratory (random, non-greedy) step made. Also it was beneficial to adjust the values with backup scheme only on positive reward.

It is, however, still difficult to assess the impact of the backup scheme and it could easily have no impact at all. Due to the randomness, it is not easy to make an objective assessment of that.

I was analysing the low impact of of the backup scheme and I came up with several possible reasons for that. First possibility is a bug in my implementation. I was, however, debugging and tracing the code and the weights were updated as expected. Another reason for that could be the fact that when the the food is densely spaced, long traces could improve the path to one food, but that could also lead to missing the other food nearby. I therefore think that long traces (big x or λ) are much more suitable for sparse food placement than dense placement.