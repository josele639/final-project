# TuText

El objetivo del proyecto es crear un programa que sea capaz de traducir el texto de una fotografia.

Puede utilizarse con carteles, rotulos, y toda clase de imagenes con texto en el que las palabras no tengan un tamaño y separacion muy diferente.

El proyecto esta compuesto de 6 pasos diferenciados:

1 - En primer lugar se coge la imagen y se realiza un preprocesado para poder pasarla por el modelo.
2 - En segundo lugar se utiliza un modelo para detectar la posicion de las palabras de la fotografia.
3 - Se ordenan las posiciones y se obtiene una imagen de cada palabra.
4 - Se elimina el ruido de las imagenes para poder obtener el texto con pytesseract.
5 - Se obtiene el texto.
6 - Se traduce.

La carpeta del proyecto incluye estas carpetas y archivos:

main.py = El archivo con el que se lanza el programa, lanza tkinterprog.py
tkinterprog.py = Archivo en el que esta la interfaz del programa.
    get_words.py = El archivo con el que se consigue el texto de la imagen, dentro de este se utilizan los siguientes archivos:
        box_to_orden = Para ordenar las diferenteres imagenes.
        improve_img.py = Para preprocesar la imagen antes de pasarla a texto.
        get_text.py = Para obtener el texto de las imagenes
    translator.py = Archivo para traducir el texto conseguido.

Dentro tambien esta la carpeta "env" que tiene el envarement con todos las librerias necesarias para que funcione el programa.

Y el archivo frozen_east_text_detection.pb, que es el modelo para detectar el texto.

Espero que disfrutes mi proyecto tanto como yo he disfrutado haciendolo.
