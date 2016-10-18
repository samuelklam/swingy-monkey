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
        state = (state['tree']['bot'], state['tree']['top'], state['monkey']['bot'], state['monkey']['top'], state['monkey']['vel'], state['tree']['dist'])
        if self.last_state is not None:
            Q[(self.last_state, self.last_action)] = Q[(self.last_state, self.last_action)] \
            + alpha*(self.last_reward + gamma*max(Q[(state, True)], Q[(state, False)]) - Q[(self.last_state, self.last_action)])


        # You'll need to take an action, too, and return it.
        # Return 0 to swing and 1 to jump.


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
Q = Counter()
alpha = 0.2
gamma = 1
highestscore = 0

for ii in xrange(iters):
    epochscore = 0
    # Make a new monkey object.
    swing = SwingyMonkey(sound=False,            # Don't play sounds.
                         text="Epoch %d" % (ii), # Display the epoch on screen.
                         tick_length=1,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)
    learner.epsilon = 0.02

    # Loop until you hit something.
    while swing.game_loop():
        pass
    # print epochscore
    # Reset the state of the learner.
    learner.reset()


    
