#@author: Hollmann Stiven Peñuela Parra

#Librerias
from machine import Pin, I2C #Para definicion de pines y OLED
from ssd1306 import SSD1306_I2C #Para funciones OLED
from hcsr04 import HCSR04 #Sensor ultrasonido
import time, utime, network, urequests #Manejo de tiempos de funcionalidad y envio de request
from time import sleep
from Funciones import buscar_icono, conectaWifi #funciones definidas en otro modulo

#Se pide nombre a mascota para usarlo en el proceso
mascota = input("Digite el nombre de su mascota y presione enter: ")
while not mascota or mascota.isspace(): #Se valida que no ingrese una variable vacia o espacios
    mascota = input("Porfavor digite un nombre: ")

#Definición de variables para elementos del circuito
infrarrojo = Pin(15, Pin.IN)
ultrasonido = HCSR04(trigger_pin = 4, echo_pin = 5)
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(01))
oled = SSD1306_I2C(ancho, alto, i2c)
contador=0
contadorV=0
acercamientos = 0

#Condicional de conexión a wifi 
if conectaWifi ("Hip Hop In Tha House", "WeAllLiveInAStoneWorldHH"):

#Mensajes que se proyectan en la OLED al ejecutar
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
     
    oled.blit(buscar_icono("dibujos/Huella2.pbm"), 36, 0) # ruta y sitio de ubicación para insertar imagen
    oled.show()
    time.sleep(3.5)
    oled.fill(0)
    oled.show()
    
    print(i2c.scan())

#Inicio de condicional para ejecución de código
    while (True):
        #Se define try except ya que es necesario para Ultrasonido 
        try:
            #Variables de lectura de sensores
            lectura = infrarrojo.value()
            distancia = ultrasonido.distance_cm()
            sleep(1)
            tiempo = time.localtime()#Convierte la hora y fecha actual en una tupla
            hora_completa = str(tiempo[3])+":"+str(tiempo[4])+":"+str(tiempo[5])
            fecha_completa = str(tiempo[2])+"/"+str(tiempo[1])+"/"+str(tiempo[0])
            
            #Condicional para enviar correo diario a la hora especificada, envia datos a grafico Thinspeak
            if hora_completa == "15:19:0" or hora_completa == "15:19:1" or hora_completa == "15:19:2":
                url_2 = "https://api.thingspeak.com/update?api_key=3J0RXK2IK9DSPUSA"
                respuesta = urequests.get(url_2+"&field1="+str(acercamientos))
                respuesta.close ()
                url = "https://maker.ifttt.com/trigger/RecopilacionAcercamientos/with/key/cI1BM7XfS78Z0HbRgu4wNe?"
                respuesta = urequests.get(url+"&value1="+mascota+"&value2="+fecha_completa+"&value3="+str(acercamientos))
                respuesta.close ()
                oled.text('Enviando informe', 0, 0)
                oled.text('diario', 38, 10)
                oled.blit(buscar_icono("images/Mail2.pbm"), 35, 30) # ruta y sitio de ubicación
                oled.show()
                time.sleep(4)
                oled.fill(0)
                
            
            #Condicional para Hcsr04 midiendo distancia de alimento en recipiente
            if distancia >= 10.00:
                
                contadorV += 1 #CON CONTADOR ENVIAR CORREO Y HACER DIVISION CON RESIDUO PARA CALCULAR MINUTOS Y SEGUNDOS
                #Se envian datos a pantalla OLED
                oled.text('No hay comida', 10, 0)
                oled.blit(buscar_icono("images/ComidaVacia2.pbm"), 22, 20) # ruta y sitio de ubicación
                oled.show()
                time.sleep(0.01)
                oled.fill(0)
                #Cuando el recipiente lleva un tiempo vacio se envia correo de alerta
                if contadorV == 4:
                    url = "https://maker.ifttt.com/trigger/NoComida/with/key/cI1BM7XfS78Z0HbRgu4wNe?"
                    respuesta = urequests.get(url+"&value1="+mascota+"&value2="+str(distancia))      
                    respuesta.close ()
                    oled.fill(0)
            #Si el animal esta cerca a la comida se envia información a OLED        
            elif lectura == 0:
                contador += 1 #CON CONTADOR ENVIAR CORREO Y HACER DIVISION CON RESIDUO PARA CALCULAR MINUTOS Y SEGUNDOS
                oled.text('Mascota comiendo', 0, 0)
                oled.blit(buscar_icono("images/Comida3.pbm"), 22, 20) # ruta y sitio de ubicación
                oled.show()
                time.sleep(0.01)
                oled.fill(0)
                #Si la mascota lleva un tiempo cerca al recipiente se envia notificación a correo
                if contador == 4:
                    acercamientos += 1
                    tiempo = time.localtime()#Convierte la hora y fecha actual en una tupla
                    fecha_completa = str(tiempo[2])+"/"+str(tiempo[1])+"/"+str(tiempo[0])
                    url = "https://maker.ifttt.com/trigger/MascotaComiendo/with/key/cI1BM7XfS78Z0HbRgu4wNe?"
                    respuesta = urequests.get(url+"&value1="+mascota+"&value2="+str(distancia))
                    respuesta.close ()
                    oled.fill(0)
            #Si el animal no se encuentra cerca de la comida y hay comida se presenta mensaje y los contadores se reinician        
            else:
                oled.text("Todo tranquilo", 0, 10)
                oled.text("por aca", 0, 20)
                oled.show()
                time.sleep(0.01)
                oled.fill(0)
                contador=0
                contadorV=0     
        except:
            print("Error!")    
#En caso de que no se pueda hacer la conexión a wifi se envia mensaje de error y no se ejecuta el programa
else:
       print ("Imposible conectar")
       miRed.active (False)
 
