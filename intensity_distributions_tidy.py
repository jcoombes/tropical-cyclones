
# coding: utf-8

# In[ ]:


#import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#import scipy.stats
#from scipy.optimize import minimize
#from scipy.special import factorial
import seaborn as sns
sns.set()

#import netCDF4
import os
#import time
#import xarray


# In[ ]:


phil_cyclones = pd.read_pickle(os.path.join('..','deconstruct_cyn','phil_cyclones.pkl'))


# In[ ]:


environmental_pressure = 1009.0
phil_cyclones['pressure_deficit'] = environmental_pressure - phil_cyclones['min_pres'] 


# # Intensity Distributions.
# 
# Input:
# 
# phil_cyclones - a list of all the cyclones from ibtracs with etopo height data within phillipines bounding box.
# 
# Output:
# 
# Probability density of intensity (choose v_max or p_min below) distribution with chi-square fit.
# 
# I want to create a plot of the highest v_max a given cyclone ever reaches.
# I want to create a plot of the v_max cyclones reach the timestep before landfall.

# ### Choose an agency and distribution type

# In[ ]:

    
def probdist(ag_choice, v_or_p):
    """
    ag_choice = 'JTWC' or 'CMA' or 'HKO' or 'WMO'
    v_or_p, str - 'max_wind' or 'min_pres' or 'pressure_deficit' else KeyError.
    """
    # In[ ]:
    
    
    #Extra variables for labelling figures when plotting.
    agency = {
    'JTWC': '10',
    'CMA' : '14',
    'WMO' : '19',
    'HKO' : '21'
     }
    
    if v_or_p == 'max_wind':
        unit = 'kt'
        long_name = 'Maximum Sustained Wind'
    elif v_or_p == 'min_pres':
        unit = 'mb'
        long_name = 'Minimum Central Pressure'
    elif v_or_p == 'pressure_deficit':
        unit = 'mb'
        long_name = '{:.0e} mb - Minimum Central Pressure'.format(environmental_pressure)
    else:
        raise(KeyError, "{} is neither 'max_wind', 'min_pres', nor 'pressure_deficit'".format(v_or_p))
    
    
    # ---------------------------
    
    # Some of the agencies have missing values for the maximum wind and minimum pressure.
    # 
    # #### Are any of the values null?
    # 
    # | Agency | Max Wind | Min Pressure | Pressure Def |
    # |--------|----------|--------------|--------------|
    # | JTWC   | Yes      | Yes          | Yes          |
    # | CMA    | Yes      | No           | No           |
    # | WMO    | Yes      | No           | No           |
    # | HKO    | No       | No           | No           |
    
    # -----------------------------------
    
    # In[ ]:
    
    
    phil7withoutna = phil_cyclones[phil_cyclones[v_or_p].notnull()]
    
    
    # In[ ]:
    
    
    intensity7 = phil7withoutna.groupby(['storm_sn', 'center'])['max_wind','min_pres', 'pressure_deficit'].max().unstack()
    
    
    # In[ ]:
    
    
    probdist7 = intensity7[v_or_p][agency[ag_choice]].value_counts().sort_index()
    probdist7
    
    
    # In[ ]:
    
    fig, ax = plt.subplots(1, 1)
    ax.scatter(probdist7.index, probdist7.values)
    ax.set_xlabel('{} of cyclone along track within phillipines box ({})'.format(v_or_p, unit))
    ax.set_ylabel('Number of cyclones in sample')
    ax.set_title('{} {}'.format(ag_choice, v_or_p))
    
    figpath = os.path.join('figures','{} {}.png'.format(ag_choice, v_or_p))
    fig.savefig(figpath)
    plt.clf()
    return fig, ax
    
    # In[ ]:
    
def agpairplot(v_or_p):
    """
    Returns pair plot of all agency pairs.
    
    v_or_p, str - 'max_wind' or 'min_pres' or 'pressure_deficit' else KeyError.
    """
    # In[ ]:
    
    
    #Extra variables for labelling figures when plotting.
    agency = {
    'JTWC': '10',
    'CMA' : '14',
    'WMO' : '19',
    'HKO' : '21'
     }
    
    if v_or_p == 'max_wind':
        unit = 'kt'
        long_name = 'Maximum Sustained Wind'
    elif v_or_p == 'min_pres':
        unit = 'mb'
        long_name = 'Minimum Central Pressure'
    elif v_or_p == 'pressure_deficit':
        unit = 'mb'
        long_name = '{:.0e} mb - Minimum Central Pressure'.format(environmental_pressure)
    else:
        raise(KeyError, "{} is neither 'max_wind', 'min_pres', nor 'pressure_deficit'".format(v_or_p))
    
    
    # ---------------------------
    
    # Some of the agencies have missing values for the maximum wind and minimum pressure.
    # 
    # #### Are any of the values null?
    # 
    # | Agency | Max Wind | Min Pressure | Pressure Def |
    # |--------|----------|--------------|--------------|
    # | JTWC   | Yes      | Yes          | Yes          |
    # | CMA    | Yes      | No           | No           |
    # | WMO    | Yes      | No           | No           |
    # | HKO    | No       | No           | No           |
    
    # -----------------------------------
    
    # In[ ]:
    
    
    phil7withoutna = phil_cyclones[phil_cyclones[v_or_p].notnull()]
    
    
    # In[ ]:
    
    
    intensity7 = phil7withoutna.groupby(['storm_sn', 'center'])['max_wind','min_pres', 'pressure_deficit'].max().unstack()
    
    # In[ ]:
    
    sns.pairplot(intensity7[v_or_p][['10','14','19','21']]).savefig(os.path.join('figures','{} pairplot.png'.format(v_or_p)))
    plt.clf()
    return None
    

if __name__ == "__main__":
    for v_or_p in ['max_wind','min_pres','pressure_deficit']:
        agpairplot(v_or_p)    #Produces 3 plots in figures folder.
        for ag_choice in ['JTWC','CMA','HKO','WMO']:
            probdist(ag_choice, v_or_p) #Produces 12 plots in figures folder.