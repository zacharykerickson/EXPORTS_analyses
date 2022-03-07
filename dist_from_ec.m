function dist = dist_from_ec(lon,lat,mtime)
% This function computes the distances from a given point to the
% eddy center (ec) during EXPORTS NA.
% Author: Zachary K Erickson
% Contact: zachary.k.erickson@noaa.gov
% Version: 0.1
% Last updated: 07 March 2022
%
% Eddy center is determined from an analysis from Erik Fields
% Eddy center information located in file 'eddyCenterEstimateFromADCP.mat'
% This file must be in the same folder for this script to work
% Future editions will remove this requirement
%
% Must have the GSW package downloaded and in MATLAB's search path for this
% to run. Can download it at: http://www.TEOS-10.org 
%
% Inputs: lon (longitude), lat (latitude), mtime (matlab datenum)
% Inputs can either be all scalar or all vectors (Nx1 matrices)
% Ouput: distance (km)


ec_data = load('eddyCenterEstimateFromADCP.mat');
ec_mtimes = ec_data.ec_t;
ec_lons = ec_data.ec_lon;
ec_lats = ec_data.ec_lat;
naned = isnan(ec_lons);

lon_interp = interp1(ec_mtimes,ec_lons,mtime,"linear");
lat_interp = interp1(ec_mtimes,ec_lats,mtime,"linear");

dist = gsw_distance(horzcat(lon_interp,lon),horzcat(lat_interp,lat))/1000;

end