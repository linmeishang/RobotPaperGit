# %%
import os
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
import lhsmdu
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
k = lhsmdu.sample(6, 200) # Latin Hypercube Sampling with multi-dimensional uniformity 
print(k.shape) # (6, 200) # This will generate a nested list with 6 variables, with 200 samples each.
k_trans = k.transpose()
print(k_trans)


#%%
for i, k in zip(unique_id, range(len(unique_id))):  # number of id

    print(k, i)

    df_ws = df_ws_total[df_ws_total['_id'] == i]
    df_gm = df_gm_total[df_gm_total['_id'] == i] 

    # loading the farm characteristics of this farm id
    farmingType = df_gm.iloc[0]['farmingType']
    crop = df_gm.iloc[0]['crop']
    system = df_gm.iloc[0]['system']
    section = df_gm.iloc[0]['section']
    size = df_gm.iloc[0]['size']

    Yield = df_gm.iloc[0]['yield'] # cannot use "yield" because it has a special function in python
    mechanisation = df_gm.iloc[0]['mechanisation']

    distance = df_gm.iloc[0]['distance']

    # create a empty data frame "simulation" to store the results
    simulation = pd.DataFrame()

    for j in k_trans[0:1]:
        
        total_weeding_area = j.item(0)*(300-100) + 100
        setup_time_per_plot = j.item(1)*(1-0.16) + 0.16 
        setup_time = setup_time_per_plot/size
        repaire_energy_cost = j.item(2)*(56-14) + 14 
        herbicide_saving =  j.item(3)*(1-0.5) + 0.5 
        supervision_ratio = j.item(4)*(1-0) + 0 
        supervision_time = supervision_ratio*3.7
        supervision_setup_wage = j.item(5)*(42-13.25)+ 13.25  
        unskilled_labor_wage = 13.25
    

        # Step 1: calculate gross profit and profit for baseline using the new wage of unskilled labor
        # replace variable labor cost
        df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'price'] = unskilled_labor_wage
        variable_labor_time = df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'amount']
        df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time * unskilled_labor_wage

        # pivot df_gm into df_baseline
        df_baseline = pd.pivot_table(df_gm, values='total', index = 'grossMarginCategory', aggfunc=np.sum)

        grossProfit_baseline = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
        netProfit_baseline = grossProfit_baseline - df_baseline.loc['fixCosts']
        # print('netProfit_baseline:', netProfit_baseline)
        

        def func(price):
            
            df_ws = df_ws_total[df_ws_total['_id'] == i]
            df_gm = df_gm_total[df_gm_total['_id'] == i] 

            # farmingType = df_gm.iloc[0]['farmingType']
            # crop = df_gm.iloc[0]['crop']
            # system = df_gm.iloc[0]['system']
            # section = df_gm.iloc[0]['section']
            # size = df_gm.iloc[0]['size']
            # Yield = df_gm.iloc[0]['yield']
            # mechanisation = df_gm.iloc[0]['mechanisation']
            # distance = df_gm.iloc[0]['distance']

        
            ######################################################################################################################
            # Step 1: calculate gross profit and profit for baseline using the new wage of unskilled labor
            # replace variable labor cost
            df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'price'] = unskilled_labor_wage
            variable_labor_time = df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'amount']
            df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time * unskilled_labor_wage

            # pivot df_gm into df_baseline
            df_baseline = pd.pivot_table(df_gm, values='total', index = 'grossMarginCategory', aggfunc=np.sum)

            grossProfit_baseline = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
            netProfit_baseline = grossProfit_baseline - df_baseline.loc['fixCosts']
            # print('netProfit_baseline:', netProfit_baseline)



            
            ######################################################################################################################
        
            # Step 2: replace related procedures with robot
            # loading robot parameters
            time = setup_time + supervision_time
            deprec = price/total_weeding_area 
            interest = deprec * 0.3
            others =  deprec * 0.002
            maintenance = repaire_energy_cost


            # copy the value of row 'Anbaupflanzenschutzspritze' or 'Anhängepflanzenschutzspritze'
            # but this new row does not belong to the df
            new_df_1=df_ws[df_ws['description'].str.contains('Anbaupflanzenschutzspritze')]
            new_df_2=df_ws[df_ws['description'].str.contains('Anhängepflanzenschutzspritze')]
            
            # select the new df that is not empty
            if new_df_1.shape[0] > 0:
                new_df = new_df_1
            else:
                new_df = new_df_2
            # print(i)
            # print(new_df.shape)


            # Adding a row of "robot" into working steps
            df_ws.loc['robot_1'] = {'description': 'Robot_1', 
                                'time': time, 
                                'deprec': deprec, 
                                'interest': interest, 
                                'others': others, 
                                'maintenance': maintenance}

            df_ws.loc['robot_2'] = {'description': 'Robot_1', 
                                'time': time, 
                                'deprec': deprec, 
                                'interest': interest, 
                                'others': others, 
                                'maintenance': maintenance}


            a = ['time', 'fuelCons', 'deprec', 'interest', 'others', 'maintenance', 'lubricants', 'services']
            c = [0, 0, 0, 0, 0, 0, 0, 0]

            if new_df_1.shape[0] > 0:
                df_ws.loc[df_ws['description'].str.contains('Anbaupflanzenschutzspritze', na = False), a] = c
            else:
                df_ws.loc[df_ws['description'].str.contains('Anhängepflanzenschutzspritze', na = False), a] = c

    
            # Attention: if new_df.shape[0] == 3, it means we have replace the fungicide cost with 0 too, so now we put it back. 
            # # new_df.shape[0] == 2, this means no fungicide is used. 
            if new_df.shape[0] == 3:
                df_ws.loc['fungicide'] = new_df.iloc[2]


                
            # print(df_ws)

            ######################################################################################################################
            # Step 3: calculate variable machine cost and fixed machine cost with robot

            variable_machine_cost = df_ws['maintenance'].sum() + df_ws['lubricants'].sum()
            fixed_machine_cost = df_ws['deprec'].sum() + df_ws['interest'].sum() + df_ws['others'].sum()
            # print("variable_machine_cost:", variable_machine_cost)
            # print("fixed_machine_cost:", fixed_machine_cost) 


            variable_labor_time = 0
            robot_time = 2*time
            fixed_labor_time = df_ws['time'].sum() - variable_labor_time - robot_time



            ######################################################################################################################
            # Step 4: calculate gross profit and net profit with robot
            # replace cost of Herbizid
            # copy the old cost of herbizid
            new_df = df_gm[df_gm['figure'].str.contains('Herbizid')]
            herbi_cost = new_df['total'].values[0]


            df_gm.loc[df_gm['figure'].str.contains('Herbizid'), 'total'] = herbi_cost * (1-herbicide_saving)



            # replace variable machine cost and fixed machine cost
            df_gm.loc[df_gm['figure'].str.contains('Variable Maschinenkosten'), 'total'] = variable_machine_cost
            df_gm.loc[df_gm['figure'].str.contains('Fixe Maschinenkosten'), 'total'] = fixed_machine_cost


            # replace variable labor cost
            df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'amount'] = variable_labor_time
            df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'total'] = variable_labor_time * unskilled_labor_wage  +  robot_time * supervision_setup_wage


            # replace fixed labor time and cost  
            df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'amount'] = fixed_labor_time
            fixed_labor_wage = df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'price']
            df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'total'] = fixed_labor_time * fixed_labor_wage


            # Calculate gross profit and net profit
            df_robot = pd.pivot_table(df_gm, values='total', index = 'grossMarginCategory', aggfunc=np.sum)
            
            grossProfit_robot = df_robot.loc['revenues'] - df_robot.loc['directCosts'] - df_robot.loc['variableCosts']
            netProfit_robot = grossProfit_robot - df_robot.loc['fixCosts']
            



            ######################################################################################################################
            # Step 5: calculate the differences between robot and baseline

            difference_grossProfit = grossProfit_robot - grossProfit_baseline
            difference_netProfit = netProfit_robot - netProfit_baseline

            # print('difference_grossProfit:', difference_grossProfit)
            # print('difference_netProfit:', difference_netProfit)

            return difference_netProfit

        root = fsolve(func, 1000) # 1000 is the starting point
        # print(root)

        df_res = pd.DataFrame({'price': root, 'total_weeding_area': total_weeding_area,
                'setup_time_per_plot': setup_time_per_plot, 'repaire_energy_cost': repaire_energy_cost, 
                'supervision_ratio': supervision_ratio,
                'supervision_time': supervision_time, 
                'supervision_setup_wage': supervision_setup_wage,
                
                'herbicide_saving': herbicide_saving,
                'grossProfit_baseline': grossProfit_baseline, 'netProfit_baseline': netProfit_baseline, 
                'farmingType': farmingType, 'crop': crop, 'system': system,
                'section': section, 'size': size, 'yield': Yield, 
                'mechanisation': mechanisation, 'distance': distance,                          
                'id': i}) 


    	    # 'grossProfit_robot': grossProfit_robot, 'netProfit_robot': netProfit_robot, 'difference_grossProfit': difference_grossProfit, 'difference_netProfit': difference_netProfit, 

        # print('df_res:', df_res.shape)

        simulation = pd.concat([simulation,df_res])
        # print(simulation)

    # Save the simulation results of each farm id into one excel
    filename = 'LHS_WTP_sugarbeet_conv_'+ str(k)
    simulation.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\\'+filename+'.xlsx')
    # Save robot parameters and differences into an excel

    
# %%
