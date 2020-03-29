#!/usr/bin/env python
# coding: utf-8
#THIS PARTICULAR SCRIPT OFFERS YOU TO PLOT YOUR OWN METEOGRAM GIVEN THE NECESSARY PARAMETERS# 
#IT REQUIRES GFS DATASET#
#YET THE IMPROVED VERSION, IN WHICH THE USAGE OF OTHER DATASETS ARE SUPPORTED, WILL BE RELEASED SOON#

from visjobs.visjobs.datas import get_data
import xarray as xr
import cartopy
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import iplot, init_notebook_mode
from pytz import timezone

#_________________________________________________________________________________*
#   Getting the GFS data using visjobs's get_data module's pick_data function     #
#_________________________________________________________________________________*

data = get_data.pick_data(year='2020', month='03', day='24', hour='12', latest=False, model='GFS')
# Function exports the GFS dataset initialized at 2020-03-24-12 UTC extending forward 5 days.
# Go to https://github.com/donmezk/visjobs for further explanation about getting the data

#_____________________________________________________*
#                Defining Functions                   #
#_____________________________________________________*
#         Assigning to the dataset variables          #
#_____________________________________________________*

def meteogram_TMSLP(lat, lon, days, data):
    """ Returns temperature and MSLP meteogram plot.
    Given the data, specified latitude and longitude 
    lat  : Latitude
    lon  : Longitude
    days : Count of days to plot
    data : GFS 0.25 Forecast dataset
    
    NOTE : Temperature given in K, changed to degreeC in the function! 
           Pressure is given in Pa, changed to hPa in the function!
           It may take several seconds to plot the meteogram.
    """
    #_____________________________________________________*
    #                Dataset Mungling Part                #
    #_____________________________________________________*
    
    #Assign requested hour counts to a variable 
    day_count = int(days)
    try:
        if day_count > 0 and day_count<6 :
            if day_count == 1:
                sliced = 9
            elif day_count == 2:
                sliced = 17
            elif day_count == 3:
                sliced = 25
            elif day_count == 4:
                sliced = 33
            elif day_count == 5:
                sliced = 38    
    except: 
        raise ValueError("Please enter days in between 1 and 5")
    
    
    # Extract Temperature and MSLP values from the dataset and Specify time range in interest
    temp = data['tmpsfc'].sel(time=data['tmpsfc']['time'].isel(time=slice(0,sliced)))
    pres = data['prmslmsl'].sel(time=data['prmslmsl']['time'].isel(time=slice(0,sliced)))
    time = data['acpcpsfc']['time'].isel(time=slice(0,sliced))
    initialization = data['acpcpsfc']['time'].isel(time=slice(0,sliced))[0].values
    init = str(initialization)[0:-16] + 'Z'
    
    #Set the Latitude and Longitude given as input 
    pres1 = pres.sel(lon = lon, lat = lat ).values/100
    temp1 = temp.sel(lon = lon, lat = lat ).values
    time1 = time.values  
    
    #_____________________________________________________*
    #             Dataset Visualization Part              #
    #_____________________________________________________*
    
    number_gp = 7
    #_____________________________________________________*
    #Create fig and set ax and customize the plot
    fig = plt.figure(figsize=(13,6))
    ax  = plt.subplot(2,1,1)
    ax.text(0.83, 1.03, 'INIT : {}'.format(init), fontsize=12, transform=ax.transAxes)
    ax.plot(time1, pres1,'bs',color='red')
    ax.plot(time1, pres1,color='red')
    ax.set_ylim(np.min(pres1)-2,np.max(pres1)+2)
    ax.legend(['pressure(mb)'], facecolor='w')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_edgecolor('#444444')
    ax.spines['bottom'].set_linewidth(4)
    ax.spines['top'].set_edgecolor('#444444')
    ax.spines['top'].set_linewidth(1)
    ax.grid(linestyle=':', linewidth=0.5)
    ax.set_facecolor('#ebebeb')
    fig.tight_layout()
    plt.title('Mean Sea Level Pressure(MSLP)',fontweight="bold")
    plt.xlabel('Date(month-day-UTC)')
    plt.ylabel('Pressure(mb-hPa)')
    
    #_____________________________________________________*
    #Set ax1 and customize the plot
    ax1 = plt.subplot(2,1,2)
    #ax1.plot(time_smooth, tempp_smooth(hours),'bs')
    ax1.stackplot(time1, temp1,color='orange')
    ax1.set_ylim(np.min(temp1)-5,np.max(temp1)+5)
    ax1.legend(['temperature(C)'], facecolor='w')
    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_edgecolor('#444444')
    ax1.spines['bottom'].set_linewidth(4)
    ax1.spines['top'].set_edgecolor('#444444')
    ax1.spines['top'].set_linewidth(1)
    ax1.grid(linestyle=':', linewidth=0.5)
    ax1.set_facecolor('#ebebeb')
    plt.title('Temperature(2m)',fontweight="bold")
    plt.xlabel('Date(month-day-UTC)')
    plt.ylabel('Temperature(C)')
    fig.tight_layout()
    
    
def meteogram_PRCVS(lat, lon, day, data):
    """ Returns Accumulated Precipitation and Surface Visibility meteogram plot.
    Given the data, specified latitude and longitude 
    lat : Latitude
    lon : Longitude
    days : Count of days to plot
    data: GFS 0.25 Forecast dataset
    
    NOTE : Visibility given in m, changed to km in the function! 
           It may take several seconds to plot the meteogram.
           
    """
    #_____________________________________________________*
    #                Dataset Mungling Part                #
    #_____________________________________________________*
    
    #Assign requested hour counts to a variable 
    day_count = int(days)
    try:
        if day_count > 0 and day_count<6 :
            if day_count == 1:
                sliced = 9
            elif day_count == 2:
                sliced = 17
            elif day_count == 3:
                sliced = 25
            elif day_count == 4:
                sliced = 33
            elif day_count == 5:
                sliced = 38    
    except: 
        raise ValueError("Please enter days in between 1 and 5")
    
    # Extract Temperature and MSLP values from the dataset and Specify time range in interest
    vis = data['vissfc'].sel(time=data['vissfc']['time'].isel(time=slice(0,sliced)))
    prec = data['acpcpsfc'].sel(time=data['acpcpsfc']['time'].isel(time=slice(0,sliced)))
    time = data['acpcpsfc']['time'].isel(time=slice(0,sliced))
    initialization = data['acpcpsfc']['time'].isel(time=slice(0,sliced))[0].values
    init = str(initialization)[0:-16] + 'Z'
    
    #Set the Latitude and Longitude given as input 
    vis1 = vis.sel(lon = lon, lat = lat ).values * (10**-3)
    prec1 = prec.sel(lon = lon, lat = lat ).values
    time1 = time.values  
    
    #_____________________________________________________*
    #             Dataset Visualization Part              #
    #_____________________________________________________*
    number_gp = 7
    #_____________________________________________________*
    #Create fig and set ax and customize the plot
    fig = plt.figure(figsize=(13,6))
    ax = plt.subplot(2,1,1)
    ax.text(0.83, 1.03, 'INIT : {}'.format(init), fontsize=12, transform=ax.transAxes)
    ax.plot(time1, prec1,'bs',color='purple')
    ax.plot(time1, prec1,color='purple')
    ax.set_ylim(np.min(prec1)-2,np.max(prec1)+2)
    ax.legend(['precipitation accumulation(mm)'], facecolor='w')
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_edgecolor('#444444')
    ax.spines['bottom'].set_linewidth(4)
    ax.spines['top'].set_edgecolor('#444444')
    ax.spines['top'].set_linewidth(1)
    ax.grid(linestyle=':', linewidth=0.5)
    ax.set_facecolor('#ebebeb')
    fig.tight_layout()
    plt.title('Precipitation Accumulation in mm',fontweight="bold")
    plt.xlabel('Date')
    plt.xlabel('Date(month-day-UTC)')
    plt.ylabel('Precipitation(mm)')
    
    #_____________________________________________________*
    #Set ax1 and customize the plot
    ax1 = plt.subplot(2,1,2)
    ax1.stackplot(time1, vis1,color='pink')
    ax1.set_ylim(np.min(vis1)-1,np.max(vis1)+5)
    ax1.legend(['Visibility(km)'], facecolor='w')
    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_edgecolor('#444444')
    ax1.spines['bottom'].set_linewidth(4)
    ax1.spines['top'].set_edgecolor('#444444')
    ax1.spines['top'].set_linewidth(1)
    ax1.grid(linestyle=':', linewidth=0.5)
    ax1.set_facecolor('#ebebeb')
    plt.title('Visibility Surface',fontweight="bold")
    plt.xlabel('Date(month-day-UTC)')
    plt.ylabel('Visibility(km)')
    fig.tight_layout()    

