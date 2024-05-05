from customtkinter import *
from PIL import Image
import subprocess
from tkinter.filedialog import askopenfilename
from skimage import io, exposure, color
import skimage
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import math
import scipy.ndimage as ndi




app=CTk()
app.geometry("1280x900")
set_appearance_mode("dark")

#Primera parte elección de imagen y carga de imagen

#Funcion para abrir explorador de archivos
filename=""
Img=""
def Image_resize(base,img):
    a=img.size[0]/img.size[1]
    if a >= 1:
        wpercent = (base / float(img.size[0]))
        bsize=base
        hsize = int((float(img.size[1]) * float(wpercent)))
    else:
        wpercent = (base / float(img.size[1]))
        hsize=base
        bsize = int((float(img.size[0]) * float(wpercent)))

    return hsize,bsize

def btn_New_Image_Com():
    global filename
    global Img
    global app
    filename=""
    Img=""
    filename = askopenfilename()
    if filename[-4:] == ".png" or filename[-4:] == ".jpg" or filename[-4:] == ".jpeg":
            img = Image.open(filename)
            bsize,hsize=Image_resize(500,img)
            Img2=CTkImage(light_image=Image.open(filename),dark_image=Image.open(filename),size=(bsize,hsize))
            lbl=CTkLabel(app,text="",image=Img2)
            lbl.pack(expand=True)
            lbl.place(relx=0.6, rely=0.5,anchor="center")
            Img= io.imread(filename)
    else:
        lbl_Warn=CTkLabel(app, text='Solo se admiten png,jpg o jpeg', width=100, height=28, fg_color="#AE5A41",bg_color="#AE5A41")
        lbl_Warn.pack(expand=True)
        lbl_Warn.place(relx=0.6, rely=0.5,anchor="center")
        
def Freq_Window():
    Freq_Win=CTkToplevel(app)
    Freq_Win.geometry("1280x900")
    
    Img2=CTkImage(light_image=Image.open(filename),dark_image=Image.open(filename),size=(bsize,hsize))
    lbl=CTkLabel(app,text="",image=Img2)
    
def btn_Continue():
    global Img
    global app
    def Close_Cont():
        new_window.destroy()
        Freq_Window()
    if(len(Img.shape)<3):
        new_window=CTkToplevel(app)
        new_window.geometry("500x400")
        lbl_Init=CTkLabel(new_window, text='Se procesara la imagen seleccionada mediante convolución y FFT', width=40, height=28)
        lbl_Init.place(relx=0.5, rely=0.5,anchor="center")
        Cont_Btn=CTkButton(new_window, text='Continuar',corner_radius=12,fg_color="#559e83",text_color="black",border_color="#559e83",command=Close_Cont)
        Cont_Btn.place(relx=0.5, rely=0.7, anchor="center")
    elif len(Img.shape)==3:
        new_window=CTkToplevel(app)
        new_window.geometry("500x400")
        lbl_Init=CTkLabel(new_window, text='Su imagen es RGB se pasará a grises para ser tratada', width=40, height=28)
        lbl_Init.place(relx=0.5, rely=0.5,anchor="center")
        Cont_Btn=CTkButton(new_window, text='Continuar',corner_radius=12,fg_color="#559e83",text_color="black",border_color="#559e83",command=Close_Cont)
        Cont_Btn.place(relx=0.5, rely=0.7, anchor="center")



#Frame naranja
frame = CTkFrame(app, width=400, height=1200, fg_color="#AE5A41")
frame.pack(expand=True)
frame.place(relx=0.1, rely=0.7,anchor="center")

#Frame naranja para imagen
frame2 = CTkFrame(app, width=600, height=600, fg_color="#AE5A41")
frame2.pack(expand=True)
frame2.place(relx=0.6, rely=0.5,anchor="center")

#Label que diga proyecto
lbl_Init=CTkLabel(app, text='Proyecto ', width=40, height=28, fg_color="#AE5A41",bg_color="#AE5A41")
lbl_Init.place(relx=0.1, rely=0.1,anchor="center")

#Botón para subir nueva imagen
btn_New_Image = CTkButton(master=app, text='Nueva Imagen',corner_radius=12,bg_color="#AE5A41",fg_color="#559e83",text_color="black",border_color="#559e83",command=btn_New_Image_Com)
btn_New_Image.place(relx=0.1, rely=0.3, anchor="center")

#Botón para continuar
btn_Cont_Bord = CTkButton(master=app, text='Continuar',corner_radius=12,bg_color="#AE5A41",fg_color="#559e83",text_color="black",border_color="#559e83",command=btn_Continue)
btn_Cont_Bord.place(relx=0.1, rely=0.4, anchor="center")



#Funciones para subir imagen

app.mainloop()