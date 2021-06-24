import vs10xx
from machine import SPI

spi = SPI(1, vs10xx.SPI_BAUDRATE) # SPI bus id=1 pinout: SCK = 14, MOSI = 13, MISO = 12

player = vs10xx.Player(
    spi,
    xResetPin = 21,
    dReqPin = 22,
    xDCSPin = 23,
    xCSPin = 25,
    CSPin = None
)

print("VS10xx Player set up.")
player.setVolume(0.8) # the range is 0 to 1.0

