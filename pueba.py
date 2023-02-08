from smbus2 import SMBus
from bluedot.btcomm import BluetoothServer
from gpiozero import LED
from signal import pause
from time import sleep

bus = SMBus(1)
led = LED(17)

# Comandos del sensor:
SENSORADDRESS = 0x40  # Direccion del sensor
ACTIVARTEMP   = 0xE3  # Activar medicion de temperatura
ACTIVARHUM    = 0xE5  # Activar medicion de humedad


class HTU21DBT():
    def readTemp(self):
        bus.write_byte(SENSORADDRESS, ACTIVARTEMP)
        sleep(0.1)
        data = bus.read_i2c_block_data(SENSORADDRESS, ACTIVARTEMP, 2)
        temp = ((data[0] * 256 + data[1]) * 175.72 / 65536.0) - 46.85

        return temp

    def readHum(self):
        bus.write_byte(SENSORADDRESS, ACTIVARHUM)
        sleep(0.1)
        data= bus.read_i2c_block_data(SENSORADDRESS, ACTIVARHUM, 2)
        hum = ((data[0] * 256 + data[1]) * 125 / 65536.0) - 6

        return hum

    def encenderLED(self, opcion):
        if opcion == 1:
            led.on()
            print("Encendido")
        elif opcion == 2:
            print("Apagado")
            led.off()

    def enviarMedicion(self, opcion):
        if opcion == 3:
            dato = round(HTU21DBT.readTemp(self), 3)
            temp = str(dato) + " °C"
            print(str(dato) + " C")
            serverBT.send(temp)
        elif opcion == 4:
            dato = round(HTU21DBT.readHum(self), 3)
            humedad = str(dato) + " %"
            print(humedad)
            serverBT.send(humedad)

        return ("Dato enviado")


sensor = HTU21DBT()


def serialComm(data):
    opcion = int(data.strip())
    sensor.encenderLED(opcion)
    sensor.enviarMedicion(opcion)


serverBT = BluetoothServer(serialComm)
print("Server activado")

pause()
