from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from hcsr04 import HCSR04
import time
import utime
from time import sleep
from oled_imagges import buscar_icono

infrarrojo = Pin(15, Pin.IN)
ultrasonido = HCSR04(trigger_pin = 4, echo_pin = 5)
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(01))
oled = SSD1306_I2C(ancho, alto, i2c)
contador=0
contadorV=0

print(i2c.scan())
 
oled.text('Proyecto Final', 6, 0)
oled.text('Diplomado', 26, 10)
oled.text('Python - Devnet', 3, 20)
oled.text('Bienvenidos', 17, 40)
oled.show()
time.sleep(4)
for i in range (0, 70):   
    oled.scroll(0,-1)
    oled.show()
    time.sleep(0.01)
 
oled.blit(buscar_icono("dibujos/Huella2.pbm"), 36, 0) # ruta y sitio de ubicación
oled.show()  #mostrar
time.sleep(3.5)
oled.fill(0)
oled.show()

while (True):
    
    try:
        lectura = infrarrojo.value()
        distancia = ultrasonido.distance_cm()
        print("Distancia = ", distancia)
        sleep(1)
        
        if distancia >= 10.00:
            contadorV += 1 #CON CONTADOR ENVIAR CORREO Y HACER DIVISION CON RESIDUO PARA CALCULAR MINUTOS Y SEGUNDOS
            oled.text('No hay comida', 10, 0)
            oled.blit(buscar_icono("images/ComidaVacia2.pbm"), 22, 20) # ruta y sitio de ubicación
            oled.text(str(contadorV), 0, 50)
            oled.show()
            time.sleep(0.01)
            oled.fill(0)
        elif lectura == 0:
            contador += 1 #CON CONTADOR ENVIAR CORREO Y HACER DIVISION CON RESIDUO PARA CALCULAR MINUTOS Y SEGUNDOS
            oled.text('Mascota comiendo', 0, 0)
            oled.blit(buscar_icono("images/Comida3.pbm"), 22, 20) # ruta y sitio de ubicación
            oled.text(str(contador), 0, 50)
            oled.show()
            time.sleep(0.01)
            oled.fill(0)
                                       
        else:
                            
            #msjOled1 = "Todo tranquilo"
            #msjOled2 = "por aca"
            oled.text("Todo tranquilo", 0, 10)
            oled.text("por aca", 0, 20)
            oled.show()
            time.sleep(0.01)
            oled.fill(0)
            contador=0
            contadorV=0
            #oled.poweroff()#Para apagar pantalla
                  
    except:
        print("Error!")
  
