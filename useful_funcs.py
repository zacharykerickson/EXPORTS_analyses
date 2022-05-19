from scipy.interpolate import RegularGridInterpolator
from netCDF4 import Dataset
import numpy as np
from scipy.stats import norm

def in_eddy(time=None,lon=None,lat=None,data=None,return_output_interpolator=False,return_binary=False,threshold=-2/np.pi,return_probability=False):
    '''
    Inputs:
        time (day in May, can be scalar or numpy array)
        lon (longitude in degrees, can be scalar or numpy array)
        lat (latitude in degrees, can be scalar or numpy array)
        data (can be a filename, a netCDF4 Dataset, or a RegularGridInterpolator
    Optional inputs (default value)
        return_output_interpolator (False): controls output, see below
        return_binary (False): controls output, see below
        return_probability (False): controls output, see below
        threshold (-2/np.pi): set threshold for determining if location is in eddy
    Output:
        if return_output_interpolator is True:
            returns RegularGridInterpolator object
        elif return_probability is True:
            returns probability that Gamma<threshold (from a bootstrap analysis, n=25, assuming normal distribution)
        elif return_binary is True:
            returns True where Gamma<threshold and False otherwise
        else: (default)
            returns Gamma at specified (time,lon,lat) coordinates
    Examples:
        # Different input types
        gamma = in_eddy(10,-15,49,'Gamma_insitu.nc')
        nc = Dataset('Gamma_insitu.nc')
        gamma = in_eddy(10,-15,49,nc) # same output as before
        g_int = in_eddy(data='Gamma_insitu_nc',return_output_interpolator=True)
        gamma = in_eddy(10,-15,49,g_int) # same output as before, may save time if you can do the previous step only once

        # Different output types
        bool_eddy = in_eddy(10,-15,49,'Gamma_insitu.nc',return_binary=True)
        prob_eddy = in_eddy(10,-15,49,'Gamma_insitu.nc',return_probability=True)

    '''
    if type(data) is str:
        data = Dataset(data,'r')
    if type(data) is Dataset:
        if return_probability:
            means = RegularGridInterpolator(
                (data.variables['time'][:],data.variables['lat'][:],data.variables['lon'][:]),
                data.variables['gamma_mean'][:],method='linear',
                bounds_error=False,fill_value=np.nan)
            stds = RegularGridInterpolator(
                (data.variables['time'][:],data.variables['lat'][:],data.variables['lon'][:]),
                data.variables['gamma_std'][:],method='linear',
                bounds_error=False,fill_value=np.nan)
            mean = means((time,lat,lon))
            std = stds((time,lat,lon))
            return norm.cdf(threshold,mean,std)

        data = RegularGridInterpolator(
            (data.variables['time'][:],data.variables['lat'][:],data.variables['lon'][:]),
            data.variables['gamma'][:],method='linear',
            bounds_error=False,fill_value=np.nan)
    if type(data) is RegularGridInterpolator:
        if return_output_interpolator:
            output = data
        else:
            output = data((time,lat,lon))
            if return_binary:
                output = output<threshold
    else:
        output = np.nan
    return output
