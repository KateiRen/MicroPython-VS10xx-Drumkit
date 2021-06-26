from time import sleep_ms
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
        print("Set Basic Instruments")
        self.talkMIDI(0xB0, 0, 0x00) # Set Default bank GM1


    def __setupMIDI__(self): # das Muster aus Writes mit Adresse und Wert scheint zu stimmen (siehe http://www.vlsi.fi/fileadmin/software/VS10XX/vs1053b-rtmidistart.zip)
        i = 0
        while i < len(vs10xx_MIDI_Plugin):
            addr = vs10xx_MIDI_Plugin[i]
            n = vs10xx_MIDI_Plugin[i+1]
            i+=2
            while n>0:
                val = vs10xx_MIDI_Plugin[i]
                super().writeRegister(addr, val)
                print("Writing {0:02x} to the address {1:02x}".format(val, addr))
                i+=1
                n-=1
                # print("n =" + str(n))

    def sendMIDI(self, data):
        self.spi.write(bytes(0))
        self.spi.write(bytes(data))
        

    def talkMIDI(self, cmd, data1, data2):
        self.waitForDREQ()
        self.xDCS.value(0)
        self.sendMIDI(cmd)
        if (cmd & 0xF0) <= 0xB0 or (cmd & 0xF0) >= 0xE0:
            self.sendMIDI(data1)
            self.sendMIDI(data2)
        else:
            self.sendMIDI(data1)
        self.xDCS.value(1)

    def noteOn(self, channel, note, attack_velocity):
        self.talkMIDI(0x90 | channel, note, attack_velocity)
        #self.talkMIDI(bytes(0x90 | channel), bytes(note), bytes(attack_velocity))

    def noteOff(self, channel, note, attack_velocity):
        self.talkMIDI(0x80 | channel, note, attack_velocity)
        #self.talkMIDI(bytes(0x80 | channel), bytes(note), bytes(attack_velocity))

spi = SPI(1, baudrate=vs10xx.SPI_BAUDRATE, firstbit=SPI.MSB) # SPI bus id=1 pinout: SCK = 14, MOSI = 13, MISO = 12
midiplayer = VS10XXMidi(spi, xResetPin = 21, dReqPin = 22, xDCSPin = 23, xCSPin = 25, CSPin = None)

print("VS10xx Player set up.")
# player.setVolume(0.8) # the range is 0 to 1.0
#print("Volume set")

midiplayer.talkMIDI(0xB0, 0x07, 120) # 0xB0 is channel message, set channel volume to near max (127)
midiplayer.talkMIDI(0xB0, 0, 0x00) # Default bank GM1

for instrument in range(0, 127):
    midiplayer.talkMIDI(0xC0, instrument, 0x00)
    print("Playing instrument: {0}".format(instrument))
    for note in range(30, 40):
        print("Playing note: {0}".format(note))
        midiplayer.noteOn(0, note, 127)
        print("sent noteOn")
        sleep_ms(200)

        midiplayer.noteOff(0, note, 127)
        print("sent noteOff")
        sleep_ms(50)
    sleep_ms(100)