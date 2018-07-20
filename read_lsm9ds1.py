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
print(Fore.RED+'LSM9DS1 sensor read - I2C port')
print('')
print('')


parser = argparse.ArgumentParser(prog='Import data from the LSM9DS1 sensor.',
    description=('Main script to import acel - gyro - magneto data from the LSM9DS1\n'
        'to a Raspberry Pi. Data form is MSEED. \n'
    ), formatter_class=RawTextHelpFormatter
)


parser.add_argument(
    '--OSR',action='store', default=256, type=float,
    help=('Oversampling rate (default: %(default)s Hz)\n'),
    metavar='256')

parser.add_argument(
    '--Measurement',action='store', default=0, type=float,
    help=('Type of measurement (default: %(default)s)\n'),
    metavar='0')

parser.add_argument(
    '--Record_time',action='store', default=3600, type=float,
    help=('Time of recording (default: %(default)s sec)\n'),
    metavar='3600')

# Read data 
StTime = (datetime.utcnow())
dT = timedelta(seconds=args.Record_time)
EdTime = StTime + dT

#Data save array
sampl_time = 1/args.OSR
n_samples = dT/sampl_time
acll_x_save = np.zeros((n_samples,),dtype=int32)
acll_y_save = np.zeros((n_samples,),dtype=int32)
acll_z_save = np.zeros((n_samples,),dtype=int32)
gyro_x_save = np.zeros((n_samples,),dtype=int32)
gyro_y_save = np.zeros((n_samples,),dtype=int32)
gyro_z_save = np.zeros((n_samples,),dtype=int32)
magn_x_save = np.zeros((n_samples,),dtype=int32)
magn_y_save = np.zeros((n_samples,),dtype=int32)
magn_z_save = np.zeros((n_samples,),dtype=int32)

acl_x_save = np.zeros((n_samples,),dtype=int32)
acl_y_save = np.zeros((n_samples,),dtype=int32)
acl_z_save = np.zeros((n_samples,),dtype=int32)
gyr_x_save = np.zeros((n_samples,),dtype=int32)
gyr_y_save = np.zeros((n_samples,),dtype=int32)
gyr_z_save = np.zeros((n_samples,),dtype=int32)
mag_x_save = np.zeros((n_samples,),dtype=int32)
mag_y_save = np.zeros((n_samples,),dtype=int32)
mag_z_save = np.zeros((n_samples,),dtype=int32)

def main(sampl_time,measurement,EdTime,StTime,n_samples,ch):

	# I2C port - adresses
	bus = smbus.SMBus(1)

	#Acellerometer 
	adr_acll = 0x6b
	mem_acll = 0x20
	cmd_acll = 0b11001000
	read_acll_xl = 0x28
	read_acll_xh = 0x29
	read_acll_yl = 0x2a
	read_acll_yh = 0x2b
	read_acll_zl = 0x2c
	read_acll_zh = 0x2d

	#Gyroscope
	adr_gyro = 0x6b
	mem_gyro = 0x10
	cmd_gyro = 0b11011000
	read_gyro_xl = 0x18
	read_gyro_xh = 0x19
	read_gyro_yl = 0x1a	
	read_gyro_yh = 0x1b
	read_gyro_zl = 0x1c
	read_gyro_zh = 0x1d

	#Gyroscope
	adr_magn = 0x1e
	mem1_magn = 0x20
	cmd1_magn = 0b11111110
	mem2_magn = 0x21
	cmd2_magn = 0b01100000
	mem3_magn = 0x22
	cmd3_magn = 0b00000000
	mem4_magn = 0x23
	cmd4_magn = 0b00001100
	read_magn_xl = 0x28
	read_magn_xh = 0x29
	read_magn_yl = 0x2a
	read_magn_yh = 0x2b
	read_magn_zl = 0x2c
	read_magn_xh = 0x2d


	if measurement == 0:
		bus.write_byte_data(adr_acll,mem_acll,cmd_acll)

		time.sleep(0.1)

		i=0

		while datetime.utcnow() < EdTime:
			xl_acll = bus.read_byte_data(adr_acll,read_acll_xl)
			xh_acll = bus.read_byte_data(adr_acll,read_acll_xh)

			acll_x_raw = xh_acll * 0x100 + xl_acll

			yl_acll = bus.read_byte_data(adr_acll,read_acll_yl)
			yh_acll = bus.read_byte_data(adr_acll,read_acll_yh)

			acll_y_raw = yh_acll * 0x100 + yl_acll

			zl_acll = bus.read_byte_data(adr_acll,read_acll_zl)
			zh_acll = bus.read_byte_data(adr_acll,read_acll_zh)

			acll_z_raw = zh_acll * 0x100 + zl_acll

			if acll_x_raw > 0x7fff
				acll_x_raw -= 0x10000
			acll_x_save[i] = acll_x_raw

			if acll_y_raw > 0x7fff
				acll_y_raw -= 0x10000
			acll_y_save[i] = acll_y_raw

			if acll_z_raw > 0x7fff
				acll_z_raw -= 0x10000
			acll_z_save[i] = acll_z_raw

			i=i+1
			time.sleep(sampl_time)

		# Fill header attributes
		stats1 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG1', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats1['starttime'] = StTime

		stats2 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG2', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats2['starttime'] = StTime

		stats3 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HGZ', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats3['starttime'] = StTime
		st1 = Stream([Trace(data=,acll_x_save header=stats1)])
		st2 = Stream([Trace(data=,acll_y_save header=stats2)])
		st3 = Stream([Trace(data=,acll_z_save header=stats3)])
		st1.write("LSM9DS1_IMU_aclX.mseed", format='MSEED', encoding=11, reclen=512)
		st2.write("LSM9DS1_IMU_aclY.mseed", format='MSEED', encoding=11, reclen=512)
		st3.write("LSM9DS1_IMU_aclZ.mseed", format='MSEED', encoding=11, reclen=512)

	if measurement == 1:
		bus.write_byte_data(adr_gyro,mem_gyro,cmd_gyro)

		time.sleep(0.1)

		i=0

		while datetime.utcnow() < EdTime:
			xl_gyro = bus.read_byte_data(adr_gyro,read_gyro_xl)
			xh_gyro = bus.read_byte_data(adr_gyro,read_gyro_xh)

			gyro_x_raw = xh_gyro * 0x100 + xl_gyro

			yl_gyro = bus.read_byte_data(adr_gyro,read_gyro_yl)
			yh_gyro = bus.read_byte_data(adr_gyro,read_gyro_yh)

			gyro_y_raw = yh_gyro * 0x100 + yl_gyro

			zl_gyro = bus.read_byte_data(adr_gyro,read_gyro_zl)
			zh_gyro = bus.read_byte_data(adr_gyro,read_gyro_zh)

			gyro_z_raw = zh_gyro * 0x100 + zl_gyro

			if gyro_x_raw > 0x7fff
				gyro_x_raw -= 0x10000
			gyro_x_save[i] = gyro_x_raw

			if gyro_y_raw > 0x7fff
				gyro_y_raw -= 0x10000
			gyro_y_save[i] = gyro_y_raw

			if gyro_z_raw > 0x7fff
				gyro_z_raw -= 0x10000
			gyro_z_save[i] = gyro_z_raw
			
			i=i+1
			time.sleep(sampl_time)

		# Fill header attributes
		stats1 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG1', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats1['starttime'] = StTime

		stats2 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG2', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats2['starttime'] = StTime

		stats3 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HGZ', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats3['starttime'] = StTime
		st1 = Stream([Trace(data=,gyro_x_save header=stats1)])
		st2 = Stream([Trace(data=,gyro_y_save header=stats2)])
		st3 = Stream([Trace(data=,gyro_z_save header=stats3)])
		st1.write("LSM9DS1_IMU_gyroX.mseed", format='MSEED', encoding=11, reclen=512)
		st2.write("LSM9DS1_IMU_gyroY.mseed", format='MSEED', encoding=11, reclen=512)
		st3.write("LSM9DS1_IMU_gyroZ.mseed", format='MSEED', encoding=11, reclen=512)

	if measurement == 2:
		bus.write_byte_data(adr_magn,mem2_magn,cmd1_magn)
		bus.write_byte_data(adr_magn,mem2_magn,cmd2_magn)
		bus.write_byte_data(adr_magn,mem3_magn,cmd3_magn)
		bus.write_byte_data(adr_magn,mem4_magn,cmd4_magn)

		time.sleep(0.1)

		i=0

		while datetime.utcnow() < EdTime:
			xl_magn = bus.read_byte_data(adr_magn,read_magn_xl)
			xh_magn = bus.read_byte_data(adr_magn,read_magn_xh)

			magn_x_raw = xh_magn * 0x100 + xl_magn

			yl_magn = bus.read_byte_data(adr_magn,read_magn_yl)
			yh_magn = bus.read_byte_data(adr_magn,read_magn_yh)

			magn_y_raw = yh_magn * 0x100 + yl_magn

			zl_magn = bus.read_byte_data(adr_magn,read_magn_zl)
			zh_magn = bus.read_byte_data(adr_magn,read_magn_zh)

			magn_z_raw = zh_magn * 0x100 + zl_magn

			if magn_x_raw > 0x7fff
				magn_x_raw -= 0x10000
			magn_x_save[i] = magn_x_raw

			if magn_y_raw > 0x7fff
				magn_y_raw -= 0x10000
			magn_y_save[i] = magn_y_raw

			if magn_z_raw > 0x7fff
				magn_z_raw -= 0x10000
			magn_z_save[i] = magn_z_raw
			
			i=i+1
			time.sleep(sampl_time)

		# Fill header attributes
		stats1 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG1', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats1['starttime'] = StTime

		stats2 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG2', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats2['starttime'] = StTime

		stats3 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HGZ', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats3['starttime'] = StTime
		st1 = Stream([Trace(data=,magn_x_save header=stats1)])
		st2 = Stream([Trace(data=,magn_y_save header=stats2)])
		st3 = Stream([Trace(data=,magn_z_save header=stats3)])
		st1.write("LSM9DS1_IMU_magnX.mseed", format='MSEED', encoding=11, reclen=512)
		st2.write("LSM9DS1_IMU_magnX.mseed", format='MSEED', encoding=11, reclen=512)
		st3.write("LSM9DS1_IMU_magnX.mseed", format='MSEED', encoding=11, reclen=512)

	if measurement == 3:

		bus.write_byte_data(adr_acll,mem_acll,cmd_acll)
		bus.write_byte_data(adr_gyro,mem_gyro,cmd_gyro)
		bus.write_byte_data(adr_magn,mem2_magn,cmd1_magn)
		bus.write_byte_data(adr_magn,mem2_magn,cmd2_magn)
		bus.write_byte_data(adr_magn,mem3_magn,cmd3_magn)
		bus.write_byte_data(adr_magn,mem4_magn,cmd4_magn)

		time.sleep(0.1)

		i=0

		while datetime.utcnow() < EdTime:
			xl_acll = bus.read_byte_data(adr_acll,read_acll_xl)
			xh_acll = bus.read_byte_data(adr_acll,read_acll_xh)

			acll_x_raw = xh_acll * 0x100 + xl_acll

			yl_acll = bus.read_byte_data(adr_acll,read_acll_yl)
			yh_acll = bus.read_byte_data(adr_acll,read_acll_yh)

			acll_y_raw = yh_acll * 0x100 + yl_acll

			zl_acll = bus.read_byte_data(adr_acll,read_acll_zl)
			zh_acll = bus.read_byte_data(adr_acll,read_acll_zh)

			acll_z_raw = zh_acll * 0x100 + zl_acll

			if acll_x_raw > 0x7fff
				acll_x_raw -= 0x10000
			acll_x_save[i] = acll_x_raw

			if acll_y_raw > 0x7fff
				acll_y_raw -= 0x10000
			acll_y_save[i] = acll_y_raw

			if acll_z_raw > 0x7fff
				acll_z_raw -= 0x10000
			acll_z_save[i] = acll_z_raw

			xl_gyro = bus.read_byte_data(adr_gyro,read_gyro_xl)
			xh_gyro = bus.read_byte_data(adr_gyro,read_gyro_xh)

			gyro_x_raw = xh_gyro * 0x100 + xl_gyro

			yl_gyro = bus.read_byte_data(adr_gyro,read_gyro_yl)
			yh_gyro = bus.read_byte_data(adr_gyro,read_gyro_yh)

			gyro_y_raw = yh_gyro * 0x100 + yl_gyro

			zl_gyro = bus.read_byte_data(adr_gyro,read_gyro_zl)
			zh_gyro = bus.read_byte_data(adr_gyro,read_gyro_zh)

			gyro_z_raw = zh_gyro * 0x100 + zl_gyro

			if gyro_x_raw > 0x7fff
				gyro_x_raw -= 0x10000
			gyro_x_save[i] = gyro_x_raw

			if gyro_y_raw > 0x7fff
				gyro_y_raw -= 0x10000
			gyro_y_save[i] = gyro_y_raw

			if gyro_z_raw > 0x7fff
				gyro_z_raw -= 0x10000
			gyro_z_save[i] = gyro_z_raw

			xl_magn = bus.read_byte_data(adr_magn,read_magn_xl)
			xh_magn = bus.read_byte_data(adr_magn,read_magn_xh)

			magn_x_raw = xh_magn * 0x100 + xl_magn

			yl_magn = bus.read_byte_data(adr_magn,read_magn_yl)
			yh_magn = bus.read_byte_data(adr_magn,read_magn_yh)

			magn_y_raw = yh_magn * 0x100 + yl_magn

			zl_magn = bus.read_byte_data(adr_magn,read_magn_zl)
			zh_magn = bus.read_byte_data(adr_magn,read_magn_zh)

			magn_z_raw = zh_magn * 0x100 + zl_magn

			if magn_x_raw > 0x7fff
				magn_x_raw -= 0x10000
			magn_x_save[i] = magn_x_raw

			if magn_y_raw > 0x7fff
				magn_y_raw -= 0x10000
			magn_y_save[i] = magn_y_raw

			if magn_z_raw > 0x7fff
				magn_z_raw -= 0x10000
			magn_z_save[i] = magn_z_raw
			
			i=i+1
			time.sleep(sampl_time)

		# Fill header attributes
		stats1 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG1', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats1['starttime'] = StTime

		stats2 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG2', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats2['starttime'] = StTime

		stats3 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HGZ', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats3['starttime'] = StTime
		st1 = Stream([Trace(data=,acll_x_save header=stats1)])
		st2 = Stream([Trace(data=,acll_y_save header=stats2)])
		st3 = Stream([Trace(data=,acll_z_save header=stats3)])
		st1.write("LSM9DS1_IMU_aclX.mseed", format='MSEED', encoding=11, reclen=512)
		st2.write("LSM9DS1_IMU_aclX.mseed", format='MSEED', encoding=11, reclen=512)
		st3.write("LSM9DS1_IMU_aclX.mseed", format='MSEED', encoding=11, reclen=512)

		# Fill header attributes
		stats11 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG1', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats11['starttime'] = StTime

		stats12 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG2', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats12['starttime'] = StTime

		stats13 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HGZ', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats3['starttime'] = StTime
		st11 = Stream([Trace(data=,gyro_x_save header=stats11)])
		st12 = Stream([Trace(data=,gyro_y_save header=stats12)])
		st13 = Stream([Trace(data=,gyro_z_save header=stats13)])
		st11.write("LSM9DS1_IMU_gyroX.mseed", format='MSEED', encoding=11, reclen=512)
		st12.write("LSM9DS1_IMU_gyroX.mseed", format='MSEED', encoding=11, reclen=512)
		st13.write("LSM9DS1_IMU_gyroX.mseed", format='MSEED', encoding=11, reclen=512)

		# Fill header attributes
		stats21 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG1', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats21['starttime'] = StTime

		stats22 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HG2', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats22['starttime'] = StTime

		stats23 = {'network': 'PI', 'station': 'MS',
         		'channel': 'HGZ', 'npts': n_samples, 'sampling_rate': 1/sampl_time,
         		'mseed': {'dataquality': 'D'}}

		stats23['starttime'] = StTime
		st21 = Stream([Trace(data=,magn_x_save header=stats21)])
		st22 = Stream([Trace(data=,magn_y_save header=stats22)])
		st23 = Stream([Trace(data=,magn_z_save header=stats23)])
		st21.write("LSM9DS1_IMU_magnX.mseed", format='MSEED', encoding=11, reclen=512)
		st22.write("LSM9DS1_IMU_magnX.mseed", format='MSEED', encoding=11, reclen=512)
		st23.write("LSM9DS1_IMU_magnX.mseed", format='MSEED', encoding=11, reclen=512)

	return acll_x_save, acll_y_save, acll_z_save, gyro_x_save, gyro_y_save, gyro_z_save, magn_x_save, magn_y_save, magn_z_save


acl_x_save,acl_y_save,acl_z_save,gyr_x_save,gyr_y_save,gyr_z_save,mag_x_save,mag_y_save,mag_z_save = main(sampl_time,measurement,EdTime)




