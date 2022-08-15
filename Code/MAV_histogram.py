
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

#%%
path = r'N:\agpo\work1\Shang\Robot\RobotPaperGit\Result'
os.chdir(path)
print("Current Working Directory " , os.getcwd())


df_org = pickle.load(open("Total_Org_sugarbeet_org_WTP_1-8.pkl", 'rb'))
df_conv = pickle.load(open("Total_Conv_sugarbeet_WTP_0-2.pkl", "rb"))
# df_org = pd.read_excel('sugarbeet_org_WTP.xlsx')
# df_conv = pd.read_excel('sugarbeet_conv_WTP.xlsx')

#%%
df_conv_negative = df_conv.loc[df_conv['price'] <= 0]
num_rows = len(df_conv[(df_conv['price']<= 0)])
print(num_rows/len(df_conv))

#%%
supervision_mean = df_conv_negative['supervision_ratio'].mean()
print(supervision_mean)
#%%
print(type(df_conv))
#%%
print(df_org.shape)


#%%
print(df_conv['price'].mean())
print(df_conv['price'].min())
print(df_conv['price'].max())


#%%
print(df_org['price'].mean())
print(df_org['price'].min())
print(df_org['price'].max())



#%%
# add a column "system" to both datasets
df_org['Farming system'] = 'organic'
df_conv['Farming system'] = 'conventional'


# Combine the two dataset together
WTP_data = pd.concat([df_org, df_conv])
WTP_data = WTP_data[['Farming system', 'price']]
WTP_data = WTP_data.reset_index(drop=True)
WTP_data.rename(columns = {'price':'WTP'}, inplace = True)
print(WTP_data)


sns.set(rc={'figure.figsize':(12,8)})
sns.set(font_scale=1.3)
sns.set_style("whitegrid")
# Palette= sns.color_palette("colorblind", n_colors=2)
# sns.set_palette(Palette)
sns.set_palette(['#000000', '#ABABAB'])

ax = sns.histplot(data=WTP_data, x="WTP", hue="Farming system", binwidth=1000)
ax.set_xlabel("MAV (€)", loc="right")
ax.set_ylabel("Count", loc="top")
ax.xaxis.labelpad = 15
ax.yaxis.labelpad = 15

plt.savefig("MAV_histplot_bW", dpi=300) 



# %%
