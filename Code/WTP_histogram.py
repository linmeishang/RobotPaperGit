
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

df_org = pd.read_excel('sugarbeet_org_WTP.xlsx')
df_conv = pd.read_excel('sugarbeet_conv_WTP.xlsx')
#%%
print(df_org['price'].mean())
#%%
# print(df_conv['price'].mean())
num_rows = len(df_conv[(df_conv['price']<= 0)])
print(num_rows/len(df_conv))

print(len(df_conv))
#%%
# add a column "system" to both datasets
df_org['system'] = 'Organic'
df_conv['system'] = 'Conventional'

#%%
# Combine the two dataset together
WTP_data = pd.concat([df_org, df_conv])
WTP_data = WTP_data[['system', 'price']]
WTP_data = WTP_data.reset_index(drop=True)
WTP_data.rename(columns = {'price':'WTP'}, inplace = True)
print(WTP_data)

#%%
sns.set(rc={'figure.figsize':(12,8)})
sns.set(font_scale=1.3)
sns.set_style("whitegrid")
Palette= sns.color_palette("colorblind", n_colors=2)
sns.set_palette(Palette)


ax = sns.histplot(data=WTP_data, x="WTP", hue="system", binwidth=1000)
ax.set_xlabel("WTP (€)", loc="right")
ax.set_ylabel("Count", loc="top")
ax.xaxis.labelpad = 15
ax.yaxis.labelpad = 15

plt.savefig("WTP_histplot", dpi=300) 



# %%
