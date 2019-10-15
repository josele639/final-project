##### Funcion procesamiento de texto #####

import pytesseract

def ocr(imagen):
    config = ("-l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(imagen, config=config)
    if text:
        #print(text)
        return text
    else:
        #print("No ha detectado nada")
        return ''