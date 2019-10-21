from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import get_words 
from tkinter import messagebox
import cv2
from translator import traducer

class Aplicacion():
    def __init__(self):
    
        self.raiz = Tk()
        self.raiz.geometry('800x700')
        #self.raiz.resizable(width=False,height=False)
        self.raiz.title('WordToAll')
        
        self.titulo = Label (self.raiz, text="Get your Words", fg="blue", width=200)
        self.titulo.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.3, anchor='center')
        self.titulo.config(font=("Helvetica", 25))
    
        
        self.subtitulo = Label (self.raiz, text="Introduce la imagen a la que quieres traducir el texto")
        self.subtitulo.place(relx=0.5, rely=0.2, relwidth=1, relheight=0.1, anchor='center')
        self.subtitulo.config(font=("Arial Bold", 10))
        
        
        #Meter foto
        self.binfo = ttk.Button(self.raiz, text='Importar Imagen', command=self.meter_foto)
        self.binfo.place(relx=0.5, rely=0.42, relwidth=0.6, relheight=0.05, anchor='n')
    
        #Traducir
        self.tradu = Label (self.raiz, text="¿A que idioma quieres traducirlo?",font=("Arial Bold", 10))
        self.tradu.place(relx=0.3, rely=0.48, relwidth=0.75, relheight=0.1, anchor='n')
        
        #Caja tracuccion
        self.boxtraductor = ttk.Combobox(self.raiz)
        self.boxtraductor['values']= ('Español','Ingles','Japones','Chino','Aleman','Frances')
        self.boxtraductor.place(relx=0.75, rely=0.51, relwidth=0.3, relheight=0.04, anchor='n')
        
        #Traducir
        self.binfo = ttk.Button(self.raiz, text='Traducir', command=lambda:self.traducir(pic))
        self.binfo.place(relx=0.5, rely=0.6, relwidth=0.6, relheight=0.05, anchor='n')
        
        #Salir
        self.bsalir = ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy)
        self.bsalir.place(relx=0.5, rely=0.9, relwidth=0.3, relheight=0.05, anchor='n')
        
        
        self.binfo.focus_set()
        self.raiz.mainloop()
        


    def meter_foto(self):
        global pic
        global tkimage
        
        pic = filedialog.askopenfilename()
        
        img = Image.open(pic)
        img.thumbnail((300,300), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(img)
        self.bsalir= Label(self.raiz, image=tkimage)
        self.bsalir.place(relx=0.5, rely=0.32, relwidth=1, relheight=0.33, anchor='center')
    
    def traducir(self,pic): 
        global frase
        global leng
        frase = get_words.image_to_text(pic,19,0.01)

        
        if self.boxtraductor.get() == 'Español':
            leng = 'es'
        
        if self.boxtraductor.get() == 'Ingles':
            leng = 'en'

        if self.boxtraductor.get() == 'Chino':
            leng = 'zh-cn'

        if self.boxtraductor.get() == 'Japones':
            leng = 'ja'

        if self.boxtraductor.get() == 'Frances':
            leng = 'fr'

        if self.boxtraductor.get() == 'Aleman':
            leng = 'de'

        try:
            p_traducida = traducer(frase,leng)

        except:
            p_traducida = "El traductor no esta disponible en este momento, copia el texto y pegalo en google traductor."
        
        self.sintraducido =Label(self.raiz, text=frase, fg="white", bg='#001b52', width=50)
        self.sintraducido.place(relx=0.5, rely=0.72, relwidth=1, relheight=0.1, anchor='center')
        
        self.traducido =Label(self.raiz, text=p_traducida, fg="white", bg='#001b52', width=50)
        self.traducido.place(relx=0.5, rely=0.79, relwidth=1, relheight=0.1, anchor='center')
       
    

def main():
    mi_app = Aplicacion()
    return 0
    