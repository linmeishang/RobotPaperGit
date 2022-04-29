#%%
import pandas as pd
import glob
from sklearn.utils import shuffle
import pickle
from pickle import dump, load
import os

#%%
# all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\LHS_*.pkl', recursive=True)
all_files = glob.glob(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\sugarbeet\MC_*.pkl', recursive=True)
print(len(all_files))

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
# df = shuffle(df)


# %%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())
# df.to_excel(r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result\LHS400_sugarbeet_org_WTP.xlsx')
# Pickle the dataframe
dump(df, open('3_MC_1000_sugarbeet_org_WTP.pkl', 'wb'))



# The dataset has been filtered in excel, so the following code is not needed anymore.
#%%
# df.loc[df['yield'].str.contains('sehr niedrig, leichter Boden', na=False), 'yield'] = 0
# df.loc[df['yield'].str.contains('niedrig, mittlerer Boden', na=False), 'yield'] = 1
# df.loc[df['yield'].str.contains('niedrig, leichter Boden', na=False), 'yield'] = 2
# df.loc[df['yield'].str.contains('mittel, schwerer Boden', na=False), 'yield'] = 3
# df.loc[df['yield'].str.contains('mittel, mittlerer Boden', na=False), 'yield'] = 4
# df.loc[df['yield'].str.contains('mittel, leichter Boden', na=False), 'yield'] = 5
# df.loc[df['yield'].str.contains('hoch, mittlerer Boden', na=False), 'yield'] = 6

# print(df['yield'])