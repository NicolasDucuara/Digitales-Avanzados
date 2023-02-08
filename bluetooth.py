from bluedot.btcomm import BluetoothServer
from adafruit_htu21d import HTU21D
import board
from gpiozero import LED
from signal import pause

led = LED(17)
i2c = board.I2C()
sensor = HTU21D(i2c)

def leerTemperatura():
    lectura = sensor.temperature
    return lectura

def leerHumedad():
    lectura = sensor.relative_humidity
    return lectura

def serialComm(data):
    opcion=int(data.strip())
    if opcion == 1:
        led.on()
    elif opcion == 2:
        led.off()
    elif opcion == 3:
        dato = round(leerTemperatura(),2)
        temp=str(dato) + " °C"
        serverBT.send(temp)
    elif opcion == 4:
        dato = round(leerHumedad(),2)
        humedad=str(dato) + " %"
        serverBT.send(humedad)
    else:
        pass

print("Server activado")
serverBT=BluetoothServer(serialComm)

pause()