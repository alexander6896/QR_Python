# -*- coding: utf-8 -*-
from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import MySQLdb

db = MySQLdb.connect(host="65.99.225.8",    # tu host, usualmente localhost
                     port=3306,
                     user="itqiscco_alex",         # tu usuario
                     passwd="vladimir6896",  # tu password
                     db="itqiscco_regitstro")        # el nombre de la base de datos

# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(2)

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

#Diccionario
estacionamiento = dict()
estacionamiento = {
  1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "",
  11: "", 12: "", 13: "", 14: "", 15: "", 16: "", 17: "", 18: "", 19: "", 20: "",
  21: "", 22: "", 23: "", 24: "", 25: "", 26: "", 27: "", 28: "", 29: "", 30: "",
  31: "", 32: "", 33: "", 34: "", 35: "", 36: "", 37: "", 38: "", 39: "", 40: "",
}

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type1 : ', decodedObject.type)
        print('Data1 : ', decodedObject.data,'\n')
        
        #Pasar a string el dato mandado desde el celular
        datoConsulta = str(decodedObject.data)
        print("DAtos a la BD: ", datoConsulta)
        #Tiempo para leer otro dato espera 5 segundos
        time.sleep(5)
        #ENCONTRAR LA FORMA DE CONECTAR A BASE DE DATOS Y CREAR LA COLA
        cursor = db.cursor()
        #Consulta hacia la Base de Datos
        sql = "Select * From estacionamiento where `no.control`='%s'"%(datoConsulta)
        cursor.execute(sql)
        result = cursor.fetchall()
        print (result)
        #Obtencion de ciertas datos de la consulta
        for row in result:
              #palabrasSeparadas = row[1:3]
              nombre = row[1]
              placas = row[4]
              noControl = row[5]
        print ("Nombre: ",nombre)
        print ("Placas: ",placas)
        print ("No. Control: ",noControl)
        datosUsuario = nombre+" "+placas+" "+noControl
        print ("Los datos del usuarios son: ",datosUsuario)

        ingresoSalida = str(input("Vas a entrar(1) o salir(2)\n"))
        if(ingresoSalida == "1"):
              print ("Ingresa el lugar de estacionamiento a elegir los disponibles son los lugares vacios")
              lugar = input("¿Que lugar vas a seleccionar?\n->")
              for k,v in estacionamiento.items():
                print ("%s -> %s" %(k,v))
              
              print ("El lugar apartado es el ", lugar)
              estacionamiento.update({lugar: datosUsuario})

              for k,v in estacionamiento.items():
                    print ("%s -> %s" %(k,v))
        else:
              lugar = input("¿De que lugar vas a salir?\n->")
              print ("Ingresa el lugar de estacionamiento del cual vas a salir")
              
              print ("El lugar apartado es el ", lugar)
              estacionamiento.update({lugar: ""})

              for k,v in estacionamiento.items():
                    print ("%s -> %s" %(k,v))
        
        """
        #Uso del diccionario estacionamiento para que un usuario use un lugar del estacionamiento
        lugar = input("¿Que lugar vas a seleccionar?\n")
        print ("Ingresa el lugar de estacionamiento a elegir los disponibles son los lugares vacios")

        #Imprimir el diccionario
        for k,v in estacionamiento.items():
          print ("%s -> %s" %(k,v))

        print ("El lugar apartado es el ", lugar)

        estacionamiento.update({lugar: datosUsuario})

        #Imprimir el diccionario
        for k,v in estacionamiento.items():
          print ("%s -> %s" %(k,v))"""

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save 
        cv2.imwrite('Capture.png', frame)     

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()