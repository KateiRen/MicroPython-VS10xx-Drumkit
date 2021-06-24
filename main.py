import vs10xx
from machine import SPI


vs10xx_MIDI_Plugin = [0x0007, 0x0001, 0x8050, 0x0006, 0x0014, 0x0030, 0x0715, 0xb080,
                    0x3400, 0x0007, 0x9255, 0x3d00, 0x0024, 0x0030, 0x0295, 0x6890,
                    0x3400, 0x0030, 0x0495, 0x3d00, 0x0024, 0x2908, 0x4d40, 0x0030,
                    0x0200, 0x000a, 0x0001, 0x0050]


class VS10XXMidi(vs10xx.Player):
    def __init__(self, spi, xResetPin, dReqPin, xDCSPin, xCSPin, CSPin = None):
        super().__init__(spi, xResetPin, dReqPin, xDCSPin, xCSPin, CSPin)
        self.__setupMIDI__()
        # Serial.println("Basic Instruments");
        # talkMIDI(0xB0, 0, 0x00); //Default bank GM1


    def __setupMIDI__(self):
        i = 0
        while i < len(vs10xx_MIDI_Plugin):
            addr = vs10xx_MIDI_Plugin[i]
            n = vs10xx_MIDI_Plugin[i+1]
            i+=2
            while n:
                val = vs10xx_MIDI_Plugin[i]
                super().writeRegister(addr, val)
                print("Writing {value} to the address {address}".format(value=val, address=addr))
                i+=1
                n-=1

    def sendMIDI(self, data):
        self.spi.write(bytes(0))
        self.spi.write(bytes(data))

    def talkMIDI(self, cmd, data1, data2):
        self.sendMIDI(cmd)
        if cmd & 0xF0 <= 0xB0 or cmd & 0xF0 >= 0xE0:
            self.sendMIDI(data1)
            self.sendMIDI(data2)
        else:
            self.sendMIDI(data1)

    def noteOn(self, channel, note, attack_velocity):
        pass

    def noteOff(self, channel, note, attack_velocity):
        pass



spi = SPI(1, vs10xx.SPI_BAUDRATE) # SPI bus id=1 pinout: SCK = 14, MOSI = 13, MISO = 12

midiplayer = VS10XXMidi(
    spi,
    xResetPin = 21,
    dReqPin = 22,
    xDCSPin = 23,
    xCSPin = 25,
    CSPin = None
)

# print("VS10xx Player set up.")
# player.setVolume(0.8) # the range is 0 to 1.0


#VSLoadUserCode();
 

# void VSLoadUserCode(void) {
#   int i = 0;

#   while (i<sizeof(sVS1053b_Realtime_MIDI_Plugin)/sizeof(sVS1053b_Realtime_MIDI_Plugin[0])) {
#     unsigned short addr, n, val;
#     addr = sVS1053b_Realtime_MIDI_Plugin[i++];
#     n = sVS1053b_Realtime_MIDI_Plugin[i++];
#     while (n--) {
#       val = sVS1053b_Realtime_MIDI_Plugin[i++];
#       VSWriteRegister(addr, val >> 8, val & 0xFF);
#     }
#   }
# }                                

# void VSWriteRegister(unsigned char addressbyte, unsigned char highbyte, unsigned char lowbyte){
#   while(!digitalRead(VS_DREQ)) ; //Wait for DREQ to go high indicating IC is available
#   digitalWrite(VS_XCS, LOW); //Select control

#   //SCI consists of instruction byte, address byte, and 16-bit data word.
#   SPI.transfer(0x02); //Write instruction
#   SPI.transfer(addressbyte);
#   SPI.transfer(highbyte);
#   SPI.transfer(lowbyte);
#   while(!digitalRead(VS_DREQ)) ; //Wait for DREQ to go high indicating command is complete
#   digitalWrite(VS_XCS, HIGH); //Deselect Control
# }




# //Plays a MIDI note. Doesn't check to see that cmd is greater than 127, or that data values are less than 127
# void talkMIDI(byte cmd, byte data1, byte data2) {
# #if USE_SPI_MIDI
#   //
#   // Wait for chip to be ready (Unlikely to be an issue with real time MIDI)
#   //
#   while (!digitalRead(VS_DREQ))
#     ;
#   digitalWrite(VS_XDCS, LOW);
# #endif
#   sendMIDI(cmd);
#   //Some commands only have one data byte. All cmds less than 0xBn have 2 data bytes 
#   //(sort of: http://253.ccarh.org/handout/midiprotocol/)
#   if( (cmd & 0xF0) <= 0xB0 || (cmd & 0xF0) >= 0xE0) {
#     sendMIDI(data1);
#     sendMIDI(data2);
#   } else {
#     sendMIDI(data1);
#   }

# #if USE_SPI_MIDI
#   digitalWrite(VS_XDCS, HIGH);
# #endif
# }

# //Send a MIDI note-on message.  Like pressing a piano key
# //channel ranges from 0-15
# void noteOn(byte channel, byte note, byte attack_velocity) {
#   talkMIDI( (0x90 | channel), note, attack_velocity);
# }

# //Send a MIDI note-off message.  Like releasing a piano key
# void noteOff(byte channel, byte note, byte release_velocity) {
#   talkMIDI( (0x80 | channel), note, release_velocity);
# }
