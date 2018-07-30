"""
RL MODULE WITH WEIGHTS (and takes Random-Search Values via cPickle)

CALL BY:    <weights_nn.py>

RETURN:     Reward Print and Parameter-dump of the Weight matrices

INFO:       -
"""

# Some dependencies
import numpy as np # Maths and stuff
import matplotlib.pyplot as plt
import gym.spaces # Simulating the Environments
import cPickle as pickle # Store Data into [.p] Files
import datetime # For Datestamp on stored files

from lif import Iw_syn_calc, Iw_gap_calc, U_neuron_calc
from parameters import *

# Initialization----------------------------------------------------------------------------

def initialize(Default_U_leak, load_matrices):
    global totalreward, done, info

    # Initializing Neurons and Sensors------------------------------------------------------
    for i in range(0,4):
        x[i] = Default_U_leak
    for i in range(0,4):
        u[i] = Default_U_leak

    # OpenAI Gym Parameters----------------------------------------------------------------
    totalreward = 0
    done = 0
    info = 0

    parameters = pickle.load( open(load_matrices, "r"))

    w_A_rnd = parameters[0]
    w_B_rnd = parameters[1]
    w_B_gap_rnd = parameters[2]
    sig_A_rnd = parameters[3]
    sig_B_rnd = parameters[4]
    C_m_rnd = parameters[5]
    G_leak_rnd = parameters[6]
    U_leak_rnd = parameters[7]

    return w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd

#-------------------------------------------------------------------------------------------

# Random Function---------------------------------------------------------------------------

def random_weights():

    # Initializing Weight matrices
    A_rnd = np.random.rand(1,10)
    B_rnd = np.random.rand(1,8)
    B_gap_rnd = np.random.rand(1,2)

    return A_rnd, B_rnd, B_gap_rnd

#-------------------------------------------------------------------------------------------

# Compute Function--------------------------------------------------------------------------

def compute(x, u, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd, B_gap_rnd):

    # Compute all Synapse Currents in this network------------------------------------------
    k = 0
    l = 0
    m = 0

    for i in range(0,4):
        for j in range (0,4):
            # Synapse Currents between Interneurons
            if A[i, j] == 1:
                # Excitatory Synapse
                I_s_inter[i, j] = Iw_syn_calc(x[i], x[j], E_ex, w_A_rnd[0, k], sig_A_rnd[0, k], mu, A_rnd[0, k])
                k += 1
            elif A[i, j] == -1:
                # Inhibitory Synapse
                I_s_inter[i, j] = Iw_syn_calc(x[i], x[j], E_in, w_A_rnd[0, k], sig_A_rnd[0, k], mu, A_rnd[0,k])
                k += 1
            else:
                I_s_inter[i, j] = 0


            # Synapse Currents between Sensory and Interneurons
            if B[i, j] == 1:
                # Inhibitory Synapse (can't be Excitatory)
                I_s_sensor[i, j] = Iw_syn_calc(u[i], u[j], E_in, w_B_rnd[0, l], sig_B_rnd[0, l], mu, B_rnd[0,l])
                l += 1
            else:
                I_s_sensor[i, j] = 0

            # Gap-Junction Currents between Sensory and Interneurons
            if B_gap[i, j] == 1:
                # There is a Gap-Junctions
                I_g_sensor[i, j] = Iw_gap_calc(x[i], x[j], w_B_gap_rnd[0, m], B_gap_rnd[0,m])
                m += 1
            else:
                I_g_sensor[i, j] = 0

    #---------------------------------------------------------------------------------------

    # Now compute inter Neurons Voltages----------------------------------------------------
    for i in range(0,4):
        I_syn_inter = I_s_inter.sum(axis = 0) # Creates a 1x5 Array with the Sum of all Columns
        I_gap_inter = I_g_inter.sum(axis = 0)
        I_syn_stimuli = I_s_sensor.sum(axis = 0)
        I_gap_stimuli = I_g_sensor.sum(axis = 0)
        x[i], fire[i] = U_neuron_calc(x[i], I_syn_inter[i], I_gap_inter[i], I_syn_stimuli[i], I_gap_stimuli[i], C_m_rnd[0,i], G_leak_rnd[0,i], U_leak_rnd[0,i], v, delta_t)

    #---------------------------------------------------------------------------------------

    I_syn = np.add(I_syn_inter, I_syn_stimuli)
    I_gap = np.add(I_gap_inter, I_gap_stimuli)

    return x, u, fire, I_syn, I_gap

#-------------------------------------------------------------------------------------------

# OpenAI Gym--------------------------------------------------------------------------------

def run_episode(env, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd, B_gap_rnd):
    global x, u, fire, I_syn, I_gap, action, env_vis

    observation = env.reset()
    totalreward = 0

    for t in np.arange(t0,T,delta_t): # RUNNING THE EPISODE - Trynig to get 200 Steps in this Episode

        # Compute the next Interneuron Voltages along with a possible "fire" Event - Now new with random parameter matrices
        x, u, fire, I_syn, I_gap = compute(x, u, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd, B_gap_rnd)
        # Decide for an action and making a Step
        if fire[0] == 1: # Sensory Neuron AVA is firing - resulting in a REVERSE Action (0)
            action = 0
            observation, reward, done, info = env.step(action)
            totalreward += reward
            #print 'RIGHT'
        elif fire[3] == 1: # Sensory Neuron AVB is firing - resulting in a FORWARD Action (1)
            action = 1
            observation, reward, done, info = env.step(action)
            totalreward += reward
            #print 'LEFT'
        else:
            #print 'Im not sure :( Going ',action
            #action = np.random.randint(0,1) # Tried a random approach - didn't seem to work
            observation, reward, done, info = env.step(action) # Have to use the action from the past time step - OpenAI Gym does not provide a "Do nothing"-Action
            totalreward += reward
        observe(observation)
        if done:
            break

    return totalreward

def observe(observation):
    global u

    cart_pos = observation[0] # [-2.4 2.4]
    #cart_vel = observation[1]
    angle = (observation[2] * 360) / (2 * np.pi) # in degrees [-12deg 12deg] (for Simulations)
    #angle_velocity = observation[3]

    # Adapt, learn, overcome-----------------------------------------------------------------------------------------

    # Setting the Angle of the Pole to Sensory Neurons PLM (Phi+) and AVM (Phi-)
    if angle > 0:
        u[1] = -70 + (50/12) * angle # PLM
        u[2] = -70
    elif angle == 0:
        u[1] = u[2] = -70
    else:
        u[2] = -70 + (50/12) * angle # AVM
        u[1] = -70

    # Setting the Cart Position to Sensory Neurons ALM (pos. movement) and PVD (neg. movement)
    if cart_pos > 0:
        u[3] = -70 + (50/2.4) * cart_pos # ALM
        u[0] = -70
    elif cart_pos == 0:
        u[0] = u[3] = -70
    else:
        u[0] = -70 + (50/2.4) * cart_pos # PVD
        u[3] = -70

    '''
    # Setting the Anglespeed of the Pole to Sensory Neurons ALM (Phi.+) and PVD (Phi.-)
    if angle_velocity >= 0:
        u[3] = -70 + (50/5) * angle_velocity # ALM
        u[0] = -70
    elif cart_pos == 0:
        u[0] = u[3] = -70
    else:
        u[0] = -70 + (50/5) * angle_velocity # PVD
        u[3] = -70
    '''

#------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
# Main Function-----------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def main(simulations, load_parameters):
    global x, u, env, action

    env_vis = []
    action = 0
    episodes = 0
    best_reward = 0
    env = gym.make('CartPole-v0')

    for _ in xrange(simulations):

        w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd = initialize(Default_U_leak, load_parameters) # Initializing all Sensory- and Interneurons with the desired leakage voltage [-70mV]
        episodes += 1 # Episode Counter
        A_rnd, B_rnd, B_gap_rnd = random_weights() # Make some new random Weights
        reward = run_episode(env, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd, B_gap_rnd)
        if reward > best_reward:
            # Set current reward as new reward
            best_reward = reward
            # Save Results of the Run with the best reward
            Weights = [A_rnd, B_rnd, B_gap_rnd]
            # Solved the Simulation
            if reward == 200:
                break
        #print 'Episode',episodes,'mit Reward',reward,'.'

    print 'The best Reward was:',best_reward
    if best_reward == 200:
        print 'I SOLVED IT!'

    date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    best_reward_s = str(int(best_reward))
    pickle.dump(Weights, open(("weight_dumps/" + date + "_" + best_reward_s + ".p"), "wb"))

    return date, best_reward_s

#-------------------------------------------------------------------------------------------


if __name__=="__main__":
    main()
