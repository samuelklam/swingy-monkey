import numpy.random as npr
import sys
from collections import Counter
import math

from SwingyMonkey import SwingyMonkey

class Learner:

    def __init__(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def action_callback(self, state):
        '''Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.'''
        # You might do some learning here based on the current state and the last state.
        global epochscore
        epochscore = state['score']
        oldstateformat = state
        treedist = math.floor(state['tree']['dist']/treedistbin)
        diff = math.floor((state['monkey']['bot']-state['tree']['bot'])/diffbin)
        state = (diff, treedist)
        if self.last_state is not None:
            Q[(self.last_state, self.last_action)] = Q[(self.last_state, self.last_action)] \
            + alpha*(self.last_reward + gamma*max(Q[(state, True)], Q[(state, False)]) - Q[(self.last_state, self.last_action)])


        # You'll need to take an action, too, and return it.
        # Return 0 to swing and 1 to jump.

        if self.last_state == state and oldstateformat['monkey']['bot'] - oldstateformat['tree']['bot'] >= 10:
            self.last_action = False
            return self.last_action


        self.last_state = state

        if Q[(state, False)] >= Q[(state, True)]:
            bestaction = False
            otheraction = True
        elif Q[(state, False)] < Q[(state, True)]:
            bestaction = True
            otheraction = False
        if npr.rand() > self.epsilon/2:
            self.last_action = bestaction
        else:
            self.last_action = otheraction

        return self.last_action



    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''
        self.last_reward = reward

iters = 100
learner = Learner()
diffbin = 30
treedistbin = 30
Q = Counter()
alpha = 0.2
gamma = 1
highestscore = 0

if len(sys.argv) == 3:
    alpha = float(sys.argv[1].split("=")[1])
    gamma = float(sys.argv[2].split("=")[1])

for diff in range(-80, 80):
    for dist in range(-80, 80):
        Q[(diff, dist), True] = -0.2

for epoch in xrange(iters):
    epochscore = 0
    # Make a new monkey object.
    swing = SwingyMonkey(sound=False,            # Don't play sounds.
                         text="Epoch %d" % (epoch), # Display the epoch on screen.
                         tick_length=1,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)
    if epoch < 70:
        learner.epsilon = 0.1/(int(epoch/10) + 1)
    else: 
        learner.epsilon = 0

    # Loop until you hit something.
    while swing.game_loop():
        pass
    # print epochscore
    # Reset the state of the learner.
    learner.reset()


    
