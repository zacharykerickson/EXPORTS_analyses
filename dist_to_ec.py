# This function computes the distances from a given point to the
# eddy center (ec) during EXPORTS NA.
# Author: Zachary K Erickson
# Contact: zachary.k.erickson@noaa.gov
# Version: 0.1
# Last updated: 07 March 2022
#
# Eddy center is determined from an analysis from Erik Fields
# Eddy center information located in file 'eddyCenterEstimateFromADCP.mat'
# This file must be in the same folder for this script to work
# Future editions will remove this requirement
#
# Functions:
# dist_to_ec(lon,lat,mtime): returns distance in km
# E_from_ec(lon,mtime): returns longitudinal distance in degrees
# N_from_ec(lat,mtime): returns latitudinal distance in degrees
# get_ec_props(): returns longitude,latitude,mtime of eddy center

import numpy as np
import h5py
import gsw

def dist_to_ec(lon,lat,mtime):
    ec_lons,ec_lats,ec_mtimes = get_ec_props()

    lon_interp = np.interp(mtime,ec_mtimes,ec_lons,left=np.nan,right=np.nan)
    lat_interp = np.interp(mtime,ec_mtimes,ec_lats,left=np.nan,right=np.nan)

    return gsw.distance(np.vstack((lon,lon_interp)),
                        np.vstack((lat,lat_interp)),axis=0)[0]/1000

def E_from_ec(lon,mtime):
    ec_lons,_,ec_mtimes = get_ec_props()
    lon_interp = np.interp(mtime,ec_mtimes,ec_lons,left=np.nan,right=np.nan)
    return lon-lon_interp

def N_from_ec(lat,mtime):
    _,ec_lats,ec_mtimes = get_ec_props()
    lat_interp = np.interp(mtime,ec_mtimes,ec_lats,left=np.nan,right=np.nan)
    return lat-lat_interp

def get_ec_props():
    f = h5py.File('eddyCenterEstimateFromADCP.mat')
    ec_mtimes = f['ec_t'][:].ravel()
    ec_lons = f['ec_lon'][:].ravel()
    ec_lats = f['ec_lat'][:].ravel()
    ec_nan = np.isnan(ec_lons*ec_lats)

    return ec_lons[~ec_nan],ec_lats[~ec_nan],ec_mtimes[~ec_nan]
