
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

#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

df = pd.read_excel('sugarbeet_conv_WTP.xlsx')
# # print(df)
# print(df['price'].min())
# print(df['price'].max())
# print(df['price'].mean())
# plt.hist(df['total_weeding_area'])


#%%
a = 'Conv'

list_interaction = ['supervision_ratio', 'supervision_setup_wage']

list_inter_farmCha = [['size', 'setup_time_per_plot'],
                    ['size', 'mechanisation']]

list_of_variables = ['total_weeding_area', 'setup_time_per_plot','repaire_energy_cost', 
                     'herbicide_saving', 'supervision_ratio', 
                     'supervision_setup_wage']

list_of_farmCha = ['size', 'mechanisation']


#%%

# All_variables = {}

# for i in list_of_variables:
    
#     variable_range = df[i].max() - df[i].min()
#     step = variable_range/4
    
#     WTP_dict = {}
    
#     for j in range(1,5):
#         low = df[i].min() + step * (j-1)
#         high = df[i].min() + step * j
#         print(low, high)

#         df_2 = df.loc[df[i].between(low, high, inclusive=True)] 
#         WTP = df_2['price'].mean()
#         print(WTP)
        
#         WTP_dict[str(j)] = WTP
    
#     All_variables[i] = WTP_dict

# print(All_variables)    

# WTP_df =pd.DataFrame.from_dict(All_variables,orient='index')
# print(WTP_df)
# WTP_df.to_excel(a+'_WTP_table.xlsx')


# #%%
# # WTP under different sizes and mechanisation levels
# for i in list_of_farmCha:
    
#     # find the discret data of this farm characteristics
#     unique_values = df[i].unique()
#     unique_values = np.sort(unique_values)
    
#     WTP_dict = {}
    
#     for j in unique_values:
        
#         df_2 = df.loc[df[i] == j] 
#         WTP = df_2['price'].mean()
#         print(WTP)
        
#         WTP_dict[str(j)] = WTP 

#     WTP_df =pd.DataFrame.from_dict(WTP_dict,orient='index')
#     print(WTP_df)
#     WTP_df.to_excel(a+'_WTP_table_'+i+'.xlsx')
    

# #%%
# param_1 = 'supervision_ratio' # must be a variable in the list of variables
# param_2 = 'supervision_setup_wage'   # must be a variable in the list of variables

# min_1 = df[param_1].min()
# max_1 = df[param_1].max()
# range_1 = max_1 - min_1
# step_1 = range_1/4


# min_2 = df[param_2].min()
# max_2 = df[param_2].max()
# range_2 = max_2 - min_2
# step_2 = range_2/4


# # take the average of WTP from the selected data
# WTP_list = []

# for j, k in itertools.product(range(1,5), range(1,5)):
    
#     print(j, k)

#     low_1 = min_1 + step_1 * (j-1)
#     high_1 = min_1 + step_1 * j
#     # print(low_1, high_1)

#     low_2 = min_2 + step_2 * (k-1)
#     high_2 = min_2 + step_2 * k
#     # print(low_2, high_2)

#     df_2 = df.loc[(df[param_1].between(low_1, high_1, inclusive=True)) & (df[param_2].between(low_2, high_2, inclusive=True))]
#     WTP = df_2['price'].mean()
#     WTP_list.append(WTP)
#     print(WTP_list)

#     # reshape list into array and save into dataframe
# WTP_array = np.reshape(WTP_list, (4,4))
# print(WTP_array)


# df = pd.DataFrame(data=WTP_array)

# df.to_excel(a+'_Matrix_'+param_1+'_'+param_2+'.xlsx')



#%%    
param_1 = 'size'  # param_1 must be either "size" or "mechanisation"
param_2 = 'setup_time_per_plot'  # param_2 must be a variable in the list of variables

# find the discret data of this farm characteristics
unique_values = df[param_1].unique()
unique_values = np.sort(unique_values)
    
min_2 = df[param_2].min()
max_2 = df[param_2].max()
range_2 = max_2 - min_2
step_2 = range_2/4

# take the average of WTP from the selected data
WTP_list = []

for j, k in itertools.product(unique_values, range(1,5)):
    
    print(j, k)

    low_2 = min_2 + step_2 * (k-1)
    high_2 = min_2 + step_2 * k
    # print(low_2, high_2)

    df_2 = df.loc[(df[param_1] ==j ) & (df[param_2].between(low_2, high_2, inclusive=True))]
    WTP = df_2['price'].mean()
    WTP_list.append(WTP)
    print(WTP_list)

    # reshape list into array and save into dataframe
WTP_array = np.reshape(WTP_list, (7,4))
print(WTP_array)


df = pd.DataFrame(data=WTP_array)

df.to_excel(a+'_Matrix_'+param_1+'_'+param_2+'.xlsx')

# %%
