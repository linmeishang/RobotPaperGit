# %%
import sqlite3
import pandas as pd
import copy
import numpy as np
import random
from random import randint
from numpy import sqrt, array
import os
#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Data'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

# load the dataset
df_gm_total = pd.read_excel('sugarbeet_conv_gm.xlsx', index_col=0)

#%%
unique_id = df_gm_total._id.unique()
print(len(unique_id))


#%%
Cost_df = pd.DataFrame()
# Seperate the big df_ws in to many small dfs based on _id ()
for i in unique_id[0:]:  # number of id
    
    print(i)

    df_gm = df_gm_total[df_gm_total['_id'] == i] 
    # print(df_gm)
    
    # loading the farm characteristics of this farm id
    farmingType = df_gm.iloc[0]['farmingType']
    crop = df_gm.iloc[0]['crop']
    system = df_gm.iloc[0]['system']
    section = df_gm.iloc[0]['section']
    size = df_gm.iloc[0]['size']
    Yield = df_gm.iloc[0]['yield']
    mechanisation = df_gm.iloc[0]['mechanisation']
    distance = df_gm.iloc[0]['distance']

    # Load each type of cost
    revenues = df_gm.loc[df_gm['grossMarginCategory'].str.contains('revenues'), 'total'].values[0]
    variable_machine_costs = df_gm.loc[df_gm['figure'].str.contains('Variable Maschinenkosten'), 'total'].values[0]
    variable_labor_costs = df_gm.loc[df_gm['figure'].str.contains('Variable Lohnkosten'), 'total'].values[0]
    fix_machine_costs  = df_gm.loc[df_gm['figure'].str.contains('Fixe Maschinenkosten'), 'total'].values[0]
    fix_labor_costs = df_gm.loc[df_gm['figure'].str.contains('Fixe Lohnkosten'), 'total'].values[0]


    # pivot df_gm into df_baseline
    df_baseline = pd.pivot_table(df_gm, values='total', index = 'grossMarginCategory', aggfunc=np.sum)
    direct_costs = df_baseline.loc['directCosts']
    variable_costs = df_baseline.loc['variableCosts'] 
    fix_costs = df_baseline.loc['fixCosts']
    
    # grossProfit_baseline = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
    grossProfit = df_baseline.loc['revenues'] - df_baseline.loc['directCosts'] - df_baseline.loc['variableCosts']
    
    netProfit = grossProfit - df_baseline.loc['fixCosts']
        # print('netProfit_baseline:', netProfit_baseline)

            

    df_res = pd.DataFrame({'revenue': revenues, 'direct_costs': direct_costs, 'variable_costs': variable_costs, 
            'variable_machine_costs': variable_machine_costs, 'variable_labor_costs': variable_labor_costs,
            'fix_costs': fix_costs, 'fix_machine_costs': fix_machine_costs, 'fix_labor_costs': fix_labor_costs,
            'grossProfit': grossProfit, 'netProfit': netProfit, 
            'farmingType': farmingType, 'crop': crop, 'system': system,
            'section': section, 'size': size, 'yield': Yield, 
            'mechanisation': mechanisation, 'distance': distance,                          
            'id': i}) 


    Cost_df = pd.concat([Cost_df,df_res])


filename = 'Cost_sugarbeet_conv'
Cost_df.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\\'+filename+'.xlsx')
# Save robot parameters and differences into an excel

# %%
