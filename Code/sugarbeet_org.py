# %%
import sqlite3
import pandas as pd
import copy
import numpy as np
import random
from random import randint
from numpy import sqrt, array
from scipy import optimize
from scipy.optimize import fsolve
import os
import lhsmdu
import pickle
from pickle import dump
import copy

#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Data'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

# load the dataset
df_ws_total = pd.read_excel('sugarbeet_org_ws.xlsx', index_col=0)
df_gm_total = pd.read_excel('sugarbeet_org_gm.xlsx', index_col=0)

#%%
unique_id = df_ws_total._id.unique()
print(len(unique_id)) # 1715 for the full dataset (but we only use 49)

unique_id = df_gm_total._id.unique()
print(len(unique_id)) # 1715 for the full dataset (but we only use 49)

#%%
# LHS for 7 dimensions
# k = lhsmdu.sample(7, 200) # Latin Hypercube Sampling with multi-dimensional uniformity 
# print(k.shape) #  This will generate a nested list with 7 variables, with X samples each.
# k_trans = k.transpose()
# # print(k_trans)
# dump(k_trans, open('k_trans.pkl', 'wb'))

#%%
# Random Monte Carlo simulation generating N data points of 7 dimension (i.e. number of variables)
np.random.seed(1)
n = np.random.rand(4000, 7)
dump(n, open('n_org_1_new.pkl', 'wb'))
print(n)

#%% Define the function that is used to derive the "price" that makes the function = 0, i.e. net profit differencen = 0
def Breakeven(price):
    
    ######################################################################################################################
    # Step 1: calculate gross profit and profit for baseline using the new wage of unskilled labor
    # replace variable labor cost
    df_gm_base = copy.deepcopy(df_gm)
    
    df_gm_base.loc[df_gm_base['figure'].str.contains('Variable Lohnkosten'), 'price'] = unskilled_labor_wage
    variable_labor_time_baseline = df_gm_base.loc[df_gm_base['figure'].str.contains('Variable Lohnkosten'), 'amount']
    df_gm_base.loc[df_gm_base['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time_baseline * unskilled_labor_wage

    # pivot df_gm into df_baseline
    df_baseline = pd.pivot_table(df_gm_base, values='total', index = 'grossMarginCategory', aggfunc=np.sum)

    # Gross profit and net profit
    grossProfit_baseline = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
    netProfit_baseline = grossProfit_baseline - df_baseline.loc['fixCosts']
    # print('grossProfit_baseline:', grossProfit_baseline)
    # print('netProfit_baseline:', netProfit_baseline)


    ######################################################################################################################
    # Step 2: Replace related procedures with robot
    df_ws_robot = copy.deepcopy(df_ws)
    df_gm_robot = copy.deepcopy(df_gm)
    
    # loading robot parameters
    time = setup_time + supervision_time
    deprec = price/total_weeding_area
    interest = deprec * 0.3
    others =  deprec * 0.1
    maintenance = repaire_energy_cost

    # copy the value of row 'Anbaupflanzenschutzspritze' or 'Anhängepflanzenschutzspritze'(but this new row does not belong to the df)
    new_df = df_ws_robot[df_ws_robot['name'].str.contains('Handhacke', na = False)]
    # print('original hand hacke costs:', new_df)
    
    # Adding a row of "robot" into working steps
    robot_dict = {'description': '2 times Robotic weeding',
                'time': time*2,
                'deprec': deprec*2, 
                'interest': interest*2, 
                'others': others*2, 
                'maintenance': maintenance*2}
    
    df_ws_robot.loc['robot'] = pd.Series(robot_dict)

    
    
    a = ['time', 'fuelCons', 'deprec', 'interest', 'others', 'maintenance', 'lubricants', 'services']

    # if not enough weeding efficiency
    c = [new_df.iloc[0]['time']*(1-weeding_efficiency), new_df.iloc[0]['fuelCons']*(1-weeding_efficiency),
        new_df.iloc[0]['deprec']*(1-weeding_efficiency), new_df.iloc[0]['interest']*(1-weeding_efficiency), 
        new_df.iloc[0]['others']*(1-weeding_efficiency), new_df.iloc[0]['maintenance']*(1-weeding_efficiency),
        new_df.iloc[0]['lubricants']*(1-weeding_efficiency), new_df.iloc[0]['services']*(1-weeding_efficiency)]
    
    d = [new_df.iloc[1]['time']*(1-weeding_efficiency), new_df.iloc[1]['fuelCons']*(1-weeding_efficiency),
        new_df.iloc[1]['deprec']*(1-weeding_efficiency), new_df.iloc[1]['interest']*(1-weeding_efficiency), 
        new_df.iloc[1]['others']*(1-weeding_efficiency), new_df.iloc[1]['maintenance']*(1-weeding_efficiency), 
        new_df.iloc[1]['lubricants']*(1-weeding_efficiency), new_df.iloc[1]['services']*(1-weeding_efficiency)]
    

    # Note it should be 'Handhacke (1. Hacke)', but python do not accept space, this way also works
    df_ws_robot.loc[df_ws_robot['name'].str.contains('Handhacke', na=False), a] = c 
    df_ws_robot.loc[df_ws_robot['name'].str.contains('Reihenschlu', na=False), a] = d
    # print(df_ws_robot['time']) # to check if the df_ws_robot is correct
    
    # Step 3: calculate variable machine cost and fixed machine cost with robot
    variable_machine_cost = df_ws_robot['maintenance'].sum() + df_ws_robot['lubricants'].sum()
    fixed_machine_cost = df_ws_robot['deprec'].sum() + df_ws_robot['interest'].sum() + df_ws_robot['others'].sum()
    # print('variable_machine_cost:', variable_machine_cost)
    # print('fixed_machine_cost:', fixed_machine_cost) 
    
    handhacke_df = df_ws_robot[df_ws_robot['name'].str.contains('Handhacke', na = False)]
    # print('new_handhacke_df:', handhacke_df)
    variable_labor_time = handhacke_df['time'].sum()/9*8
    robot_time = 2*time
    fixed_labor_time = df_ws_robot['time'].sum() - variable_labor_time - robot_time
    # print('variable_labor_time:', variable_labor_time)
    # print('robot_time:', robot_time)
    # print('fixed_labor_time:', fixed_labor_time)

    # Step 4: calculate gross profit and net profit with robot
    # replace variable machine cost and fixed machine cost    
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Variable Maschinenkosten'), 'total'] = variable_machine_cost
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Fixe Maschinenkosten'), 'total'] = fixed_machine_cost
   
    # replace variable labor cost
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time * unskilled_labor_wage  +  robot_time * supervision_setup_wage
    # print('Variable Lohnkosten:', df_gm_robot.loc[df_gm_robot['figure'].str.contains('Variable Lohnkosten'), 'total'])
    
    # replace fixed labor cost
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Fixe Lohnkosten'), 'total'] = fixed_labor_time * 21


    # ##### No problem here after #########################
    # Calculate gross profit and net profit
    df_robot = pd.pivot_table(df_gm_robot, values='total', index = 'grossMarginCategory', aggfunc=np.sum)
    # print(df_robot)

    grossProfit_robot = df_robot.loc['revenues'] - df_robot.loc['directCosts'] - df_robot.loc['variableCosts']
    netProfit_robot = grossProfit_robot - df_robot.loc['fixCosts']

    # print("grossProfit_robot:", grossProfit_robot)
    # print("netProfit_robot:", netProfit_robot)

    ######################################################################################################################
    # Step 5: calculate the differences between robot and baseline      
    difference_netProfit = netProfit_robot - netProfit_baseline
    # print('difference_grossProfit:', difference_grossProfit)
    # print('difference_netProfit:', difference_netProfit)

    return difference_netProfit


#%%
# loop over the 49 farm ids: for each farm id, we solve the the equation for many times
# Seperate the big df_ws in to many small dfs based on _id ()
for i, k in zip(unique_id[0:], range(0, len(unique_id))):  # number of id
    
    print(k, i)
    # Load the working step (df_ws) and gross margin (df_gm) based on the id
    df_ws = df_ws_total[df_ws_total['_id'] == i]
    df_gm = df_gm_total[df_gm_total['_id'] == i] 

    # loading the farm characteristics of this farm id
    size = df_gm.iloc[0]['size']
    mechanisation = df_gm.iloc[0]['mechanisation']
    # print(size, mechanisation)
    
    # Store simulation data in a dataframe called "simulation"
    simulation = pd.DataFrame()

    # Assign the random results to each variable:
    for j in n[0:]: 
      
        size = size
        mechanisation = mechanisation
        total_weeding_area = j.item(0)*(600-200) + 200 # changed to 200-600
        setup_time_per_plot = j.item(1)*(2-0.16) + 0.16  # changed to 2 hours max
        setup_time = setup_time_per_plot/size
        repaire_energy_cost = j.item(2)*(56-14) + 14 
        weeding_efficiency =  j.item(3)*(1-0.5) + 0.5 
        supervision_ratio = j.item(4)*(1-0) + 0 
        supervision_time = supervision_ratio*3.2
        supervision_setup_wage = j.item(5)*(42-21)+ 21 # changed to 21-42
        unskilled_labor_wage = j.item(6)*(21-13.25) + 13.25
        
        root = fsolve(Breakeven, 20000) # Breakeven = 0, 20000 is the initial value

        # Store the results
        df_res = pd.DataFrame({'price': root, 'total_weeding_area': total_weeding_area,
                'setup_time_per_plot': setup_time_per_plot, 'repaire_energy_cost': repaire_energy_cost, 
                'weeding_efficiency': weeding_efficiency, 
                'supervision_ratio': supervision_ratio,
                'supervision_time': supervision_time, 
                'supervision_setup_wage': supervision_setup_wage,
                'unskilled_labor_wage': unskilled_labor_wage, 
                'size': size,  
                'mechanisation': mechanisation,                         
                'id': i}) 
        

        # Concat the result of one solve into the big "simulation" dataframe 
        simulation = pd.concat([simulation,df_res])
        # print(simulation)
    
    # Save the simulation dataframe (containing N solves) 
    path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet'
    os.chdir(path)
    print("Current Working Directory " , os.getcwd())
    
    filename = 'WTP_sugarbeet_org_'+ str(k)
    dump(simulation, open('{0}.pkl'.format(filename), 'wb'))
    
    
    # If you want to save in excel
    # simulation.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\\'+filename+'.xlsx')

# %%
