set_mask = [2**i for i in range(8)]
clear_mask = [0xFF-2**i for i in range(8)]

def if_bit(byte, bit):
	return (byte & set_mask[bit]) > 0
		 
def set_bit(byte, bit):
	return byte | set_mask[bit]


def clear_bit(byte, bit):
	return byte & clear_mask[bit]

def HIGH(val):
	#High byte function
	return val >> 8

def LOW(val):
	#Low byte function
	return val & 0x00ff

def getHEX(data):
	s=''
	for b in bytes(data):
		s+=' '+('0'+hex(b).replace('0x',''))[-2:]
	return s[1:].upper()
