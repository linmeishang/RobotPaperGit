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
all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet2\*org*.pkl', recursive=True)

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
a = 'Org_7'

path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())
# df.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\LHS400_sugarbeet_org_WTP.xlsx')
# Pickle the dataframe
dump(df, open(a+'_sugarbeet_WTP.pkl', 'wb'))

# %%
