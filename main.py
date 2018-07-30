"""
MAIN FILE in the "BA" Neuronal Network Repositoy

CALL BY:    <main.py>

RETURN:     -

INFO:       This Git-Repository holds all the Code written for my Bachelor Thesis at the Chair of Automatic Control at TF Uni Kiel.
            The Programming Language is Python.

            In this Main-Function, modules are being called and reviewed.
"""

from modules import random_search as rs
from modules import random_search_v2 as rs2
from modules import weights_nn as w

from modules import visiualize as vs
from modules import inspect

def main():

    #best_reward_s = str(int(best_reward_s))

    # RANDOM SEARCH
    #date, best_reward_s = rs.main(10000) # Calling the RANDOM SEARCH Module to calculate new matrices with x Episodes
    #call_matrices = "parameter_dumps/" + date + "_rs_" + best_reward_s + ".p"
    #vs.main(call_matrices) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices

    # RANDOM SEARCH V2
    date, best_reward_s = rs2.main(10000)
    load_parameters = "parameter_dumps/" + date + "_rs2_" + best_reward_s + ".p"
    #vs.main(call_matrices) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices

    # WEIGHT APPLICATION (RandomSearch)
    #load_parameters = "parameter_dumps/20180730_14-29-29_rs2_69.p"
    date, best_reward_s = w.main(10000, load_parameters)
    weight_matrices = "weight_dumps/" + date + "_" + best_reward_s + ".p"
    #weight_matrices = "weight_dumps/20180730_16-31-18_150.p"
    vs.main_with_weights(load_parameters, weight_matrices) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices

    # GENETIC ALGORITHMS
    #...

    #-----------------------------------------------------------------------------------------------------


    # REWARD: 30
    #call_matrices = "parameter_dumps/result_matrices.p"

    #REWARD: 32
    #call_matrices = "parameter_dumps/20180716_16-53-19_result_matrices_reward_32.p"

    #REWARD: 69
    #call_matrices = "parameter_dumps/20180730_14-29-29_rs2_69.p"

    #vs.main(call_matrices) # Callig the VISIUALIZATION Module to show the newly learned paramteter matrices

    # INSPECT FUNCTION------------------------------------------------------------------------------------
    # Parameters of RandomSearch Module:
    #inspect.main(call_matrices)

    # Parameters of Weight Module:
    inspect.weights(weight_matrices)


if __name__=="__main__":
    main()
