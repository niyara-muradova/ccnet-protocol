import myhex


class Message:

	baudrate=9600	
	timeout=10
	writeTimeout=10
	
	# Начало пакета
	STX = 0x02
	# Длина пакета
	Len = 0x00
	# Код команды
	CTL = 0x00
	# Данные
	DATA = []
	# Начало пакета
	ETX = 0x03
	# Контрольная сумма
	CHK = 0x00
	# Контрольный бит, чередуется 0,1.
	CBIT = 0x00
	# Extended Note
	SUB = []
	# тело запроса
	body = []
	# ответ на запрос
	reply = []

	def proceed(self):
		self.ACK = ((self.reply[2] & 1) ^ self.CBIT) == 0
		self.NAK = ((self.reply[2] & 1) ^ self.CBIT) > 0
		self.CBIT ^= 1
		self.reply_len = self.reply[1]
		self.reply_CTL = self.reply[2] & 0xFE
		self.ext_reply = (self.reply_CTL==0x70)
		self.ext_data = []
		if self.ext_reply:
			self.reply_sub=self.reply[3]
			self.omni_data = self.reply[4:10]
			self.ext_data = self.reply[10:]
		else:
			self.omni_data = self.reply[3:9]
			self.ext_data = self.reply[9:]
		return self

	def generate(self):
		self.Len = len(self.SUB + self.DATA)+5
		self.body = [self.Len, self.CTL | self.CBIT] + self.SUB+ self.DATA
		self.CHK=0
		for byte in self.body:
			self.CHK ^= byte
		self.body = [self.STX]+self.body+[self.ETX, self.CHK]
		return self

