"""
MAIN FILE in the "BA" Neuronal Network Repositoy - FOR CMD USE WITHOUT GUI AND VISIUALIZATION

CALL BY:    <main_cmd.py>

RETURN:     -

INFO:       This Git-Repository holds all the Code written for my Bachelor Thesis at the Chair of Automatic Control at TF Uni Kiel.
            The Programming Language is Python.

            In this Main-Function, modules are being called and reviewed.
"""

from modules import random_search as rs
from modules import random_search_v2 as rs2
from modules import weights_nn as w
from modules import genetic_algorithm as ga
from modules import inspect_nn as ins
from modules import parameters

import numpy as np



def main():
    global parameter_matrices, weight_matrices

    reward_arr = np.array([])

    vis_runtime = 5 # in sec. - FOR VISIUALIZATION

    sim_time_parameters = 5 # FOR SIMULATION of Parameters
    sim_time_genetic = 60 # FOR SIMULATION of Genetic Algorithm
    sim_time_weights = 5 # FOR SIMULATION of additional Weights

    # Simulation time in HOURS ------------------------------
    #sim_time_parameters = sim_time_parameters * 60 * 60
    #sim_time_weights = sim_time_weights * 60 * 60
    #--------------------------------------------------------
    # Simulation time in MINUTES ----------------------------
    #sim_time_parameters = sim_time_parameters * 60
    #sim_time_weights = sim_time_weights * 60
    #--------------------------------------------------------

    # RANDOM SEARCH V2
    #date, best_reward_p = rs2.main(sim_time_parameters)
    #parameter_matrices = parameters.current_dir + "/parameter_dumps/" + date + "_rs2_v2_" + best_reward_p + ".hkl"

    # WEIGHT APPLICATION (RandomSearch)
    #date, best_reward_w = w.main(sim_time_weights, parameter_matrices, best_reward_p)

    # GENETIC Algorithms
    date, best_reward_g = ga.main(sim_time_genetic,1) # ga.main(SIMULATION TIME, PLOT<0=no,1=yes>)
    #for i in range(10):
    #    date, best_reward_g = ga.main(sim_time_genetic,0) # ga.main(SIMULATION TIME, PLOT<0=no,1=yes>)
    #    reward_arr = np.append(reward_arr, best_reward_g)
    #print (reward_arr)

    # Simulation 15.08.2018 - symmetrical Parameters
    #parameter_matrices = parameters.current_dir + "/parameter_dumps/20180817_01-50-02_rs2_v2_158.hkl"
    #parameter_matrices = parameters.current_dir + "/parameter_dumps/20180817_01-52-01_rs2_v2_182.hkl"
    #parameter_matrices = parameters.current_dir + "/parameter_dumps/20180817_01-54-01_rs2_v2_104.hkl"
    #parameter_matrices = parameters.current_dir + "/parameter_dumps/20180817_01-56-01_rs2_v2_131.hkl" #Bisher hoechster Satz

    #weight_matrices = parameters.current_dir + "/weight_dumps/20180817_13-50-02_200.hkl"
    #weight_matrices = parameters.current_dir + "/weight_dumps/20180817_13-52-01_200.hkl"
    #weight_matrices = parameters.current_dir + "/weight_dumps/20180817_13-54-01_200.hkl"
    #weight_matrices = parameters.current_dir + "/weight_dumps/20180817_13-56-01_200.hkl"

    # Visiualize only the Parameter Simulation:
    #vs.main(parameter_matrices, vis_runtime) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices

    # WEIGHT APPLICATION (RandomSearch)
    #date, best_reward_w = w.main(sim_time_weights, parameter_matrices, best_reward_p)
    #if best_reward_p <= best_reward_w:
    #    weight_matrices = parameters.current_dir + "/weight_dumps/" + date + "_" + best_reward_w + ".hkl"
    #    vs.main_with_weights(parameter_matrices, weight_matrices, vis_runtime) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices
    #else:
    #    vs.main(parameter_matrices, vis_runtime) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices


if __name__=="__main__":
    main()
