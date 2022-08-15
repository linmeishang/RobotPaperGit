#%%
import os
from tkinter import font
from turtle import color
import pandas as pd
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

farming = ["Organic", "Conventional"]
markers = ["o", "v"]
line_styles = ["--", ":"]


#%%
# Define the figure size
fig = plt.figure(figsize=(14, 5))

# Basic setting of the figure
sns.set()
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "Arial"


ax=plt.subplot2grid((1,2),(0,0))
df = pd.read_excel('size-mech.xlsx', sheet_name = 'size')


for i, j, k in zip(farming, markers, line_styles): 
    sns.set_theme(style="whitegrid")
    ax = sns.lineplot(x="size", y= i, marker=j, markersize=8, data=df, label= i, color = "dimgrey", linestyle=k)
    
ax.set_xlabel("Plot size", loc="right")
ax.set_ylabel("Average WTP", loc="top", fontsize=12)
plt.legend(loc='lower right')
plt.title('(a)', y=-0.17)
plt.ylim(80000, 160000)



ax=plt.subplot2grid((1,2),(0,1))

df = pd.read_excel('size-mech.xlsx', sheet_name = 'mech')

for i, j, k in zip(farming, markers, line_styles): 
    sns.set_theme(style="whitegrid")
    ax = sns.lineplot(x="mech", y= i, marker=j, markersize=8, data=df, label= i, color = "dimgrey", linestyle=k)
    
ax.set_xlabel("Mechanisation level", loc="right")
ax.set_ylabel("Average WTP", loc="top", fontsize=12)
plt.legend(loc='lower right')
plt.title('(a)', y=-0.17)
plt.ylim(80000, 160000)

