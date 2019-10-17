from PIL import Image
import pandas as pd
import numpy as np
import cv2
import os
import sys
import time
from matplotlib.pyplot import imshow as ims
import matplotlib
import pytesseract 
import pylab as pl
import math
from imutils.object_detection import non_max_suppression

import box_to_order
import improve_img
import get_text


def preparar_imagen(imagen,alto, ancho):#cogemos imagen
    image = cv2.imread(imagen)
    #hacemos copia
    orig = image.copy()
    
    #sacamos alto y ancho
    (H, W) = image.shape[:2]

    
    proporcion = H/W
    alto= int(alto * proporcion)
        
    #ponemos el nuevo alto y ancho, ¿PORQUE? Para hacerlo multiplo de 32, que se ajuste por tipo de pixel
    (newW, newH) = (ancho*32, alto*32)
    rW = W / float(newW)
    rH = H / float(newH)
    

    #lo aplicamos a la imagen y sacamos H y W de nuevo
    image = cv2.resize(image, (newW ,newH))
    
    (H, W) = image.shape[:2]
    
    return orig, image, rW, rH, H, W

#funcion para detectar las palabra y etiquetar los puntos
def detectar_palabras(image, H, W):
    #nombre de las etiquetas principales, REVISAR
    layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]
    #Importamos el detector de texto, REVISAR que es el EAST
    #print("[INFO] loading EAST text detector...")
   
    
   
    
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")
    #net = cv2.dnn.readNetFromDarknet(frozen_east_text_detection.pb)
    #Construimos el cuadrito que va a rodear la imagen
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),(123.68, 116.78, 103.94), swapRB=True, crop=False)
    #start = time.time()
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    #end = time.time()

    #Muestra info sobre cuanto ha tardado en detectarlo
    #print("[INFO] text detection took {:.6f} seconds".format(end - start))

    #Construimos los planos para meter los cuadritos alrrededor de los textos
    #numRows te da el numero de palabras identificadas por sus
    (numRows, numCols) = scores.shape[2:4]
    
    
    return numRows, numCols, scores, geometry

def get_esquinas(numRows, numCols, scores, geometry):
    rects = []
    confidences = []
    for y in range(0, numRows):
        #Con los scores, probabilidad de que este bien, seguido de los
        #punto geometricos los ponemos en el texto para saber donde estan 

        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop sobre el numero de columnas
        for x in range(0, numCols):
            #metemos una variable de que si no hay suficiente confianza no lo meta, INVESTIGAR Y DECIDIR
            if scoresData[x] < 0.05: #args["min_confidence"]:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            #Extraer el angulo del texto para poder poner el recuadro girado
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)


            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

      
            #Crear los puntos exactos donde se debe poner el recuadro
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)


            #Añadirlo a la lista de cuadros y de confianza
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
            
            
            
    return rects, confidences


def recortar_palabras(orig, rects, confidences, rW, rH, padding , H, W):

   
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    palabras_separadas = []
    
    boxes = box_to_order.get_orden(boxes)

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
            #Hacemos un reescalado del cuadrito identificador acorde al que hicimos al principio.
            startX = int(startX * rW)
            if int(startX - (startX * padding))  > 0:
                startX = int(startX - (startX * padding))
            startY = int(startY * rH)
            if int(startY - (startY * padding)) > 0:
                startY = int(startY - (startY * padding))
            endX = int(endX * rW)
            if int(endX + (endX * padding)) > 0:
                endX = int(endX + (endX * padding))
            endY = int(endY * rH)
            if int(endY + (endY * padding)) > 0:
                endY = int(endY + (endY * padding))

      
            #Dibujar el rectangulo alrededor del texto en la imagen.
            crop = orig[startY:endY,startX:endX]
            #cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 3)
            palabras_separadas.append(crop)

        
    
    return palabras_separadas, orig, boxes


def image_to_text(nombre_imagen, size, pad, resize = True, tratar = True, tratar_mas=True):
    orig, image, rW, rH, H, W = preparar_imagen(nombre_imagen,size,size) #Multiplicar 32 por algo para hacer su multiplo
    numRows, numCols, scores, geometry = detectar_palabras(image, H, W)
    rects, confidences = get_esquinas(numRows, numCols, scores, geometry)
    palabras, orig, boxes = recortar_palabras(orig, rects, confidences,rW, rH, pad , H, W)
    imagenes_finales = []

    palabras_text = []
    for i in range(len(palabras)):
            if resize:
                imagen_resize = improve_img.resize_imagen(palabras[i],int(2000/size))
            if tratar:
                imagen_tratada = improve_img.tratar_imagen(imagen_resize)
            if tratar_mas:
                imagen_final = improve_img.tratar_img_2(imagen_tratada)
            else:
                imagen_final = palabras[i]
    
            
            imagenes_finales.append(imagen_final) 
            ocrtext = get_text.ocr(imagenes_finales[i])
            palabras_text.append(ocrtext)
            
    frase = get_text.unificar_texto(palabras_text)
    
    return frase 
