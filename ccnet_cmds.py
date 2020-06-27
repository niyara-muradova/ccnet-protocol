import myhex
import ccnet_msgf
import ccnet_pars


class Commands(ccnet_msgf.Message, ccnet_pars.CCNetReply):

    def POLL(self):
        self.OMNI()
        self.OrientationAnyWay()
        self.ExpandedOmnibusMode()
        self.EscrowMode()
        self.EnableAllDenomination()
        return self

    def CLOSE(self):
        self.OMNI()
        self.OrientationAnyWay()
        self.ExpandedOmnibusMode()
        self.EscrowMode()
        self.DisableDenomination()
        return self

    def OMNI(self):
        self.CTL=0x10
        self.DATA=[0x00, 0x00, 0x00]
        return self
    #byte 0
    def EnableDenomination(self, bit):
        self.DATA[0]=myhex.set_bit(self.DATA[0], bit)
        return self
    def EnableAllDenomination(self):
        self.DATA[0]=0x7F
        return self
    def DisableDenomination(self):
        self.DATA[0]=0x00
        return self
    #*************************byte 1*****************************
    #0
    def PolledMode(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],0)
        return self
    def SpecialMode(self):
        self.DATA[1]=myhex.set_bit(self.DATA[1],0)
        return self
    #1
    def AcceptanceMode(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],1)
        return self
    def SecurityMode(self):
        self.DATA[1]=myhex.set_bit(self.DATA[1],1)
        return self
    #2..3
    def OrientationFaceUpRightEdge(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],2)
        self.DATA[1]=myhex.clear_bit(self.DATA[1],3)
        return self
    def OrientationFaceUp(self):
        self.DATA[1]=myhex.set_bit(self.DATA[1],2)
        self.DATA[1]=myhex.clear_bit(self.DATA[1],3)
        return self
    def OrientationAnyWay(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],2)
        self.DATA[1]=myhex.set_bit(self.DATA[1],3)
        return self
    #4
    def NonEscrowMode(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],4)
        return self
    def EscrowMode(self):
        self.DATA[1]=myhex.set_bit(self.DATA[1],4)
        return self
    #5
    def NonStackMode(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],5)
        return self
    def STACK(self):
        self.DATA[1]=myhex.set_bit(self.DATA[1],5)
        return self
    #6
    def NonReturnMode(self):
        self.DATA[1]=myhex.clear_bit(self.DATA[1],6)
        return self
    def RETURN(self):
        self.DATA[1]=myhex.set_bit(self.DATA[1],6)
        return self

    #*************************byte 2*****************************
    #0
    def NonPushMode(self):
        self.DATA[2]=myhex.clear_bit(self.DATA[2],0)
        return self

    def PushMode(self):
        self.DATA[2]=myhex.set_bit(self.DATA[2],0)
        return self

    #1
    def NonBarcodeMode(self):
        self.DATA[2]=myhex.clear_bit(self.DATA[2],1)
        return self

    def BarcodeMode(self):
        self.DATA[2]=myhex.set_bit(self.DATA[2],1)
        return self

    #2..3
    def PowerUpPolicyA(self):
        self.DATA[2]=myhex.clear_bit(self.DATA[2],2)
        self.DATA[2]=myhex.clear_bit(self.DATA[2],3)
        return self

    def PowerUpPolicyB(self):
        self.DATA[2]=myhex.set_bit(self.DATA[2],2)
        self.DATA[2]=myhex.clear_bit(self.DATA[2],3)
        return self

    def PowerUpPolicyC(self):
        self.DATA[2]=myhex.clear_bit(self.DATA[2],2)
        self.DATA[2]=myhex.set_bit(self.DATA[2],3)
        return self

    #4
    def NonExpandedOmnibusMode(self):
        self.DATA[2]=myhex.clear_bit(self.DATA[2],4)
        return self

    def ExpandedOmnibusMode(self):
        self.DATA[2]=myhex.set_bit(self.DATA[2],4)
        return self

    # EXTENDED COMMANDS LIST

    def EXTC(self):
        self.CTL=0x70
        self.DATA=[0x00, 0x00, 0x00]
        return self
    def SubType(self,sub_type, length):
        self.SUB=[sub_type]
        self.DATA=[0x00 for i in range(length)]
        return self
    def EnableBill(self, bill):
        self.DATA[3+bill//7]=myhex.set_bit(self.DATA[3+bill//7], bill%7)
        return self
    def EnableBillRange(self, end_bill):
        for bill in range(end_bill):
            self.EnableBill(bill)
        return self

    #**************Query Expanded Note Specification***************
    def QuerryNoteSpecification(self, index):
        self.DATA[3]=index
        return self
