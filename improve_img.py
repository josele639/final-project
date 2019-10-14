

##### Funciones tratamiento de la imagen  #####

import cv2

def tratar_imagen(f_palabra):
    gray = cv2.cvtColor(f_palabra, cv2.COLOR_BGR2GRAY)
    return gray

def tratar_img_2(f_palabra):
    img = cv2.threshold(f_palabra, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return img

def resize_imagen(f_palabra, n):
    r = n/ f_palabra.shape[1]
    dim = (n, int(f_palabra.shape[0]*r))

    resized = cv2.resize(f_palabra, dim, interpolation = cv2.INTER_AREA)
    return resized
