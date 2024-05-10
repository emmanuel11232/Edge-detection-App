from customtkinter import *
from PIL import Image
import subprocess
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from skimage import io, exposure, color
import skimage
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import math
import scipy.ndimage as ndi
from skimage.filters import sobel, prewitt, scharr
from scipy.fft import fft2, fftshift

from skimage import io, color, filters
from skimage.filters import threshold_local

# Función para convertir la imagen a tonos de gris si es a color
def convert_to_grayscale(image):
    if len(image.shape) == 3:  # Comprobamos si la imagen es a color
        # Ignoramos el canal alfa si existe
        if image.shape[2] == 4:
            image = image[:, :, :3]
        grayscale_image = color.rgb2gray(image)
    else:
        grayscale_image = image
    return grayscale_image

def Frec_Treatment(imagen,valor_rectangulo):
    # Convertir la imagen a tonos de gris si es a color
    imagen_gris = convert_to_grayscale(imagen)

    # Calcular la FFT de la imagen en escala de grises
    fft_imagen_gris = np.fft.fft2(imagen_gris)

    # Aplicar la FFT de desplazamiento
    fft_shifted = np.fft.fftshift(fft_imagen_gris)

    # Definir las dimensiones del rectángulo del filtro
    rows, cols = fft_shifted.shape
    center_row, center_col = rows // 2, cols // 2
    rect_height = int(rows * valor_rectangulo)
    rect_width = int(cols * valor_rectangulo)

    # Crear la matriz del filtro
    filtro_pasa_alta = np.ones_like(fft_shifted)
    filtro_pasa_alta[center_row - rect_height // 2:center_row + rect_height // 2, 
                    center_col - rect_width // 2:center_col + rect_width // 2] = 0

    # Aplicar el filtro a la FFT
    fft_filtred = fft_shifted * filtro_pasa_alta

    # Calcular la FFT inversa y obtener la imagen filtrada
    imagen_filtrada = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_filtred)))

    # Iterar sobre los píxeles de la imagen filtrada y aplicar umbralización
    umbral = 0.1  # Umbral para decidir si un píxel es blanco o negro
    imagen_umbralizada = np.zeros_like(imagen_filtrada)  # Inicializar la imagen umbralizada

    # Iterar sobre los píxeles
    for i in range(imagen_filtrada.shape[0]):
        for j in range(imagen_filtrada.shape[1]):
            # Si el valor del píxel es mayor que el umbral, establecerlo como blanco en la imagen umbralizada
            if imagen_filtrada[i, j] > umbral:
                imagen_umbralizada[i, j] = 1
    
    return imagen_umbralizada

app=CTk()
app.geometry("1280x900")
set_appearance_mode("dark")

#Primera parte elección de imagen y carga de imagen

#Funcion para abrir explorador de archivos
filename=""
Img=""
Freq=0
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
    if filename[-4:] == ".png" or filename[-4:] == ".jpg" or filename[-5:] == ".jpeg":
            Img = Image.open(filename)
            hsize,bsize=Image_resize(500,Img)
            Img2=CTkImage(light_image=Image.open(filename),dark_image=Image.open(filename),size=(bsize,hsize))
            lbl=CTkLabel(app,text="",image=Img2)
            lbl.pack(expand=True)
            lbl.place(relx=0.6, rely=0.5,anchor="center")
            Img= io.imread(filename)
    else:
        lbl_Warn=CTkLabel(app, text='Solo se admiten png,jpg o jpeg', width=100, height=28, fg_color="#AE5A41",bg_color="#AE5A41")
        lbl_Warn.pack(expand=True)
        lbl_Warn.place(relx=0.6, rely=0.5,anchor="center")

def Res_Win():
    global Freq
    Res_Win=CTkToplevel(app)
    Res_Win.geometry("1280x900")
    Tab=CTkTabview(master=Res_Win,width=600,height=600)
    Tab.pack(padx=80,pady=80)

    Original=Tab.add("Original")
    Edge_FFT=Tab.add("FFT")
    Edge_Conv=Tab.add("Conv")

    #Print original en gris
    image2=Img.convert(mode="L")
    hsize,bsize=Image_resize(500,image2)
    Img2=CTkImage(light_image = image2 ,dark_image = image2 ,size = (bsize,hsize))
    lbl=CTkLabel(Original,text="",image=Img2)
    lbl.pack(expand=True)
    lbl.place(relx=0.5, rely=0.5,anchor="center")

    #Edge by FFT
    my_path=askdirectory()
    Img_2_Treat= io.imread(filename)
    Img_FFT=Frec_Treatment(Img_2_Treat,(Freq/100))

    plt.imshow(Img_FFT, cmap=plt.cm.gray)
    plt.title('Detección para la frecuencia dada')
    plt.savefig(os.path.join(my_path,"FFT.png"), bbox_inches='tight')
    plt.close()

    image_FFT=Image.open(os.path.join(my_path,"FFT.png"))

    hsize,bsize=Image_resize(500,image_FFT)
    Img3=CTkImage(light_image = image_FFT ,dark_image = image_FFT ,size = (bsize,hsize))
    lbl=CTkLabel(Edge_FFT,text="",image=Img3)
    lbl.pack(expand=True)
    lbl.place(relx=0.5, rely=0.5,anchor="center")

    #Edge by prewitt
    gray_Img = skimage.color.rgb2gray(Img)
    #Apply Prewitt filter to the image 'gray_candy'
    prewitt_filtered = prewitt(gray_Img)

    plt.imshow(prewitt_filtered, cmap=plt.cm.gray)
    plt.title('Prewitt Filter')
    plt.savefig(os.path.join(my_path,"PwFilt.png"), bbox_inches='tight')
    plt.close()

    image_Prewitt=Image.open(os.path.join(my_path,"PwFilt.png"))


    hsize,bsize=Image_resize(500,image_Prewitt)
    Img_f=CTkImage(light_image=image_Prewitt,dark_image=image_Prewitt,size=(bsize,hsize))
    lbl_f=CTkLabel(Edge_Conv,text="",image=Img_f)
    lbl_f.pack(expand=True)
    lbl_f.place(relx=0.5, rely=0.5,anchor="center")
    print(Freq)   


def Freq_Window():
    global Img
    global filename
    global Freq
    Img = Image.open(filename)
    Freq_Win=CTkToplevel(app)
    Freq_Win.geometry("1280x900")
    frame_Freq = CTkFrame(Freq_Win, width=1000, height=600, fg_color="#AE5A41")
    frame_Freq.pack(expand=True)
    frame_Freq.place(relx=0.5, rely=0.4,anchor="center")
    hsize,bsize=Image_resize(400,Img)
    image_gray=Img.convert(mode="L")
    Img2=CTkImage(light_image=image_gray,dark_image=image_gray,size=(bsize,hsize))
    lbl=CTkLabel(Freq_Win,text="",image=Img2)
    lbl.pack(expand=True)
    lbl.place(relx=0.3, rely=0.4,anchor="center")

    image = skimage.img_as_float(skimage.color.rgb2gray(Img))
    image_f = np.abs(fftshift(fft2(image)))
    image_f=Image.fromarray(image_f)

    plt.figure(facecolor="#AE5A41")
    plt.title("Original FFT")
    plt.imshow(image_f)
    my_path=asksaveasfilename()
    plt.savefig(my_path, bbox_inches='tight') 
    plt.close()

    
    image_f=Image.open(my_path)

    hsize,bsize=Image_resize(400,image_f)
    Img_f=CTkImage(light_image=image_f,dark_image=image_f,size=(bsize,hsize))
    lbl_f=CTkLabel(Freq_Win,text="",image=Img_f)
    lbl_f.pack(expand=True)
    lbl_f.place(relx=0.7, rely=0.4,anchor="center")
    def sliding(value):
        lbl_slide.configure(text=int(value))

    slide=CTkSlider(Freq_Win,from_=0,to=100,command=sliding,bg_color="#AE5A41")
    slide.place(relx=0.5, rely=0.7,anchor="center")

    lbl_slide=CTkLabel(Freq_Win,text=slide.get(),bg_color="#AE5A41")
    lbl_slide.place(relx=0.5, rely=0.725,anchor="center")

    def Close_Cont_Freq():
        global Freq 
        Freq=slide.get()
        Freq_Win.destroy()
        Res_Win()
    Cont_Btn=CTkButton(Freq_Win, text='Continuar',corner_radius=12,fg_color="#559e83",text_color="black",border_color="#559e83",command=Close_Cont_Freq)
    Cont_Btn.place(relx=0.5, rely=0.8, anchor="center")
    

    
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