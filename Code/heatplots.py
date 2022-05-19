#%%
import os
from tkinter import font
from turtle import color
import pandas as pd
import  numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
from sympy import Line
#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())

#%%
df1 = pd.read_excel('2-12_MC_Matrix_unskilled_labor_wage_weeding_efficiency.xlsx')
df2 = pd.read_excel('2-12_MC_Matrix_supervision_setup_wage_supervision_ratio.xlsx')

print(df1)

fig, axes = plt.subplots(ncols=2, figsize=(14, 5))

ax1, ax2 = axes

im1 = ax1.matshow(df1)
im2 = ax2.matshow(df2)

fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)




# %%
