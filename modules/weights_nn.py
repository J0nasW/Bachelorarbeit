"""
RL MODULE WITH WEIGHTS (and takes Random-Search Values via cPickle)

CALL BY:    <weights_nn.py>

RETURN:     Reward Print and Parameter-dump of the Weight matrices

INFO:       -
"""

# Some dependencies
import numpy as np # Maths and stuff
import gym.spaces # Simulating the Environments
import hickle as hkl
import time # For Runtime Evaluations
import datetime # For Datestamp on stored files

from .lif import Iw_syn_calc, Iw_gap_calc, U_neuron_calc
from .parameters import *
from .random_search_v2 import observe

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

    parameters = hkl.load(load_matrices)

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
    A_rnd = np.squeeze(np.random.rand(1,A_all))
    B_rnd = np.squeeze(np.random.rand(1,B_all))

    return A_rnd, B_rnd

def random_weights_symm():

    # Initializing Weight matrices
    A_rnd = np.random.rand(1,A_all_symm)
    A_rnd = np.append(A_rnd, A_rnd)
    B_rnd = np.random.rand(1,B_all_symm)
    B_rnd = np.append(B_rnd, B_rnd)

    return A_rnd, B_rnd

#-------------------------------------------------------------------------------------------

# Compute Function--------------------------------------------------------------------------

def compute(x, u, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd):

    # Compute all Synapse Currents in this network------------------------------------------
    k = 0
    l = 0
    m = 0
    n = 0

    for i in range(0,4):
        for j in range (0,4):
            # Synapse Currents between Interneurons
            if A[i, j] == 1:
                # Excitatory Synapse
                I_s_inter[i, j] = Iw_syn_calc(x[i], x[j], E_in, w_A_rnd[k], sig_A_rnd[k], mu, A_rnd[k])
                k += 1
            elif A[i, j] == 2:
                # Inhibitory Synapse
                I_s_inter[i, j] = Iw_syn_calc(x[i], x[j], E_ex, w_A_rnd[k], sig_A_rnd[k], mu, A_rnd[k])
                k += 1
            else:
                I_s_inter[i, j] = 0


            # Synapse Currents between Sensory and Interneurons
            if B[i, j] == 1:
                # Inhibitory Synapse (can't be Excitatory)
                I_s_sensor[i, j] = Iw_syn_calc(u[i], u[j], E_in, w_B_rnd[m], sig_B_rnd[m], mu, B_rnd[l])
                l += 1
                m += 1
            elif B[i, j] == 2:
                I_s_sensor[i, j] = Iw_syn_calc(u[i], u[j], E_ex, w_B_rnd[m], sig_B_rnd[m], mu, B_rnd[l])
                l += 1
                m += 1
            elif B[i, j] == 3:
                # Gap Junction
                I_g_sensor[i, j] = Iw_gap_calc(u[i], x[j], w_B_gap_rnd[n], B_rnd[l])
                l += 1
                n += 1
            else:
                I_s_sensor[i, j] = 0
                I_g_sensor[i, j] = 0

    # ---------------------------------------------------------------------------------------

    # Now compute inter Neurons Voltages----------------------------------------------------
    for i in range(0,4):
        I_syn_inter = I_s_inter.sum(axis = 0) # Creates a 1x5 Array with the Sum of all Columns
        I_gap_inter = I_g_inter.sum(axis = 0)
        I_syn_stimuli = I_s_sensor.sum(axis = 0)
        I_gap_stimuli = I_g_sensor.sum(axis = 0)
        x[i], fire[i] = U_neuron_calc(x[i], I_syn_inter[i], I_gap_inter[i], I_syn_stimuli[i], I_gap_stimuli[i], C_m_rnd[i], G_leak_rnd[i], U_leak_rnd[i], v, delta_t)

    #---------------------------------------------------------------------------------------

    I_syn = np.add(I_syn_inter, I_syn_stimuli)
    I_gap = np.add(I_gap_inter, I_gap_stimuli)

    return x, u, fire, I_syn, I_gap

#-------------------------------------------------------------------------------------------

# OpenAI Gym--------------------------------------------------------------------------------

def run_episode(env, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd):
    global x, u, fire, I_syn, I_gap, action, env_vis

    observation = env.reset()
    totalreward = 0

    for t in np.arange(t0,T,delta_t): # RUNNING THE EPISODE

        # Compute the next Interneuron Voltages along with a possible "fire" Event - Now new with random parameter matrices
        x, u, fire, I_syn, I_gap = compute(x, u, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd)
        # Decide for an action and making a Step
        if fire[0] == 1: # Sensory Neuron AVA is firing - resulting in a REVERSE Action (0)
            action = 0
            observation, reward, done, info = env.step(action)
        elif fire[3] == 1: # Sensory Neuron AVB is firing - resulting in a FORWARD Action (1)
            action = 1
            observation, reward, done, info = env.step(action)
        else:
            observation, reward, done, info = env.step(action) # Have to use the action from the past time step - OpenAI Gym does not provide a "Do nothing"-Action

        totalreward += reward
        observe(observation)
        if done:
            break

    return totalreward

#------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
# Main Function-----------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def main(sim_time, load_parameters, best_reward_p):
    global x, u, env, action

    start_time = time.time()

    action = 0
    episodes = 0
    best_reward = 0
    env = gym.make('CartPole-v0')

    while True:
        w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd = initialize(Default_U_leak, load_parameters) # Initializing all Sensory- and Interneurons with the desired leakage voltage [-70mV]
        episodes += 1 # Episode Counter
        if IsSymmetrical == True:
            A_rnd, B_rnd = random_weights_symm() # Make some new random Weights
        elif IsSymmetrical == False:
            A_rnd, B_rnd = random_weights() # Make some new random Weights
        reward = run_episode(env, w_A_rnd, w_B_rnd, w_B_gap_rnd, sig_A_rnd, sig_B_rnd, C_m_rnd, G_leak_rnd, U_leak_rnd, A_rnd, B_rnd)
        if reward > best_reward:
            # Set current reward as new reward
            best_reward = reward
            # Save Results of the Run with the best reward
            Weights = [A_rnd, B_rnd]
        #print 'Episode',episodes,'mit Reward',reward,'.'
        if (time.time() - start_time) >= sim_time:
            break

    best_reward_p = int(best_reward_p)
    best_reward_s = str(int(best_reward))
    date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

    if best_reward_p >= best_reward:
        # Information Text File
        file = open((current_dir + "/information/" + date + "_weight_run_FAILED.txt"), "w")
        file.write(("Corresponding Parameter Set: " + load_parameters + "\nWeight run from " + date + " with Reward " + best_reward_s + " did FAIL! NeuronalCircuit_v3"))
        file.close()
    else:
        episodes = str(int(episodes))
        hkl.dump(Weights, (current_dir + "/weight_dumps/" + date + "_" + best_reward_s + ".hkl"), mode='w')

        print ('The best Reward was:',best_reward)

        # Information Text File
        file = open((current_dir + "/information/" + date + "_weight_run_" + best_reward_s + ".txt"), "w")
        file.write(("Corresponding Parameter Set: " + load_parameters + "\nWeight run from " + date + " with Reward " + best_reward_s + " and " + episodes + " Episodes. NeuronalCircuit_v3"))
        file.close()

        print("--- %s seconds ---" % (time.time() - start_time))

    return date, best_reward_s

#-------------------------------------------------------------------------------------------


if __name__=="__main__":
    main()
