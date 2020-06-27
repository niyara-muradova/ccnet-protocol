import json
import myhex

class CCNetReply:

	bills = []
	bill_enables = []
	bill_security = []

	Accepting = False
	Stacking = False
	Escrowed = False
	CassetteAttached = False

	ext_reply = False

	
	Models=[
		[0x01, 'Discontinued, ZT1000, US'],
		[0x0C, 'Discontinued, ZT1107, US'],
		[0x0F, 'Discontinued, ZT1200, Australia'],
		[0x14, 'Obsolete, ZT1200, US'],
		[0x41, 'AE2600 Gen2D, Australia'],
		[0x42, 'AE2800 Gen2D, Russia'],
		[0x43, 'AE2600 Gen2D, Canada'],
		[0x44, 'AE2800 Gen2D, Euro'],
		[0x45, 'Reserved (VN2300 US Economy)'],
		[0x46, 'Reserved (VN2600 Gen2B & 2D, China)'],
		[0x47, 'Reserved (AE2800 Gen2D, Argentina)'],
		[0x4D, 'AE2800 Gen2D, Mexico'],
		[0x50, 'AE2600 Gen2B, C and D, US Premium'],
		[0x51, 'Discontinued, Philippines'],
		[0x57, 'AE2800 Gen2D, Brazil'],
		[0x58, 'AE2800 Gen2D, US Expanded'],
		[0x1E, 'Discontinued, Series 3000 VFX (BDS)'],
		[0x1F, 'Obsolete, Series 3000 EBDS'],
		[0x4A, 'Discontinued, Cashflow SC 66, Monolithic Code'],
		[0x54, 'Cashflow SC 83, Split Component/Extended Notes'],
		[0x55, 'Cashflow SC 66, Split Component/Extended Notes'],

	]

	def ccnet_parse(self, data):
		#************byte 0*********************
		self.Idling=myhex.if_bit(data[0],0)
		self.Accepting=myhex.if_bit(data[0],1)
		self.Escrowed=myhex.if_bit(data[0],2)
		self.Stacking=myhex.if_bit(data[0],3)
		self.Stacked=myhex.if_bit(data[0],4)
		self.Returning=myhex.if_bit(data[0],5)
		self.Returned=myhex.if_bit(data[0],6)
		#************byte 1*********************
		self.Cheated=myhex.if_bit(data[1],0)
		self.Rejected=myhex.if_bit(data[1],1)
		self.Jammed=myhex.if_bit(data[1],2)
		self.StackerFull=myhex.if_bit(data[1],3)
		self.CassetteAttached=myhex.if_bit(data[1],4)
		self.Paused=myhex.if_bit(data[1],5)
		self.CalibrationInProgress=myhex.if_bit(data[1],6)
		#************byte 2*********************
		self.PowerUp=myhex.if_bit(data[2],0)
		self.InvalidCommand=myhex.if_bit(data[2],1)
		self.Failure=myhex.if_bit(data[2],2)
		self.BillValue=(data[2]&0b111000)>>3
		#************byte 3*********************
		self.Stalled=myhex.if_bit(data[3],0)
		self.FlashDownload=myhex.if_bit(data[3],1)
		self.PreStack=myhex.if_bit(data[3],2)
		self.RawBarcode=myhex.if_bit(data[3],3)
		self.DeviceCaps=myhex.if_bit(data[3],4)
		#************byte 4*********************
		self.ModelNumber=data[4]
		self.model=[x for x in self.Models if x[0]==self.ModelNumber]
		if len(self.model)>0:
			self.ModelName=self.model[0][1]
		else:
			self.ModelName="Unknown Model number"
		#************byte 5*********************
		self.CodeRevision = data[5] / 10
		
	def ccnet_parse_ext(self, data):
		if len(data)<18:
			return
		try:
			self.Index=data[0]
			self.ISOCode=data[1:4].decode("utf-8")
			self.BaseValue=str(int(data[4:7].decode("utf-8")))
			self.Sign=chr(data[7])
			self.Exponent=str(int(data[8:10].decode("utf-8")))
			self.Orientation=data[10]
			self.Type=data[11]
			self.Series=data[12]
			self.Compatibility=data[13]
			self.Version=data[14]
			self.Reserved=data[14:]
			self.Expression=self.BaseValue+'*10**('+self.Sign+self.Exponent+')'
			self.BillValue=eval(self.Expression)
			self.Bill={'amount': self.BillValue, 'country': self.ISOCode}
			self.BillJSON=json.dumps(self.Bill, separators=(",", ":"))
		except Exception as e:
			pass
		
