import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = df=pd.read_csv('medical_examination.csv')

# 2
df['height']=df['height']/100
df['BMI']=df['weight']/(df['height']**2)
df['overweight'] = (df['BMI']>25).astype(int)
df.drop(columns=['BMI'],inplace=True)

# 3
df[['cholesterol','gluc']]=df[['cholesterol','gluc']].applymap(lambda x:0 if x==1 else 1)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars=["cardio"], 
                     value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"], 
                     var_name="variable", value_name="value")


    # 6
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="count")
    

    # 7
    catplot = sns.catplot(x="variable", y="count", hue="value", col="cardio",
                      data=df_cat, kind="bar", palette="Set2")

    catplot.set_axis_labels("variable", "total")
    catplot.set_titles("Cardio = {col_name}")

    
    return catplot.figure

    # 8
    fig = draw_cat_plot()


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &  
        (df["height"] >= df["height"].quantile(0.025)) &  
        (df["height"] <= df["height"].quantile(0.975)) &  
        (df["weight"] >= df["weight"].quantile(0.025)) & 
        (df["weight"] <= df["weight"].quantile(0.975))   
    ]
    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15
    sns.heatmap(corr, annot=True, fmt=".1f", mask=mask, cmap="coolwarm", center=0, linewidths=0.5, ax=ax)



    # 16
    fig.savefig('heatmap.png')
    return fig
