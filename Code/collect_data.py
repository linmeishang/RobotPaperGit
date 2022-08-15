#%%
import pandas as pd
import numpy as np
import glob
from sklearn.utils import shuffle
import pickle
from pickle import dump, load
import os
from scipy import stats
#%%
<<<<<<< HEAD
all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet2\*org*.pkl', recursive=True)
=======
all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\*conv*.pkl', recursive=True)
>>>>>>> 21c99419abe83c9c88b05460a14450cacfc13ca3

#%%
df = pd.DataFrame()
for file in all_files:
    if file.endswith('.pkl'):
        
        # df = df.append(pd.read_excel(file)) 
        df = df.append(load(open(file, 'rb')))
        print(df.shape)
        
df.head() 
print(df.shape)


### For loading excels 
# all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\*.xlsx', recursive=True)
# print(len(all_files))
# df = pd.DataFrame()
# for file in all_files:
#     if file.endswith('.xlsx'):
        
#         df = df.append(pd.read_excel(file)) 
    
#         print(df.shape)
        
# df.head() 
# print(df.shape)

#%%
# df = shuffle(df)


# %%
<<<<<<< HEAD
a = 'Org_7'
=======
a = '3_MC_5000'
>>>>>>> 21c99419abe83c9c88b05460a14450cacfc13ca3

path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())
# df.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\LHS400_sugarbeet_org_WTP.xlsx')
# Pickle the dataframe
<<<<<<< HEAD
dump(df, open(a+'_sugarbeet_WTP.pkl', 'wb'))
=======
dump(df, open(a+'_sugarbeet_conv_WTP.pkl', 'wb'))
>>>>>>> 21c99419abe83c9c88b05460a14450cacfc13ca3

# %%
