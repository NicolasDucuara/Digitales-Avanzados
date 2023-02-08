from gpiozero import LEDBoard,Button,LED
from time import sleep,time
from signal import pause
from gpiozero import LEDMultiCharDisplay,LEDCharDisplay,Button,LED
from time import sleep,time
from signal import pause

d=LEDCharDisplay(25,5,6,26,16,13,12)
display=LEDMultiCharDisplay(d,23,24)

bmotor=Button(17,pull_up=0,hold_time=1)
bvalue=Button(27,pull_up=0,hold_time=1)
encoder=Button(22,pull_up=0)

inicio=LED(19)
inicio.value=0
contador=50
cont=0
vueltas=0

eAnterior=1
eActual=0

def aumento():
    sleep(1)
    global vueltas
    vueltas=1
    print("aumento")

def disminucion():
    global contador,vueltas,cont
    print("disminucion")
    contador-=1
    if vueltas==1:
        if cont>2:
            vueltas=0
    sleep(0.2)
        
        
def activar():
    global eAnterior,eActual
    if eAnterior!=eActual:
        print("encendido")
        inicio.value=1
        eActual=1
        sleep(0.2)
    else:
        print("apagado")
        inicio.value=0
        eActual=0
        sleep(0.2)
        
        
def reiniciar():
    print("Reseteado")
    global contador,eActual,eAnterior,vueltas
    contador=50
    eActual=0
    eAnterior=1
    vueltas=0
    inicio.value=0
    sleep(0.2)
    
    
def visualizacion():
    global contador,cont,vueltas
    display.value=str(contador)
    sleep(0.01)
    if vueltas==1:
        contador+=1
        cont+=1
        sleep(1)
    
    
bvalue.when_pressed=disminucion
bvalue.when_held=aumento

bmotor.when_pressed=activar
bmotor.when_held=reiniciar


while True:

    if 0<=contador<100:
        
        visualizacion()
            
        if inicio.value==1:
            if encoder.value==0:
                contador-=1
                while encoder.value==0:
                    pass
        
    else:
        inicio.value=0
        
            
        
    
    
        
