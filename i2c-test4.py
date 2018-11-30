import smbus
import time

bus = smbus.SMBus(1)

#who_am_i = bus.read_byte_data(0x6B, 0x0F)
#print("WHO_AM_I:", who_am_i)
#print("")

def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

# enable gyroscope
bus.write_byte_data(0x6B, 0x10, 0b11000011)

# enable accelerometer
bus.write_byte_data(0x6B, 0x20, 0b11000110)

# enable magnetometer
bus.write_byte_data(0x1E, 0x20, 0b11111100)
bus.write_byte_data(0x1E, 0x21, 0b00000000)
bus.write_byte_data(0x1E, 0x22, 0b00000000)
bus.write_byte_data(0x1E, 0x23, 0b00001100)

# temperature
print("***** temperature   *****")
out_temp_l = bus.read_byte_data(0x6B, 0x15)
#print("OUT_TEMP_L:", out_temp_l)
out_temp_h = bus.read_byte_data(0x6B, 0x16)
#print("OUT_TEMP_H:", out_temp_h & 0x0F)
out_temp = twos_complement((((out_temp_h & 0X0F) << 8) | out_temp_l), 12) / 16 + 25 
print("OUT_TEMP:", out_temp, "degrees C")
print("")

# angular rate / gyroscope
print("***** gyroscope     *****")
out_x_g_l = bus.read_byte_data(0x6B, 0x18)
out_x_g_h = bus.read_byte_data(0x6B, 0x19) - 0xf0
out_x_g = twos_complement((out_x_g_h << 8) | out_x_g_l, 12) / 1e3
print("OUT_X_G:", out_x_g, "dps")
out_y_g_l = bus.read_byte_data(0x6B, 0x1A)
out_y_g_h = bus.read_byte_data(0x6B, 0x1B) - 0xf0
out_y_g = twos_complement((out_y_g_h << 8) | out_y_g_l, 12) / 1e3
print("OUT_Y_G:", out_y_g, "dps")
out_z_g_l = bus.read_byte_data(0x6B, 0x1C)
out_z_g_h = bus.read_byte_data(0x6B, 0x1D) - 0xf0
out_z_g = twos_complement((out_z_g_h << 8) | out_z_g_l, 12) / 1e3
print("OUT_Z_G:", out_z_g, "dps")
print("") # \r\n

# linear acceleration / accelerometer
print("***** accelerometer *****")
out_x_xl_l = bus.read_byte_data(0x6B, 0x28)
out_x_xl_h = bus.read_byte_data(0x6B, 0x29)
out_x_xl = twos_complement((out_x_xl_h << 8) | out_x_xl_l, 12) / 1e3
print("OUT_X_XL:", out_x_xl, "g")
out_y_xl_l = bus.read_byte_data(0x6B, 0x2A)
out_y_xl_h = bus.read_byte_data(0x6B, 0x2B)
out_y_xl = twos_complement((out_y_xl_h << 8) | out_y_xl_l, 12) / 1e3
print("OUT_Y_XL:", out_y_xl, "g")
out_z_xl_l = bus.read_byte_data(0x6B, 0x2C)
out_z_xl_h = bus.read_byte_data(0x6B, 0x2D)
out_z_xl = twos_complement((out_z_xl_h << 8) | out_z_xl_l, 12) / 1e3
print("OUT_Z_XL:", out_z_xl, "g")
print("") # \r\n

# magnetic field / magnetometer
print("***** magnetometer  *****")
out_x_m_l = bus.read_byte_data(0x1E, 0x28)
out_x_m_h = bus.read_byte_data(0x1E, 0x29)
out_x_m = twos_complement((out_x_m_h << 8) | out_x_m_l, 12) / 1e3
print("OUT_X_M:", out_x_m, "gauss")
out_y_m_l = bus.read_byte_data(0x1E, 0x2A)
out_y_m_h = bus.read_byte_data(0x1E, 0x2B)
out_y_m = twos_complement((out_y_m_h << 8) | out_y_m_l, 12) / 1e3
print("OUT_Y_M:", out_y_m, "gauss")
out_z_m_l = bus.read_byte_data(0x1E, 0x2C)
out_z_m_h = bus.read_byte_data(0x1E, 0x2D)
out_z_m = twos_complement((out_z_m_h << 8) | out_z_m_l, 12) / 1e3
print("OUT_Z_M:", out_z_m, "gauss")
print("") # \r\n



# LSM9DS0 Gyro address, 0x6B(107)
# Select control register1, 0x20(32)
#               0x0F(15)        Data rate = 95Hz, Power ON
#                                       X, Y, Z-Axis enabled
#bus.write_byte_data(0x1E, 0x10, 0b11011011)
# LSM9DS0 address, 0x6B(107)
# Select control register4, 0x23(35)
#               0x30(48)        DPS = 2000, Continuous update
#bus.write_byte_data(0x6B, 0x23, 0x30)

#time.sleep(0.5)

# LSM9DS0 Gyro address, 0x6B(107)
# Read data back from 0x28(40), 2 bytes
# X-Axis Gyro LSB, X-Axis Gyro MSB
#data0 = bus.read_byte_data(0x6B, 0x28)
#data1 = bus.read_byte_data(0x6B, 0x29)

# Convert the data
#xGyro = data1 * 256 + data0
#if xGyro > 32767 :
#        xGyro -= 65536

#print(xGyro)
