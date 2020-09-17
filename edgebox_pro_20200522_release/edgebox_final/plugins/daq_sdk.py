from ctypes import *
import os
import platform

#DAQ stauts code 
(\
	DAQ_STATUS_GOOD,\
	DAQ_STATUS_BAD_CONNECT,\
	DAQ_STATUS_BAD_COMMUNICATION,\
	DAQ_STATUS_BAD_AUTHENTICATION,\
	DAQ_STATUS_BAD_HAS_CLIENT,\
	DAQ_STATUS_BAD_PTHREAD,\
	DAQ_STATUS_BAD_CHANNEL_ID,\
	DAQ_STATUS_BAD_DATA_SIZE,\
	DAQ_STATUS_INVALID_SOCKET,\
	DAQ_STATUS_CMD_FAIL,\
) = (0, -1, -2, -3, -4, -5, -6, -7, -8, -9)
#DAQ_HPS_Buffer
(\
	HPS_BUFFER_SIZE_128K,\
	HPS_BUFFER_SIZE_256K,\
	HPS_BUFFER_SIZE_512K,\
	HPS_BUFFER_SIZE_1M,\
	HPS_BUFFER_SIZE_2M,\
	HPS_BUFFER_SIZE_4M,\
	HPS_BUFFER_SIZE_8M,\
	HPS_BUFFER_SIZE_16M\
) = (1,2,4,8,16,32,64,128)

(HPS_MODE_A,HPS_MODE_B) = (0, 1) #DAQ_HPS_MODE

#DAQ_HPS_Sample
(DAQ_FALSE, DAQ_TRUE) = (0, 1) #DAQ_Boolean

#DAQ_HPS_Sample
(\
	HPS_SAMPLE_RATE_1K,\
	HPS_SAMPLE_RATE_2K,\
	HPS_SAMPLE_RATE_4K,\
	HPS_SAMPLE_RATE_8K,\
	HPS_SAMPLE_RATE_16K,\
	HPS_SAMPLE_RATE_32K,\
	HPS_SAMPLE_RATE_64K,\
	HPS_SAMPLE_RATE_128K,\
	HPS_SAMPLE_RATE_256K\
) = (1, 2, 4, 8, 16, 32, 64, 128, 256)

(HPS_SAMPLE_V, HPS_SAMPLE_A) = (0 ,1) #DAQ_HPS_VA_TYPE

(HPS_COUPLING_AC_V, HPS_COUPLING_DC_V,HPS_COUPLING_AC_A, HPS_COUPLING_DC_A) = (0 ,1,2,3) #lucy change 20200325 DAQ_HPS_COUPLING

(HPS_DIO_INPUT, HPS_DIO_OUTPUT) = (0, 1) #DAQ_HPS_DIO_DIR

(HPS_DIO_LOW, HPS_DIO_HIGH) = (0, 1) #DAQ_HPS_DIO_LEVEL

(HPS_TRIGGER_FPGA_CLOSE,HPS_TRIGGER_FPGA_OPEN)=(0,1)#DAQ_HPS_TRIGGER_FPGA

(\
	HPS_DIO_PORT_1, \
	HPS_DIO_PORT_2, \
	HPS_DIO_PORT_3, \
	HPS_DIO_PORT_4, \
	HPS_DIO_PORT_5, \
	HPS_DIO_PORT_6\
) = (1, 2, 3, 4, 5, 6) #DAQ_HPS_DIO_PORT

class DAQ_Channel_Data(Structure):
    _fields_ = [
				("sequence_num",c_int),
				("channel_id",c_int),
                ("validnum", c_int),
                ("data", c_int*16),
                ("hts", c_uint),
                ("lts", c_uint)]
  
#lucy add 20200306

class  DAQ_Socket(Structure):
	_fields_= [("data_socket", c_int),
			   ("command_socket", c_int)]
#licy add end   
   
class DaqSDK():
	socket = 0
	
	csocket = (DAQ_Socket)()
	csocket.data_socket=-1
	csocket.command_socket=-1

	psocket = pointer(csocket)
	def __init__(self):  
		path = os.path.dirname(os.path.realpath(__file__))
		if platform.system() == 'Windows':
			if platform.architecture()[0] == '32bit':
				self.lib = cdll.LoadLibrary(os.path.join(path, 'daq_sdk_32bit.dll'))
			elif platform.architecture()[0] == '64bit':
				self.lib = cdll.LoadLibrary(os.path.join(path, 'daq_sdk_64bit.dll'))
			else:
				print("The architecture is not supported.")
				exit()
		elif platform.system() == 'Linux':
				if platform.architecture()[0] == '32bit':
					self.lib = cdll.LoadLibrary(os.path.join(path, 'libdaq_sdk_32bit.so'))
				elif platform.architecture()[0] == '64bit':
					self.lib = cdll.LoadLibrary(os.path.join(path, 'libdaq_sdk_64bit.so'))
				else:
					print("The architecture is not supported.")
					exit()
		else:
			print("The system is not supported.")
			exit()
	#function: daq_set_buffer_size
		#size: 0 ~ 500,000
	def daq_set_buffer_size(self, size):
		self.lib.daq_set_buffer_size(c_uint(size))

	#function: daq_connect
	def daq_connect(self, ip, port, user, pwd):
		cip = ip.encode("ascii")
		cuser = user.encode("ascii")
		cpwd = pwd.encode("ascii")
		ret = self.lib.daq_connect(cip, c_uint(port), cuser, cpwd, self.psocket)
		#lucy add 20200314
		self.socket = self.csocket.data_socket
		return ret

	#function: daq_get_channel_data
		#channel_id: 0~11
		#size
	def daq_get_channel_data(self, channel_id, size):
		data = (DAQ_Channel_Data * size)()
		pdata = pointer(data)
		ret = self.lib.daq_get_channel_data(c_uint(channel_id), c_uint(size), pdata, self.psocket)
		return ret, data

	#function: daq_basic_config
		#buffer:
			#HPS_BUFFER_SIZE_256K
			#HPS_BUFFER_SIZE_512K
			#HPS_BUFFER_SIZE_1M
			#HPS_BUFFER_SIZE_2M
			#HPS_BUFFER_SIZE_4M
			#HPS_BUFFER_SIZE_8M
			#HPS_BUFFER_SIZE_16M
		#mode:
			#HPS_MODE_A
			#HPS_MODE_B
	def daq_basic_config(self, buffer, mode):
		ret = self.lib.daq_basic_config(buffer, mode, self.psocket)
		return ret		

	#function: daq_clear_buffer
		#channel_id: 0~11		
	def daq_clear_buffer(self, channel_id):
		ret = self.lib.daq_clear_buffer(c_uint(channel_id), self.psocket)
		return ret	

	#function: daq_buffer_config
		#buffer:
			#HPS_BUFFER_SIZE_256K
			#HPS_BUFFER_SIZE_512K
			#HPS_BUFFER_SIZE_1M
			#HPS_BUFFER_SIZE_2M
			#HPS_BUFFER_SIZE_4M
			#HPS_BUFFER_SIZE_8M
			#HPS_BUFFER_SIZE_16M	
	def daq_buffer_config(self, buffer):
		ret = self.lib.daq_buffer_config(buffer, self.psocket)
		return ret	

	#function: daq_sample_config
		#channel_id: 0~11
		#mode:
			#HPS_MODE_A
			#HPS_MODE_B
	def daq_sample_config(self, channel_id, mode):
		#lucy add 202020314
		ret = self.lib.daq_sample_config(c_uint(channel_id), mode, self.psocket)
		return ret

	#function: daq_power_config
		#on:
			#DAQ_FALSE: off
			#DAQ_TRUE:  on
	def daq_power_config(self, on):
		ret = self.lib.daq_power_config(on, self.psocket)
		return ret

	#function: daq_channel_enable_config
		#channel_id: 0~11
		#enable:
			#DAQ_FALSE: off
			#DAQ_TRUE:  on
	def daq_channel_enable_config(self, channel_id, enable):
		ret = self.lib.daq_channel_enable_config(c_uint(channel_id), enable, self.psocket)
		return ret

	#function: daq_mode_config
		#sample_A, sample_B:
			#HPS_SAMPLE_RATE_1K
			#HPS_SAMPLE_RATE_2K
			#HPS_SAMPLE_RATE_4K
			#HPS_SAMPLE_RATE_8K
			#HPS_SAMPLE_RATE_16K
			#HPS_SAMPLE_RATE_32K
			#HPS_SAMPLE_RATE_64K
			#HPS_SAMPLE_RATE_128K
			#HPS_SAMPLE_RATE_256K
	def daq_mode_config(self, sample_A, sample_B):
		ret = self.lib.daq_mode_config(sample_A, sample_B, self.psocket)
		return ret

	#function: daq_iepe_coupling_config
		#channel_id: 0~11
		#iepe:
			#DAQ_FALSE: off
			#DAQ_TRUE:  on
		#coupling:
			#HPS_COUPLING_AC
			#HPS_COUPLING_DC
	def daq_iepe_coupling_config(self, channel_id, iepe, coupling):
		ret = self.lib.daq_iepe_coupling_config(c_uint(channel_id), iepe, coupling, self.psocket)
		return ret

	#function: daq_collect_voltage_current_config
		#channel_id: 0~11
		#type:
			#HPS_SAMPLE_V
			#HPS_SAMPLE_A
	def daq_collect_voltage_current_config(self, channel_id, type):
		ret = self.lib.daq_collect_voltage_current_config(c_uint(channel_id), type, self.psocket)
		return ret

	#function: daq_disconnect
	def daq_disconnect(self):
		self.lib.daq_disconnect(self.psocket)

	def daq_io_config(self, dio_port, dio_dir):
		ret = self.lib.daq_io_config(c_uint(dio_port), c_uint(dio_dir), self.psocket)
		return ret

	def daq_io_set(self, dio_port, dio_value):
		ret = self.lib.daq_io_set(c_uint(dio_port), c_uint(dio_value), self.psocket)
		return ret

	def daq_io_get(self, dio_port):
		value = c_uint(0)
		pvalue = pointer(value)
		ret = self.lib.daq_io_get(c_uint(dio_port), pvalue, self.psocket)
		return ret,value

	def daq_trigger_io_set(self, dio_port):
		ret = self.lib.daq_trigger_io_set(c_uint(dio_port), self.psocket)
		return ret
	#lucy add 20200306
	#funciton : daq_trigger_fpga
		#value:
			#HPS_TRIGGER_FPGA_CLOSE
			#HPS_TRIGGER_FPGA_OPEN
	def daq_trigger_fpga(self, value):
		ret = self.lib.daq_trigger_fpga(value, self.psocket)
		return ret
	#lucy add end 

###################example###################
'''
import os
import _thread
from daq_sdk import *
import time


def check_cnt(last, data):
	for i in range(0,data.validnum - 1):
		if(last == 0):
			last = data.data[i]
			continue;
		if(last + 1 != data.data[i]):
			print("Error: ", "Last:", last, "current:", data.data[i])
		last = data.data[i]
	return last


def get_data_thread(name, delay):
	print("running...")
	size = 100
	last_cnt = 0
	while  1:
		ret ,smp_data = sdk.daq_get_channel_data(0,size)
		for i in range(0, size):
			print("===================================")
			print("channel_id:", smp_data[i].channel_id, " validnum:", smp_data[i].validnum)
			print("hts:", '%#x'%smp_data[i].hts, " lts:", '%#x'%smp_data[i].lts)
			for j in range(0, smp_data[i].validnum):
				print('%#x '%smp_data[i].data[j], end='')
			print(" ")

def exit_main(ret):
	if(ret != 0):
		exit()
	
if __name__ == "__main__":
	sdk = DaqSDK()
	sdk.daq_set_buffer_size(50000)
	
	ret = sdk.daq_connect("192.168.1.100", 23333, "admin", "admin")

	ret = sdk.daq_mode_config(HPS_SAMPLE_RATE_16K, HPS_SAMPLE_RATE_128K)
	print("Call daq_mode_config, ret = ", ret)
	exit_main(ret)

	print("Call daq_connect, ret = ", ret)
	ret = sdk.daq_sample_config(0, HPS_MODE_A)
	print("Call daq_sample_config, ret = ", ret)

	ret = sdk.daq_buffer_config(HPS_BUFFER_SIZE_256K)
	print("Call daq_buffer_config, ret = ", ret)
	exit_main(ret)

	exit_main(ret)	
	try:
		_thread.start_new_thread(get_data_thread, ("get_data_thread", 2, ))
	except:
		print("ERROR!!")
	
	ret = sdk.daq_basic_config(HPS_BUFFER_SIZE_4M, HPS_MODE_A)
	print("Call daq_basic_config, ret = ", ret)
	exit_main(ret)
	
	ret = sdk.daq_clear_buffer(0)
	print("Call daq_clear_buffer, ret = ", ret)
	exit_main(ret)

	ret = sdk.daq_buffer_config(HPS_BUFFER_SIZE_8M)
	print("Call daq_buffer_config, ret = ", ret)
	exit_main(ret)

	ret = sdk.daq_sample_config(3, HPS_MODE_B)
	print("Call daq_sample_config, ret = ", ret)
	exit_main(ret)

	#ret = sdk.daq_power_config(DAQ_FALSE)
	#print("Call daq_power_config, ret = ", ret)
	#exit_main(ret)
	
	ret = sdk.daq_channel_enable_config(2, DAQ_TRUE)
	print("Call daq_channel_enable_config, ret = ", ret)
	exit_main(ret)

	ret = sdk.daq_mode_config(HPS_SAMPLE_RATE_256K, HPS_SAMPLE_RATE_128K)
	print("Call daq_mode_config, ret = ", ret)
	exit_main(ret)
	
	ret = sdk.daq_iepe_coupling_config(1, DAQ_TRUE, HPS_COUPLING_DC)
	print("Call daq_iepe_coupling_config, ret = ", ret)
	exit_main(ret)
	
	ret = sdk.daq_collect_voltage_current_config(0, HPS_SAMPLE_V)
	print("Call daq_collect_voltage_current_config, ret = ", ret)
	exit_main(ret)
	
	while 1:
		time.sleep(10)
	sdk.daq_disconnect()

'''
    
