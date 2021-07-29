import network, time, urequests
from time import sleep
import framebuf #Para trabajar con imagenes

def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)


def conectaWifi (red, password):    
  global miRed
  miRed = network.WLAN(network.STA_IF)     
  
  if not miRed.isconnected():              #Si no está conectado…    
      miRed.active(True)                   #activa la interface
      miRed.connect(red, password)         #Intenta conectar con la red
      print('Conectando a la red', red +"…")
      timeout = time.time ()
      while not miRed.isconnected():           #Mientras no se conecte..
          
          if (time.ticks_diff (time.time (), timeout) > 10):              
              return False
  return True