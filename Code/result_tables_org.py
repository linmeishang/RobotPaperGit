
#%%
import pandas as pd
import glob
from sklearn.utils import shuffle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import itertools
import pickle
from pickle import load
import openpyxl as pxl
from scipy import stats
#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

#%%
# df = pd.read_excel('Time-LHS_WTP_sugarbeet_org_0.xlsx')

all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\*.pkl', recursive=True)
print(all_files)

#%%
df = pd.DataFrame()
for file in all_files:
    if file.endswith('.pkl'):
        
        # df = df.append(pd.read_excel(file)) 
        df = df.append(load(open(file, 'rb')))
        print(df.shape)
        
df.head() 
print(df.shape)

#%%
df.columns
#%%
# df12 = load(open('11_MC_2000_sugarbeet_org_WTP.pkl', 'rb'))
# print(df12)

#%%
a = '1-13_MC'

list_interaction = [['supervision_ratio', 'supervision_setup_wage'], ['unskilled_labor_wage', 'weeding_efficiency']]

list_inter_farmCha = [['size', 'setup_time_per_plot'],
                    ['size', 'mechanisation']]

list_of_variables = ['total_weeding_area', 'setup_time_per_plot','repaire_energy_cost', 
                     'weeding_efficiency', 'supervision_ratio', 
                     'supervision_setup_wage', 'unskilled_labor_wage']

list_of_farmCha = ['size', 'mechanisation']


#%%
All_variables = {}

for i in list_of_variables[0:]:
    
    variable_range = df[i].max() - df[i].min()
    step = variable_range/4
    
    WTP_dict = {}
    
    for j in range(1,5):
        low = df[i].min() + step * (j-1)
        high = df[i].min() + step * j
        print(low, high)

        df_2 = df.loc[df[i].between(low, high, inclusive=True)] 
        print(df_2.shape)
        # df_3 = df_2[(np.abs(stats.zscore(df_2['price'])) < 3)]
        # print(df_3.shape)
        WTP = df_2['price'].mean()
        print(WTP)
        # plt.hist(WTP)
        # plt.show()
        
        WTP_dict[str(j)] = WTP
    
    All_variables[i] = WTP_dict

print(All_variables)    

WTP_df =pd.DataFrame.from_dict(All_variables,orient='index')
print(WTP_df)
WTP_df.to_excel(a+'_WTP_mean.xlsx')


#%%


#%%
# Thomas: WTP Q1-Q4
# Find the min and max of WTP 
WTP_range = df['price'].max() - df['price'].min()
step = WTP_range/4
print(step)

# For each Q_WTP, calculate the average of each variables
Q_dict = {}
    
for j in range(1,5):
    low = df['price'].min() + step * (j-1)
    high = df['price'].min() + step * j
    print(low, high)
    
    Q_df = df.loc[df['price'].between(low, high, inclusive=True)] 
    
    mean_dict = {}
    for k in list_of_variables:
        variable_mean = Q_df[k].mean()
        print(variable_mean)
        mean_dict[str(k)] = variable_mean

    print(mean_dict)
    
    Q_dict[str(j)] = mean_dict
    
Q_WTP_df =pd.DataFrame.from_dict(Q_dict,orient='index')
print(Q_WTP_df)
Q_df_trans = Q_WTP_df.T
Q_df_trans.to_excel(a+'_WTP_Q_mean_Thomas.xlsx')



#%%
# # WTP under different sizes and mechanisation levels
for i in list_of_farmCha:
    
    # find the discret data of this farm characteristics
    unique_values = df[i].unique()
    unique_values = np.sort(unique_values)
    
    WTP_dict = {}
    
    for j in unique_values:
        
        df_2 = df.loc[df[i] == j] 
        WTP = df_2['price'].mean()
        print(WTP)
        
        WTP_dict[str(j)] = WTP 

    WTP_df =pd.DataFrame.from_dict(WTP_dict,orient='index')
    print(WTP_df)
    WTP_df.to_excel(a+'_MC_2-12_WTP_'+i+'.xlsx')
    
    



#%%
# Interaction metrix
param_1 = 'supervision_setup_wage' 
param_2 = 'supervision_ratio'

min_1 = df[param_1].min()
max_1 = df[param_1].max()
print(max_1)
range_1 = max_1 - min_1
step_1 = range_1/4
print(step_1)

min_2 = df[param_2].min()
max_2 = df[param_2].max()
range_2 = max_2 - min_2
step_2 = range_2/4
print(min_2)
print(max_2)
print(step_2)

# take the average of WTP from the selected data
WTP_list = []

for j, k in itertools.product(range(1,5), range(1,5)):
    
    print(j, k)

    low_1 = min_1 + step_1 * (j-1)
    high_1 = min_1 + step_1 * j
    print(param_1, low_1, high_1)

    low_2 = min_2 + step_2 * (k-1)
    high_2 = min_2 + step_2 * k
    print(param_2, low_2, high_2)

    df_2 = df.loc[(df[param_1].between(low_1, high_1, inclusive=True)) & (df[param_2].between(low_2, high_2, inclusive=True))]
    WTP = df_2['price'].mean()
    WTP_list.append(WTP)
    print(WTP_list)

    # reshape list into array and save into dataframe
WTP_array = np.reshape(WTP_list, (4,4))
print(WTP_array)

df = pd.DataFrame(data=WTP_array)

df.to_excel(a+'_Matrix_'+param_1+'_'+param_2+'.xlsx')

#%%


# #%%

# # #%%

# #%%    
# param_1 = 'size' # param_1 must be either "size" or "mechanisation"
# param_2 = 'setup_time_per_plot' # param_2 must be a variable in the list of variables

# # find the discret data of this farm characteristics
# unique_values = df[param_1].unique()
# unique_values = np.sort(unique_values)
    
# min_2 = df[param_2].min()
# max_2 = df[param_2].max()
# range_2 = max_2 - min_2
# step_2 = range_2/4


# # take the average of WTP from the selected data
# WTP_list = []

# for j, k in itertools.product(unique_values, range(1,5)):
    
#     print(j, k)

#     low_2 = min_2 + step_2 * (k-1)
#     high_2 = min_2 + step_2 * k
#     # print(low_2, high_2)

#     df_2 = df.loc[(df[param_1] ==j ) & (df[param_2].between(low_2, high_2, inclusive=True))]
#     WTP = df_2['price'].mean()
#     WTP_list.append(WTP)
#     print(WTP_list)

#     # reshape list into array and save into dataframe
# WTP_array = np.reshape(WTP_list, (len(unique_values),4))
# print(WTP_array)


# df = pd.DataFrame(data=WTP_array)

# df.to_excel(a+'_LHS_1000_Matrix_'+param_1+'_'+param_2+'.xlsx')


# #%%

# # # Here is the code to get the ranges of each variables
# # All_variables = {}

# # for i in list_of_variables:
    
# #     variable_range = df[i].max() - df[i].min()
# #     step = variable_range/4
    
# #     Range_dict = {}
    
# #     for j in range(1,5):
# #         low = df[i].min() + step * (j-1)
# #         high = df[i].min() + step * j
# #         print(low, high)

        
#         # Range = str("{:.2f}".format(low)) + "-" + str("{:.2f}".format(high))
#         # print(Range)
        
#         # Range_dict[str(j)] = Range
    
# #     All_variables[i] = Range_dict

# # print(All_variables)    

# # Range_df =pd.DataFrame.from_dict(All_variables,orient='index')
# # print(Range_df)
# # Range_df.to_excel(a+'_range_table.xlsx')

# # #%%




# # %%

# #%%
# # WTP under different quarters of variables

# # First select a variable and the Q_df that this variables' value is in different Qs

# # For this Q_df, calculate the mean of all variables

# filename = r"N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\Mean-MC-2-12.xlsx"

# writer = pd.ExcelWriter(path, engine = 'xlsxwriter')

# excel_book = pxl.load_workbook(filename)

# with pd.ExcelWriter(filename, engine='openpyxl') as writer:
#     # Your loaded workbook is set as the "base of work"
#     writer.book = excel_book

#     for i in list_of_variables:
        
#         variable_range = df[i].max() - df[i].min()
#         step = variable_range/4
        
#         Q_dict = {}
#         for j in range(1,5):
#             low = df[i].min() + step * (j-1)
#             high = df[i].min() + step * j
#             print(low, high)

#             Q_df = df.loc[df[i].between(low, high, inclusive=True)] 
            
#             mean_dict = {}
#             for k in list_of_variables:
#                 variable_mean = Q_df[k].mean()
#                 print(variable_mean)
#                 mean_dict[str(k)] = variable_mean
        
#             print(mean_dict)
            
#             Q_dict[str(j)] = mean_dict
        
#         Q_df =pd.DataFrame.from_dict(Q_dict,orient='index')
#         Q_df_trans = Q_df.T
        
#         # Write the new data to the file without overwriting what already exists
#         Q_df_trans.to_excel(writer, str(i), index=False)

#         # Save the file
#         writer.save()

# #%
# %%
