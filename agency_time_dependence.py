
# coding: utf-8

# In[ ]:


import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats
from scipy.optimize import minimize
from scipy.special import factorial
import seaborn as sns
sns.set()

import netCDF4
import os
import time
import xarray


# In[ ]:


phil_cyclones = pd.read_pickle(os.path.join('..','deconstruct_cyn','phil_cyclones.pkl'))


# In[ ]:


environmental_pressure = 1009.0
phil_cyclones['pressure_deficit'] = environmental_pressure - phil_cyclones['min_pres'] 


# # Agency Time Dependence
# 
# Input:
# 
# phil_cyclones - a list of all the cyclones from ibtracs with etopo height data within phillipines bounding box.
# 
# Output:
# 
# The difference of two agencies as a function of time.

# ### Choose an agency and distribution type

    # In[ ]:
    
def time_series_agency_diff(ag_choice, ag_choice2, v_or_p):    
    ag_choice = 'JTWC'
    ag_choice2 = 'WMO'
    v_or_p = 'max_wind' #max_wind or min_pres
    
    
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
    else:
        raise(KeyError, "{} is neither 'max_wind' nor 'min_pres'".format(v_or_p))
    
    
    # ---------------------------
    
    # Some of the agencies have missing values for the maximum wind and minimum pressure.
    # 
    # #### Are any of the values null?
    # 
    # | Agency | Max Wind | Min Pressure | 
    # |--------|----------|--------------|
    # | JTWC   | Yes      | Yes          |
    # | CMA    | Yes      | No           |
    # | WMO    | Yes      | No           |
    # | HKO    | No       | No           |
    
    # -----------------------------------
    
    # In[ ]:
    
    
    phil7withoutna = phil_cyclones[phil_cyclones[v_or_p].notnull()]
    
    
    # In[ ]:
    
    
    intensity7 = phil7withoutna.groupby(['storm_sn', 'center'])['max_wind','min_pres'].max().unstack()
    
    
    # In[ ]:
    
    
    agency_diff = intensity7[v_or_p,agency[ag_choice]] - intensity7[v_or_p, agency[ag_choice2]]
    agency_diff_without_na = agency_diff.dropna()
    
    newframe = pd.DataFrame(agency_diff_without_na,columns = ['{} {} - {} {}'.format(v_or_p, ag_choice, v_or_p, ag_choice2),])
    
    
    # In[ ]:
    
    
    newframe2 = newframe.reset_index()
    
    
    # In[ ]:
    
    
    newframe2['first_measurement'] = newframe2['storm_sn'].str.slice(start=0, stop=7)
    
    
    # In[ ]:
    
    
    first_half = newframe2['storm_sn'].str.slice(start=0,stop=7)
    
    
    
    newframe2['first_measurement'] = first_half.apply(
    lambda x: datetime.datetime(int(x[:4]), 1, 1) + datetime.timedelta(int(x[4:7]) - 1)
    )
    
    
    # In[ ]:
    
    
    
    # --------------
    
    # In[ ]:
    
    plt.scatter(newframe2['first_measurement'], newframe2['{} {} - {} {}'.format(v_or_p, ag_choice, v_or_p, ag_choice2)].apply(abs))
    plt.savefig(os.path.join('figures','{} {} - {} {}'.format(v_or_p, ag_choice, v_or_p, ag_choice2)))
    
    
    # In[ ]:
    
    
    tens = newframe2['first_measurement'] > datetime.datetime(2010,1,1)
    diffstring = '{} {} - {} {}'.format(v_or_p, ag_choice, v_or_p, ag_choice2)
    
    
    # In[ ]:
    
    
    plt.scatter(newframe2.first_measurement[tens], newframe2[diffstring][tens])
    
    
    # In[ ]:
    
    
    eighties = ((newframe2['first_measurement'] > datetime.datetime(1980,1,1)) & (newframe2['first_measurement'] < datetime.datetime(1990,1,1)))
    
    
    # In[ ]:
    
    
    plt.scatter(newframe2.first_measurement[eighties], newframe2[diffstring][eighties])
    
    
    # ------------
    probdist7 = intensity7[v_or_p][agency[ag_choice]].value_counts().sort_index()
    plt.scatter(probdist7.index, probdist7.values)
    plt.xlabel('{} of cyclone along track within phillipines box ({})'.format(v_or_p, unit))
    plt.ylabel('Number of cyclones in sample')
    plt.title('{} {}'.format(ag_choice, v_or_p))
    
    figpath = os.path.join('figures','{} {}.png'.format(ag_choice, v_or_p))
    plt.savefig(figpath)
    plt.clf()
    # In[ ]:
    
    
    #sns.pairplot(intensity7[v_or_p][['10','14','19','21']]).savefig(os.path.join('figures','{} pairplot.png'.format(v_or_p)))
    
if __name__ == "__main__":
    ag_choices = ['JTWC','CMA','HKO','WMO']
    for v_or_p in ['max_wind','min_pres']:
        for ag_choice in range(len(ag_choices)):
            for ag_choice2 in range(ag_choice):
                time_series_agency_diff(ag_choice, ag_choice2, v_or_p) #Produces 2 * 6 plots in figures folder.