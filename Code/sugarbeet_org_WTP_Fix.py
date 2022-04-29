﻿# %%
import sqlite3
import pandas as pd
import copy
import numpy as np
import random
from random import randint
from sympy import symbols, Eq, solve
from numpy import sqrt, array
from scipy.optimize import fixed_point
from scipy import optimize
from scipy.optimize import fsolve
# from scipy.stats import qmc
# import scipy.stats.qmc
import os
import lhsmdu

import pickle
from pickle import dump

#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Data'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

# load the dataset
df_ws_total = pd.read_excel('sugarbeet_org_ws.xlsx', index_col=0)
df_gm_total = pd.read_excel('sugarbeet_org_gm.xlsx', index_col=0)

#%%
unique_id = df_ws_total._id.unique()
print(len(unique_id)) # 1715

unique_id = df_gm_total._id.unique()
print(len(unique_id)) # 1715

#%%
# LHS for 7 dimensions
# k = lhsmdu.sample(7, 200) # Latin Hypercube Sampling with multi-dimensional uniformity 
# print(k.shape) #  This will generate a nested list with 7 variables, with X samples each.
# k_trans = k.transpose()
# # print(k_trans)
# dump(k_trans, open('k_trans.pkl', 'wb'))


#%%
# Random Monte Carlo simulation
N = np.random.rand(7, 1000)
N_trans = N.transpose()
print(N_trans.shape)
dump(N_trans, open('N_trans.pkl', 'wb'))


#%% Define the function that is used to derive the "price" that makes the function = 0, i.e. net profit differencen = 0

def func(price):
    ######################################################################################################################
    # Step 1: calculate gross profit and profit for baseline using the new wage of unskilled labor
    # replace variable labor cost
    df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'price'] = unskilled_labor_wage
    variable_labor_time = df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'amount']
    df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time * unskilled_labor_wage

    # pivot df_gm into df_baseline
    df_baseline = pd.pivot_table(df_gm, values='total', index = 'grossMarginCategory', aggfunc=np.sum)

    # Gross profit and net profit
    grossProfit_baseline = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
    netProfit_baseline = grossProfit_baseline - df_baseline.loc['fixCosts']
    # print('netProfit_baseline:', netProfit_baseline)

    ######################################################################################################################
    # Step 2: Replace related procedures with robot
    # loading robot parameters
    time = setup_time + supervision_time
    deprec = price/total_weeding_area 
    interest = deprec * 0.3
    others =  deprec * 0.002
    maintenance = repaire_energy_cost

    # copy the value of row 'Anbaupflanzenschutzspritze' or 'Anhängepflanzenschutzspritze'(but this new row does not belong to the df)
    new_df = df_ws[df_ws['name'].str.contains('Handhacke', na = False)]
    # print('original hand hacke costs:', new_df)
    
    # Adding a row of "robot" into working steps
    df_ws.loc['robot_1'] = {'description': 'Robot_1', 
                        'time': time, 
                        'deprec': deprec, 
                        'interest': interest, 
                        'others': others, 
                        'maintenance': maintenance}

    df_ws.loc['robot_2'] = {'description': 'Robot_2', 
                        'time': time, 
                        'deprec': deprec, 
                        'interest': interest, 
                        'others': others, 
                        'maintenance': maintenance}   
    
    # Calculate the cost caused by a non perfect (100%) weeding efficiency 
    a = ['time', 'fuelCons', 'deprec', 'interest', 'others', 'maintenance', 'lubricants', 'services']

    c = [new_df.iloc[0]['time']*(1-weeding_efficiency), new_df.iloc[0]['fuelCons']*(1-weeding_efficiency),
        new_df.iloc[0]['deprec']*(1-weeding_efficiency), new_df.iloc[0]['interest']*(1-weeding_efficiency), 
        new_df.iloc[0]['others']*(1-weeding_efficiency), new_df.iloc[0]['maintenance']*(1-weeding_efficiency),
        new_df.iloc[0]['lubricants']*(1-weeding_efficiency), new_df.iloc[0]['services']*(1-weeding_efficiency)]

    d = [new_df.iloc[1]['time']*(1-weeding_efficiency), new_df.iloc[1]['fuelCons']*(1-weeding_efficiency),
        new_df.iloc[1]['deprec']*(1-weeding_efficiency), new_df.iloc[1]['interest']*(1-weeding_efficiency), 
        new_df.iloc[1]['others']*(1-weeding_efficiency), new_df.iloc[1]['maintenance']*(1-weeding_efficiency), 
        new_df.iloc[1]['lubricants']*(1-weeding_efficiency), new_df.iloc[1]['services']*(1-weeding_efficiency)]


    # Note it should be 'Handhacke (1. Hacke)', but python do not accept space, this way also works
    df_ws.loc[df_ws['name'].str.contains('Handhacke', na=False), a] = c 
    df_ws.loc[df_ws['name'].str.contains('Reihenschlu', na=False), a] = d

    ######################################################################################################################
    # Step 3: calculate variable machine cost and fixed machine cost with robot
    variable_machine_cost = df_ws['maintenance'].sum() + df_ws['lubricants'].sum()
    fixed_machine_cost = df_ws['deprec'].sum() + df_ws['interest'].sum() + df_ws['others'].sum()
    # print('variable_machine_cost:', variable_machine_cost)
    # print('fixed_machine_cost:', fixed_machine_cost) 

    handhacke_df = df_ws[df_ws['name'].str.contains('Handhacke', na = False)]
    # print('new_handhacke_df:', handhacke_df)

    variable_labor_time = handhacke_df['time'].sum()/9*8
    robot_time = 2*time
    fixed_labor_time = df_ws['time'].sum() - variable_labor_time - robot_time
    # print('variable_labor_time:', variable_labor_time)
    # print('robot_time:', robot_time)
    # print('fixed_labor_time:', fixed_labor_time)  

    ######################################################################################################################
    # Step 4: calculate gross profit and net profit with robot
    # replace variable machine cost and fixed machine cost
    df_gm.loc[df_gm['figure'].str.contains('Variable Maschinenkosten'), 'total'] = variable_machine_cost
    df_gm.loc[df_gm['figure'].str.contains('Fixe Maschinenkosten'), 'total'] = fixed_machine_cost

    # replace variable labor cost
    df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'amount'] = variable_labor_time # robot time is missing here, but it does not matter because it is added below in the "total"
    df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time * unskilled_labor_wage  +  robot_time * supervision_setup_wage

    # replace fixed labor time and cost  
    df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'amount'] = fixed_labor_time
    fixed_labor_wage = df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'price']
    df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'total'] = fixed_labor_time * fixed_labor_wage

    # Calculate gross profit and net profit
    df_robot = pd.pivot_table(df_gm, values='total', index = 'grossMarginCategory', aggfunc=np.sum)
    # print(df_robot)

    # variable_costs_robot = df_robot.loc['variableCosts'].values[0]
    # print(variable_costs_robot)

    # fixed_costs_robot = df_robot.loc['fixCosts'].values[0]
    # print(fixed_costs_robot)

    grossProfit_robot = df_robot.loc['revenues'] - df_robot.loc['directCosts'] - df_robot.loc['variableCosts']
    netProfit_robot = grossProfit_robot - df_robot.loc['fixCosts']

    ######################################################################################################################
    # Step 5: calculate the differences between robot and baseline
    difference_grossProfit = grossProfit_robot - grossProfit_baseline
    difference_netProfit = netProfit_robot - netProfit_baseline
    # print('difference_grossProfit:', difference_grossProfit)
    # print('difference_netProfit:', difference_netProfit)

    return difference_netProfit


#%%
# loop over the 49 farm ids: for each farm id, we solve the the equation for many times
# Seperate the big df_ws in to many small dfs based on _id ()
for i, k in zip(unique_id[0:], range(0, len(unique_id))):  # number of id
    
    print(i, k)
    
    # Load the working step (df_ws) and gross margin (df_gm) based on the id
    df_ws = df_ws_total[df_ws_total['_id'] == i]
    df_gm = df_gm_total[df_gm_total['_id'] == i] 

    # loading the farm characteristics of this farm id
    size = df_gm.iloc[0]['size']
    mechanisation = df_gm.iloc[0]['mechanisation']
    
    
    # Store simulation data in a dataframe called "simulation"
    simulation = pd.DataFrame()

    # Assign the random results to each variable:
    for j in N_trans[0:]:
 
        total_weeding_area = j.item(0)*(300-100) + 100
        setup_time_per_plot = j.item(1)*(1-0.16) + 0.16 
        setup_time = setup_time_per_plot/size
        repaire_energy_cost = j.item(2)*(56-14) + 14 
        weeding_efficiency =  j.item(3)*(1-0.5) + 0.5 
        supervision_ratio = j.item(4)*(1-0) + 0 
        supervision_time = supervision_ratio*3.7
        supervision_setup_wage = j.item(5)*(42-13.25)+ 13.25  
        unskilled_labor_wage = j.item(6)*(21-13.25) + 13.25
        
        # Solve the function using the above given parameters
        root = fsolve(func, 5000) # func = 0, 5000 is the initial value to try
        # root the solution
 
        #Store the result of this given combination of parameters
        df_res = pd.DataFrame({'price': root, 'total_weeding_area': total_weeding_area,
                'setup_time_per_plot': setup_time_per_plot, 'repaire_energy_cost': repaire_energy_cost, 
                'weeding_efficiency': weeding_efficiency, 
                'supervision_ratio': supervision_ratio,
                'supervision_time': supervision_time, 
                'supervision_setup_wage': supervision_setup_wage,
                'unskilled_labor_wage': unskilled_labor_wage,
                'grossProfit_baseline': grossProfit_baseline, 'netProfit_baseline': netProfit_baseline, 
                'farmingType': farmingType, 'crop': crop, 'system': system,
                'section': section, 'size': size, 'yield': Yield, 
                'mechanisation': mechanisation, 'distance': distance,                          
                'id': i}) 

    	    # 'grossProfit_robot': grossProfit_robot, 'netProfit_robot': netProfit_robot, 'difference_grossProfit': difference_grossProfit, 'difference_netProfit': difference_netProfit, 

        # Concat the result of one solve into the big "simulation" dataframe 
        simulation = pd.concat([simulation,df_res])
        # print(simulation)
    
    # Save the simulation dataframe (containing N solves) 
    filename = 'Time-LHS_WTP_sugarbeet_org_'+ str(k)
    simulation.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\\'+filename+'.xlsx')

