#*****************************************************************#
#
#	LSM9DS1 Pressure sensor read I2C port
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Jul. 2018
#
#****************************************************************#

#Modules
import time
import smbus
import sys
from colorama import Fore, Back, Style
import numpy as np 
import argparse
from argparse import RawTextHelpFormatter

print('')
print('Convertion of raw data, MS5837-02BA differential pressure sensor')
print('')
print('')

parser = argparse.ArgumentParser(prog='Convert raw data from the LSM9DS1 sensor.',
    description=('Main script to convert acel - gyro - magneto data from the LSM9DS1\n'
    ), formatter_class=RawTextHelpFormatter
)

parser.add_argument(
    '--Type_data',action='store', default=0, type=float,
    help=('Type of data; 0=acl, 1=gyro, 2=magneto. (default: %(default)s)\n'),
    metavar='0')

parser.add_argument(
    'data_X', action='store', default=None, type=str,
    help='Path to x data, can be SAC or mseed.\n',
    metavar='<data>')

parser.add_argument(
    'data_Y', action='store', default=None, type=str,
    help='Path to y data, can be SAC or mseed.\n',
    metavar='<data>')

parser.add_argument(
    'data_Z', action='store', default=None, type=str,
    help='Path to z data, can be SAC or mseed.\n',
    metavar='<data>')

data_x = read(args.data_X)
data_y = read(args.data_Y)
data_z = read(args.data_Z)

statsx = data_x[0].stats
statsy = data_y[0].stats
statsz = data_z[0].stats

n_samples = len(data_x)

sens_Acl = 0.725e-3
sens_Gyr = 70e-3
sens_Mag = 0.58e-3


if args.Type_data == 0:
	for i in range(0,n_samples):
		data_x[i] *= sens_Acl
		data_y[i] *= sens_Acl
		data_z[i] *= sens_Acl

if args.Type_data == 1:
	for i in range(0,n_samples):
		data_x[i] *= sens_Gyr
		data_y[i] *= sens_Gyr
		data_z[i] *= sens_Gyr

if args.Type_data == 2:
	for i in range(0,n_samples):
		data_x[i] *= sens_Mag
		data_y[i] *= sens_Mag
		data_z[i] *= sens_Mag

nctitle = [args.Type_data]
flag1 = 'Conv_LSM9DS1_X%s' %nctitle
flag2 = 'Conv_LSM9DS1_Y%s' %nctitle
flag3 = 'Conv_LSM9DS1_Z%s' %nctitle

st1 = Stream([Trace(data=data_x, header=stats)])
st2 = Stream([Trace(data=data_y, header=stats)])
st3 = Stream([Trace(data=data_z, header=stats)])

st1.write("%s.mseed" % flag1, format='MSEED', encoding=11, reclen=512)
st2.write("%s.mseed" % flag2, format='MSEED', encoding=11, reclen=512)
st3.write("%s.mseed" % flag3, format='MSEED', encoding=11, reclen=512)
