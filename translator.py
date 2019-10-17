from googletrans import Translator

def traducer(frase, idi):              
    traductor=Translator()
    traduccion=traductor.translate(frase,dest=idi)
    print(traduccion)
    return traduccion.text

