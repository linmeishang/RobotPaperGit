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
from pickle import dump, load
import copy
#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Data'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

# load the dataset
df_ws_total = pd.read_excel('sugarbeet_conv_ws.xlsx', index_col=0)
df_gm_total = pd.read_excel('sugarbeet_conv_gm.xlsx', index_col=0)

#%%
unique_id = df_ws_total._id.unique()
print(len(unique_id)) # 2401

unique_id = df_gm_total._id.unique()
print(len(unique_id)) # 2401

#%%
# LHS for 6 dimensions
# k = lhsmdu.sample(6, 200) # Latin Hypercube Sampling with multi-dimensional uniformity 
# print(k.shape) #  This will generate a nested list with 7 variables, with X samples each.
# k_trans = k.transpose()
# # print(k_trans)
# dump(k_trans, open('k_trans.pkl', 'wb'))


#%%
# Random Monte Carlo simulation generating N data points of 7 dimension (i.e. number of variables)
np.random.seed(1)
n = np.random.rand(4000, 6)
dump(n, open('n_conv_1_new.pkl', 'wb'))

#%%
def Breakeven(price):
    
    # Step 1: calculate gross profit and profit for baseline
    df_gm_base = copy.deepcopy(df_gm)
    
    # pivot df_gm_base into df_baseline
    df_baseline = pd.pivot_table(df_gm_base, values='total', index = 'grossMarginCategory', aggfunc=np.sum)

    grossProfit_baseline = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
    netProfit_baseline = grossProfit_baseline - df_baseline.loc['fixCosts']
    # print('netProfit_baseline:', netProfit_baseline)


    # Step 2: replace related procedures with robot
    df_ws_robot = copy.deepcopy(df_ws)
    df_gm_robot = copy.deepcopy(df_gm)
    
    # loading robot parameters
    time = setup_time + supervision_time
    deprec = price/total_weeding_area 
    interest = deprec * 0.3
    others =  deprec * 0.1
    maintenance = repaire_energy_cost


    # copy the value of row 'Anbaupflanzenschutzspritze' or 'Anhängepflanzenschutzspritze'
    # but this new row does not belong to the df
    new_df_1=df_ws_robot[df_ws_robot['description'].str.contains('Anbaupflanzenschutzspritze')]
    new_df_2=df_ws_robot[df_ws_robot['description'].str.contains('Anhängepflanzenschutzspritze')]
    
    # select the new df that is not empty
    if new_df_1.shape[0] > 0:
        new_df = new_df_1
    else:
        new_df = new_df_2
    # print(i)
    # print(new_df.shape)
    robot_dict = {'description': '2 times Robotic weeding',
            'time': time*2,
            'deprec': deprec*2, 
            'interest': interest*2, 
            'others': others*2, 
            'maintenance': maintenance*2}
    
    # Adding a row of "robot" into working steps
    df_ws_robot.loc['robot'] = pd.Series(robot_dict)


    a = ['time', 'fuelCons', 'deprec', 'interest', 'others', 'maintenance', 'lubricants', 'services']
    c = [0, 0, 0, 0, 0, 0, 0, 0]

    if new_df_1.shape[0] > 0:
        df_ws_robot.loc[df_ws_robot['description'].str.contains('Anbaupflanzenschutzspritze', na = False), a] = c
    else:
        df_ws_robot.loc[df_ws_robot['description'].str.contains('Anhängepflanzenschutzspritze', na = False), a] = c


    # Attention: if new_df.shape[0] == 3, it means we have replace the fungicide cost with 0 too, so now we put it back. 
    # # new_df.shape[0] == 2, this means no fungicide is used. 
    if new_df.shape[0] == 3:
        df_ws_robot.loc['fungicide'] = new_df.iloc[2]
        
    # print(df_ws_robot)


    ######################################################################################################################
    # Step 3: calculate variable machine cost and fixed machine cost with robot
    variable_machine_cost = df_ws_robot['maintenance'].sum() + df_ws_robot['lubricants'].sum()
    fixed_machine_cost = df_ws_robot['deprec'].sum() + df_ws_robot['interest'].sum() + df_ws_robot['others'].sum()
    # print("variable_machine_cost:", variable_machine_cost)
    # print("fixed_machine_cost:", fixed_machine_cost) 

    robot_time = 2*time
    fixed_labor_time = df_ws_robot['time'].sum() - robot_time

    ######################################################################################################################
    # Step 4: calculate gross profit and net profit with robot
    # replace cost of Herbizid
    # copy the old cost of herbizid
    new_df = df_gm_robot[df_gm_robot['figure'].str.contains('Herbizid')]
    herbi_cost = new_df['total'].values[0]

    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Herbizid'), 'total'] = herbi_cost * (1-herbicide_saving)


    # replace variable machine cost and fixed machine cost
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Variable Maschinenkosten'), 'total'] = variable_machine_cost
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Fixe Maschinenkosten'), 'total'] = fixed_machine_cost


    # replace variable labor cost
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Variable Lohnkosten'), 'total'] = robot_time * supervision_setup_wage


    # replace fixed labor time and cost  
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Fixe Lohnkosten'), 'amount'] = fixed_labor_time
    fixed_labor_wage = df_gm_robot.loc[df_gm_robot['figure'].str.contains('Fixe Lohnkosten'), 'price']
    df_gm_robot.loc[df_gm_robot['figure'].str.contains('Fixe Lohnkosten'), 'total'] = fixed_labor_time * fixed_labor_wage


    # Calculate gross profit and net profit
    df_robot = pd.pivot_table(df_gm_robot, values='total', index = 'grossMarginCategory', aggfunc=np.sum)
    
    grossProfit_robot = df_robot.loc['revenues'] - df_robot.loc['directCosts'] - df_robot.loc['variableCosts']
    netProfit_robot = grossProfit_robot - df_robot.loc['fixCosts']
    
    ######################################################################################################################
    # Step 5: calculate the differences between robot and baseline
    difference_netProfit = netProfit_robot - netProfit_baseline

    # print('difference_grossProfit:', difference_grossProfit)
    # print('difference_netProfit:', difference_netProfit)

    return difference_netProfit

      

#%%
for i, k in zip(unique_id[-1:0], range(len(unique_id))):  # number of id

    print(k, i)

    df_ws = df_ws_total[df_ws_total['_id'] == i]
    df_gm = df_gm_total[df_gm_total['_id'] == i] 

    # loading the farm characteristics of this farm id
    size = df_gm.iloc[0]['size']
    mechanisation = df_gm.iloc[0]['mechanisation']
    # print(size, mechanisation)

    # create a empty data frame "simulation" to store the results
    simulation = pd.DataFrame()

    for j in n[0:]:
        
        total_weeding_area = j.item(0)*(600-200) + 200
        setup_time_per_plot = j.item(1)*(2-0.16) + 0.16 
        setup_time = setup_time_per_plot/size
        repaire_energy_cost = j.item(2)*(56-14) + 14 
        herbicide_saving =  j.item(3)*(1-0.5) + 0.5 
        supervision_ratio = j.item(4)*(1-0) + 0
        supervision_time = supervision_ratio*3.2
        supervision_setup_wage = j.item(5)*(42-21)+ 21  

    
        root = fsolve(Breakeven, 20000) # Breakeven = 0, 20000 is the initial value

        df_res = pd.DataFrame({'price': root, 'total_weeding_area': total_weeding_area,
                'setup_time_per_plot': setup_time_per_plot, 'repaire_energy_cost': repaire_energy_cost, 
                'supervision_ratio': supervision_ratio,
                'supervision_time': supervision_time, 
                'supervision_setup_wage': supervision_setup_wage,
                'herbicide_saving': herbicide_saving,
                'size': size, 
                'mechanisation': mechanisation,                     
                'id': i}) 

        simulation = pd.concat([simulation,df_res])
        # print(simulation)

    path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet'
    os.chdir(path)
    print("Current Working Directory " , os.getcwd())
    
    # Save the simulation results of each farm id into one excel
    filename = 'WTP_sugarbeet_conv_'+ str(k)
    dump(simulation, open('{0}.pkl'.format(filename), 'wb'))
       
    # If you want to save in excel
    # simulation.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\\'+filename+'.xlsx')


# %%
