import os
import time
import serial
import configparser
import ccnet_cmds


class Device(ccnet_cmds.Commands):
    configName = 'default.conf'

    serial = None

    last_reply = []

    def __init__(self):
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.timeout = 10
        self.serial.writeTimeout = 10

        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.bytesize = serial.SEVENBITS
        self.serial.parity = serial.PARITY_EVEN

        if not os.path.exists(self.configName):
            self.createConfig()
        else:
            self.readConfig()

    def close_port(self):
        if self.serial:
            self.serial.close()

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read(self.configName)
        self.serial.port = config['DEFAULT']['port']
        self.serial.baudrate = int(config['DEFAULT']['baudrate'])
        self.serial.timeout = int(config['DEFAULT']['timeout'])
        self.serial.writeTimeout = int(config['DEFAULT']['writeTimeout'])

    def createConfig(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'port': 'COM1',
                             'baudrate': 19200, 'timeout': 10, 'writeTimeout': 10}
        with open(self.configName, 'w') as configfile:
            config.write(configfile)

    def send(self):
        # ->SEND COMMAND
        time.sleep(0.1)
        self.serial.write(self.generate().body)
        # <-WAIT REPLY
        time.sleep(0.01)
        self.first = self.serial.read(2)
        # self.last = self.serial.read(self.first[1] - 2)
        # PARSE ANSWER
        self.reply = self.first #+ self.last
        # PROCEED ANSWER
        self.proceed()
        # PARSE ANSWER
        self.ccnet_parse(self.omni_data)
        # EXTENDED ANSWER
        if self.ext_reply:
            self.ccnet_parse_ext(self.ext_data)
