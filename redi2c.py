from smbus2 import SMBus, i2c_msg
from gpiozero import Button
from time import sleep

addMbed = 0x10
addRtc = 0x68
addEEPROM = 0x50

stopButton = Button(17, pull_up=0)
bus = SMBus(1)

opcion = 0
select = 0
flag = 0
dirEEPROM = 0
noDatos = 0
readblock = 0

sensor = []
tiempo = []
saveEEPROM = []
lectura = []


def imp():
    print("\n[1]: Leer sensor\n"
          "[2]: Leer fecha actual\n"
          "[3]: Guardar datos EEPROM\n"
          "[4]: Leer datos en EEPROM\n"
          "[5]: Escribir Nibble\n"
          "[STOP]: Presione el boton para detener la lectura del sensor")


def leerSensor():
    global sensor
    bus.write_byte_data(addMbed, 0, 0)
    sensor = bus.read_i2c_block_data(addMbed, 0, 2)
    num = ((sensor[0] << 8) + sensor[1])
    hb = int(num/100)
    lb = int(num % 100)
    sensor = [hb, lb]
    print("%i,%i V" % (sensor[0], sensor[1]))
    sleep(0.2)


def impTime():
    global tiempo
    time = bus.read_i2c_block_data(addRtc, 0, 7)
    tiempo = [time[4], time[5], time[2], time[1]]
    print("%x/%x %x:%x" % (time[4], time[5], time[2], time[1]))


def escribirNibble():
    nibble = int(input("Ingrese un numero entre 0 y 15: "))
    while 0 > nibble or nibble > 15:
        print("Numero fuera de rango, intente de nuevo.")
        nibble = int(input("Ingrese un número entre 0 y 15: "))
    print(nibble)
    bus.write_byte_data(addMbed, 0, nibble)
    bus.write_byte_data(addMbed, 0, nibble)


def menuwriteEEPROMM():
    global opcion, saveEEPROM, sensor, tiempo, noDatos, dirEEPROM
    saveEEPROM = sensor+tiempo
    noDatos = len(saveEEPROM)
    if saveEEPROM != []:
        dirEEPROM = (
            int(input("Ingrese el registro desde donde quiere guardar los datos: ")))
        while 0 > dirEEPROM < 35768-noDatos+1:
            print("Registro fuera de rango, intente de nuevo.")
            dirEEPROM = (
                int(input("Ingrese el registro desde donde quiere guardar los datos: ")))
        print("Escribir el siguiente bloque de datos desde el registro %i hasta %i: " % (
            dirEEPROM, dirEEPROM+noDatos))
        for i in saveEEPROM:
            print("[%x] " % (i), end="")
    else:
        print("Bloque de datos vacio")
        opcion = 0


def menureadEEPROM():
    global opcion, select, flag, noDatos, dirEEPROM
    select = (int(input("[1]: Leer un dato\n[2]: Leer un bloque de datos\n"
                        "[3]: Salir\nSeleccione que hacer: ")))
    if select == 1:
        dirEEPROM = (int(input("Ingrese el registro que quiere leer: ")))
        while 0 > dirEEPROM < 35768:
            print("Registro fuera de rango, intente de nuevo.")
            dirEEPROM = (int(input("Ingrese el registro que quiere leer: ")))
        flag = 1
    elif select == 2:
        dirEEPROM = (
            int(input("Ingrese el registro desde donde quiere leer: ")))
        while 0 > dirEEPROM < 35768-noDatos+1:
            print("Limite exedido para leer el dato")
            dirEEPROM = (
                int(input("Ingrese el registro desde donde quiere leer: ")))
        noDatos = (
            int(input("Ingrese la cantidad de registros que quiere leer: ")))
        while 0 > dirEEPROM < 35768-noDatos+1:
            print("Limite exedido para leer el buffer")
            dirEEPROM = (
                int(input("Ingrese la cantidad de registros que quiere leer: ")))
        flag = 2
    elif select == 3:
        opcion = 0
        flag=0
    else:
        opcion = 0


def escribirEEPROM(bus, address, direccion, data, size):
    longitud = size+2
    for i in range(longitud):
        msb, lsb = direccion >> 8, direccion & 0xFF
        buf = [msb, lsb]+data
        escribir = i2c_msg.write(address, buf)
        bus.i2c_rdwr(escribir)
        sleep(0.01)


def leerEEPROM(bus, address, direccion, size):
    data = []
    for i in range(1):
        msb, lsb = direccion >> 8, direccion & 0xFF
        escribir = i2c_msg.write(address, [msb, lsb])
        bus.i2c_rdwr(escribir)
        leer = i2c_msg.read(address, size)
        bus.i2c_rdwr(escribir, leer)
        data += list(leer)
        sleep(0.01)
    return data


def menu():
    global opcion, lectura, flag
    if opcion == 0:
        opcion = int(input("\nSleccione que quiere hacer: "))
    elif opcion == 1:
        leerSensor()
    elif opcion == 2:
        impTime()
        opcion = 0
    elif opcion == 3:
        menuwriteEEPROMM()
        confirmar = input("\nDigite y/n para confirmar: ")
        if confirmar == 'y':
            escribirEEPROM(bus, addEEPROM, dirEEPROM, saveEEPROM, noDatos)
            print("Guardado")
            opcion = 0
        else:
            opcion = 0
    elif opcion == 4:
        menureadEEPROM()
        if flag == 1:
            lectura = leerEEPROM(bus, addEEPROM, dirEEPROM, 1)
            print("%x" % (lectura[0]))
            lectura = []
            flag = 1
        elif flag == 2:
            lectura = leerEEPROM(bus, addEEPROM, dirEEPROM, noDatos)
            for i in lectura:
                print("[%x]" % (i), end="")
            print("\n")
            lectura = []
            flag = 2
    elif opcion == 5:
        escribirNibble()
        opcion = 0
    else:
        opcion = 0


def parar():
    global opcion
    imp()
    opcion = 0
    sleep(0.3)


stopButton.when_pressed = parar

imp()
while True:
    menu()
