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

farming = ["organic", "conventional"]
markers = ["o", "v"]
line_styles = ["--", ":"]


#%%
# Define the figure size
fig = plt.figure(figsize=(14, 10))

# Basic setting of the figure

sns.set(font_scale = 5.0)

sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "Arial"
# plt.rcParams.update({'font.size': 20})


ax=plt.subplot2grid((2,2),(0,0))
df = pd.read_excel('size-mech.xlsx', sheet_name = 'size')


sns.set_theme(style="whitegrid")
ax = sns.lineplot(x="size", y= 'organic', marker='o', markersize=8, 
                  data=df, label= 'organic', color = "black", linestyle='--')
    
ax.set_xlabel("Plot size (ha)", loc="right")
ax.set_ylabel("Average MAV (€)", loc="top", fontsize=12)
plt.legend(loc='lower right')
plt.title('(a)', y=-0.17)
plt.ylim(270000, 285000)



ax=plt.subplot2grid((2,2),(0,1))

df = pd.read_excel('size-mech.xlsx', sheet_name = 'mech')

sns.set_theme(style="whitegrid")
ax = sns.lineplot(x="mech", y= 'organic', marker='o', markersize=8, 
                  data=df, label= 'organic', color = "black", linestyle='--')
    
ax.set_xlabel("Mechanisation level (kW)", loc="right")
ax.set_ylabel("Average MAV (€)", loc="top", fontsize=12)
plt.legend(loc='lower right')
plt.title('(b)', y=-0.17)
plt.ylim(270000, 285000)



##################
ax=plt.subplot2grid((2,2),(1,0))
df = pd.read_excel('size-mech.xlsx', sheet_name = 'size')


sns.set_theme(style="whitegrid")
ax = sns.lineplot(x="size", y= 'conventional', marker='v', markersize=8, 
                  data=df, label= 'conventional', color = "black", linestyle=':')
    
ax.set_xlabel("Plot size (ha)", loc="right")
ax.set_ylabel("Average MAV (€)", loc="top", fontsize=12)
plt.legend(loc='lower right')
plt.title('(c)', y=-0.17)
plt.ylim(4500, 13000)



ax=plt.subplot2grid((2,2),(1,1))

df = pd.read_excel('size-mech.xlsx', sheet_name = 'mech')

sns.set_theme(style="whitegrid")
ax = sns.lineplot(x="mech", y= 'conventional', marker='v', markersize=8, 
                  data=df, label= 'conventional', color = "black", linestyle=':')
    
ax.set_xlabel("Mechanisation level (kW)", loc="right")
ax.set_ylabel("Average MAV (€)", loc="top", fontsize=12)
plt.legend(loc='lower right')
plt.title('(d)', y=-0.17)
plt.ylim(4500, 13000)



plt.savefig("size-mech", dpi=300) 
# %%
