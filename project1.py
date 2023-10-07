import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import cv2 as cv
from tkinter.filedialog import asksaveasfile

my_w = tk.Tk()
my_w.geometry("1300x620")
my_w.minsize(1250,620)
my_w.maxsize(1250,620)
my_w.title('Project1')
l1 = tk.Label(my_w,text='Upload Files & Display', width=30)
l1.place(x=-1, y=12)
b1 = tk.Button(my_w, text='Upload Files', width=20, bg='#F9D7B3', command=lambda: upload_file())
b1.place(x=40, y=32)

b2 = tk.Button(my_w,  text='Do the thing', width=20, bg='#F9D7B3', command=lambda: apply_filter(c))
b2.place(x=210, y=32)

b3 = tk.Button(my_w,  text='Histogram Equalization', width=20, bg='#F9D7B3', command=lambda: select_filter(1))
b3.place(x=550, y=32)

b4 = tk.Button(my_w,  text='Edge Detection', width=20, bg='#F9D7B3', command=lambda: select_filter(2))
b4.place(x=720, y=32)

b5 = tk.Button(my_w,  text='Sharpening', width=20, bg='#F9D7B3', command=lambda: select_filter(3))
b5.place(x=890, y=32)

b6 = tk.Button(my_w,  text='Denoising', width=20, bg='#F9D7B3', command=lambda: select_filter(4))
b6.place(x=1060, y=32)

global contrast_val, brightness_val, rgb_val

l2 = tk.Label(my_w, text='Contrast', width=30)
l2.place(x=35, y=550)
contrast_val = 50.0

l3 = tk.Label(my_w, text='Brightness', width=30)
l3.place(x=305, y=550)
brightness_val = 50.0

l4 = tk.Label(my_w, text='Color', width=30)
l4.place(x=575, y=550)
rgb_val = 50.0

global b, o, r
global modified_img
global trash
trash = Image.open("white.jpg")
trash = trash.resize((400, 450))
trash = ImageTk.PhotoImage(trash)

o = 0
b = 0
r = 0


def upload_file():
    f_types = [('Jpg Files', '*.jpg'),
    ('PNG Files','*.png')]   # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=False,filetypes=f_types)
    global img, img2, img3, backup, e1, e2, e3, l5, l6, img_no
    img = Image.open(filename)  # read the image file
    img = img.resize((400, 450))  # new width & height
    backup = img
    contrast_slider.set(50)
    brightness_slider.set(50)
    rgb_slider.set(50)

    pho = ImageTk.PhotoImage(img)

    e1 = tk.Label(my_w)
    e1.place(x=5,y=70)
    e1.image = pho
    e1['image'] = pho

    e2 = tk.Label(my_w,image = trash)
    e2.place(x=420, y=70)

    e3 = tk.Label(my_w,image = trash)
    e3.place(x=835, y=70)

    l5 = tk.Label(my_w,text='',width=30)
    l5.place(x=520, y=475)

    l6 = tk.Label(my_w, text='',width=30)
    l6.place(x=950, y=475)

def hist_eq():
    global img2, img3
    arr_img = np.array(img)
    if img.mode =="L":
        equ = cv.equalizeHist(arr_img)
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(arr_img)
    elif img.mode =="RGB":
        gray = cv.cvtColor(arr_img, cv.COLOR_BGR2GRAY)
        equ = cv.equalizeHist(gray)
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(gray)
    elif img.mode =="RGBA":
        gray = cv.cvtColor(arr_img,cv.COLOR_RGBA2GRAY)
        equ = cv.equalizeHist(gray)
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(gray)

    equ = Image.fromarray(equ)
    img2 = equ
    equ = ImageTk.PhotoImage(equ)
    e2.image = equ
    e2['image'] = equ
    l5.config(text='Normal HE')
    l5.place(x=520, y=525)

    cl1 = Image.fromarray(cl1)
    img3 = cl1
    cl1 = ImageTk.PhotoImage(cl1)

    e3.image = cl1
    e3['image'] = cl1
    l6.config(text='CLAHE')
    l6.place(x=930, y=525)


def edge_detection():
    global img2, img3
    arr_img = np.array(img)
    img_blur = cv.GaussianBlur(arr_img, (3, 3), 0)

    if img.mode == "RGB":
        gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
        sobelxy = cv.Sobel(src=gray, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)
        edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)
    elif img.mode == "L" :
        sobelxy = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)
        edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)
    elif img.mode == "RGBA":
        gray = cv.cvtColor(img_blur, cv.COLOR_RGBA2GRAY)
        sobelxy = cv.Sobel(src=gray, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)
        edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)

    sobelxy = Image.fromarray(sobelxy)
    img2 = sobelxy
    sobelxy = ImageTk.PhotoImage(sobelxy)
    e2.image = sobelxy
    e2['image'] = sobelxy
    l5.config(text='X-Y sobel')
    l5.place(x=520, y=525)

    edges = Image.fromarray(edges)
    img3 = edges
    edges = ImageTk.PhotoImage(edges)
    e3.image = edges
    e3['image'] = edges
    l6.config(text='Canny')
    l6.place(x=930, y=525)


def sharpening():
    global img2
    arr_img = np.array(img)
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened = cv.filter2D(arr_img, -1, kernel)

    sharpened = Image.fromarray(sharpened)
    img2 = sharpened
    sharpened = ImageTk.PhotoImage(sharpened)
    e2.image = sharpened
    e2['image'] = sharpened
    l5.config(text='Sharp')
    l5.place(x=520, y=525)

    e3.image = trash
    e3['image'] = trash
    l6.config(text='')
    l6.place(x=930, y=525)



def denoising():
    global img2
    arr_img = np.array(img)
    if img.mode == "L":
        dst = cv.fastNlMeansDenoising(arr_img, None, 20, 7, 21)
    else:
        dst = cv.fastNlMeansDenoisingColored(arr_img, None, 10, 10, 7, 21)

    dst = Image.fromarray(dst)
    img2 = dst
    dst = ImageTk.PhotoImage(dst)
    e2.image = dst
    e2['image'] = dst
    l5.config(text='Denoised')
    l5.place(x=520, y=525)

    e3.image = trash
    e3['image'] = trash
    l6.config(text='')
    l6.place(x=930, y=525)


def select_filter(x):
    global c
    c = x
    if c == 1:
        b3.configure(bg='#FFA84B')
        b4.configure(bg='#F9D7B3')
        b5.configure(bg='#F9D7B3')
        b6.configure(bg='#F9D7B3')

    elif c == 2:
        b3.configure(bg='#F9D7B3')
        b4.configure(bg='#FFA84B')
        b5.configure(bg='#F9D7B3')
        b6.configure(bg='#F9D7B3')

    elif c == 3:
        b3.configure(bg='#F9D7B3')
        b4.configure(bg='#F9D7B3')
        b5.configure(bg='#FFA84B')
        b6.configure(bg='#F9D7B3')

    elif c == 4:
        b3.configure(bg='#F9D7B3')
        b4.configure(bg='#F9D7B3')
        b5.configure(bg='#F9D7B3')
        b6.configure(bg='#FFA84B')

    elif c == 5:
        b3.configure(bg='#F9D7B3')
        b4.configure(bg='#F9D7B3')
        b5.configure(bg='#F9D7B3')
        b6.configure(bg='#F9D7B3')

    elif c == 6:
        b3.configure(bg='#F9D7B3')
        b4.configure(bg='#F9D7B3')
        b5.configure(bg='#F9D7B3')
        b6.configure(bg='#F9D7B3')


def apply_filter(c):
    if c == 1:
        return hist_eq()

    elif c == 2:
        return edge_detection()

    elif c == 3:
        return sharpening()

    elif c == 4:
        return denoising()


def change_contrast(var):
    global img, modified_img, contrast_val, brightness_val, rgb_val, b, o, r, backup, img_no
    b = 1
    r = 1
    if o == 1:
        img = ImageEnhance.Brightness(backup).enhance((brightness_val/50))
        img = ImageEnhance.Color(img).enhance((rgb_val * 0.04) - 1)
    contrast_val = int(var)
    modified_img = ImageEnhance.Contrast(img).enhance((contrast_val * 0.04) - 1)
    pho = ImageTk.PhotoImage(modified_img)
    e1.image = pho
    e1['image'] = pho
    img = img.resize((400, 450))
    o = 0


def change_brightness(var):
    global img, modified_img, contrast_val, brightness_val, rgb_val, b, o, r, backup, img_no
    r = 1
    o = 1
    if b == 1:
        img = ImageEnhance.Color(backup).enhance((rgb_val * 0.04) - 1)
        img = ImageEnhance.Contrast(img).enhance((contrast_val * 0.04) - 1)
    brightness_val = int(var)
    modified_img = ImageEnhance.Brightness(img).enhance((brightness_val/50))
    pho = ImageTk.PhotoImage(modified_img)
    e1.image = pho
    e1['image'] = pho
    img = img.resize((400, 450))
    b = 0


def change_rgb(var):
    global img, modified_img, contrast_val, brightness_val, rgb_val, b, o, r, backup, img_no
    b = 1
    o = 1
    if r == 1:
        img = ImageEnhance.Brightness(backup).enhance((brightness_val/50))
        img = ImageEnhance.Contrast(img).enhance((contrast_val * 0.04) - 1)
    rgb_val = int(var)
    modified_img = ImageEnhance.Color(img).enhance((rgb_val * 0.04) - 1)
    pho = ImageTk.PhotoImage(modified_img)
    e1.image = pho
    e1['image'] = pho
    img = img.resize((400, 450))
    r = 0


def save_img():

    global img, backup
    img = ImageEnhance.Brightness(backup).enhance((brightness_val/50))
    img = ImageEnhance.Contrast(img).enhance((contrast_val * 0.04) - 1)
    img = ImageEnhance.Color(img).enhance((rgb_val * 0.04) - 1)

    if img.mode == "RGBA":
        img = img.convert('RGB')

    img = img.resize((400, 450))
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    img.save(filename)


def reset_img():
    global img, backup
    img = backup
    pho = ImageTk.PhotoImage(img)
    e1.image = pho
    e1['image'] = pho
    contrast_slider.set(50)
    brightness_slider.set(50)
    rgb_slider.set(50)

def sel(var):
    global img_no
    img_no = var

contrast_slider = Scale(from_=0, to=100, orient=HORIZONTAL, bg="#E6FFFF", length=250, width=12, command=change_contrast)
contrast_slider.place(x=15,y=570)

brightness_slider = Scale(from_=0, to=100, orient=HORIZONTAL, bg="#E6FFFF", length=250, width=12, command=change_brightness)
brightness_slider.place(x=285, y=570)

rgb_slider = Scale(from_=0, to=100, orient=HORIZONTAL, bg="#E6FFFF", length=250, width=12, command=change_rgb)
rgb_slider.place(x=555, y=570)

b9 = tk.Button(my_w,  text='Save file', width=20, bg='#F9D7B3', command=lambda: save_img())
b9.place(x=880, y=570)

b10 = tk.Button(my_w,  text='Reset', width=20, bg='#F9D7B3', command=lambda: reset_img())
b10.place(x=1040, y=570)

r1 = tk.Radiobutton(my_w, text='', value=1, command=sel)


r2 = tk.Radiobutton(my_w, text='', value=2, command=sel)


r3 = tk.Radiobutton(my_w, text='', value=3, command=sel)


my_w.mainloop()
