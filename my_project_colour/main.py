import cv2
import tkinter
from tkinter import *
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.simpledialog import askfloat, askinteger
from processing.filter import *
from processing.img_class import Img, ImgBinary, ImgGray, ImgRGB
import numpy as np
from PIL import Image, ImageTk

img = Img()
def read_bin_image_menu():
   global img, image, label_image, photo, root, image_label
   name = askopenfilename(initialdir="./",
                          filetypes=(("JPG", "*.jpg"),("PNG", "*.png")),
                          title="Choose an image."
                          ) 

   img = ImgBinary()                     
   try:
      img.read(name)
   except:
      showerror(title="Error", message="cv2 could not read an image.")
   else:
      update_image()

def read_gray_image_menu():
   global img, image, label_image, photo, root, image_label
   name = askopenfilename(initialdir="./",
                          filetypes=(("JPG", "*.jpg"),("PNG", "*.png")),
                          title="Choose an image."
                          ) 

   img = ImgGray()
   try:
      img.read(name)
   except:
      showerror(title="Error", message="cv2 could not read an image.")
   else:
      update_image()

def read_RGB_image_menu():
   global img, image, label_image, photo, root, image_label
   name = askopenfilename(initialdir="./",
                          filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),
                          title="Choose an image."
                          ) 

   img = ImgRGB()                     
   try:
      img.read(name)
   except:
      showerror(title="Error", message="cv2 could not read an image.")
   else:
      update_image()

def save_image_menu():
   global img
   name = asksaveasfile(mode='w', filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),defaultextension=".png")
   img.write(name.name)


def nothing():
   pass


def stat_correction():
   global img

   name = askopenfilename(initialdir="./",
                          filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),
                          title="Choose a reference image for stat correction."
                          )
   hist_img = ImgGray()
   hist_img.read(name)
   hist = hist_img.get_hist()

   pr = Convert(img)
   try:
      img = pr.stat_correction(hist)
      update_image()
   except:
      showerror(title="Error", message="could not process data type.")
      

def stat_correction_3D():
   global img

   name = askopenfilename(initialdir="./",
                          filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),
                          title="Choose a reference image for stat correction."
                          )
   hist_img = ImgRGB()
   hist_img.read(name)
   hist = hist_img.get_hist()

   pr = Convert(img)
   try:
      img = pr.stat_correction_3D(hist)
      update_image()
   except:
      showerror(title="Error", message="could not process data type.")

def color_to_mono():
   global img

   pr = Convert(img)
   try:
      img = pr.color_to_mono()
      update_image()
   except:
      showerror(title="Error", message="could not process data type.")

def mono_to_color():
   global img

   pr = Convert(img)
   try:
      img = pr.mono_to_color()
      update_image()
   except:
      showerror(title="Error", message="could not process data type.")

def mono_to_bin():
   global img

   thresh = askinteger(title="input",
                       prompt="enter a value from 0 to 255")

   pr = Convert(img)
   try:
      img = pr.mono_to_bin(thresh)
      update_image()
   except:
      showerror(title="Error", message="could not process data type.")

def bin_to_mono():
   global img

   pr = Convert(img)
   try:
      img = pr.bin_to_mono(thresh)
      update_image()
   except:
      showerror(title="Error", message="could not process data type.")

  

   
### DO NOT TOUCH THIS ###
   
def add_image_to_gui():
   global root
   image_label = tkinter.Label(root)
   image_label.pack()
   return image_label


def update_image():
   global root, image_label, img
   image = Image.fromarray(img.img)
   tk_image = ImageTk.PhotoImage(image)
   image_label.configure(image=tk_image)
   image_label.image = tk_image
   root.after(100, update_image, root, image_label)

root = Tk()
root.geometry("750x450")
menubar = Menu(root)

image_label = add_image_to_gui()

# первый выпадающий список
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open binary image", command=read_bin_image_menu)
filemenu.add_command(label="Open gray image", command=read_gray_image_menu)
filemenu.add_command(label="Open RGB image", command=read_RGB_image_menu)
filemenu.add_command(label="Save", command=save_image_menu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
###

# второй выпадающий список
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Nothing", command=nothing)
editmenu.add_command(label="StatCorrection-1D", command=stat_correction)
editmenu.add_command(label="StatCorrection-3D", command=stat_correction_3D)
editmenu.add_command(label="Convert RGB to gray", command=color_to_mono)
editmenu.add_command(label="Convert gray to RGB", command=mono_to_color)
editmenu.add_command(label="Convert gray to binary", command=mono_to_bin)
editmenu.add_command(label="Convert binary to gray", command=bin_to_mono)
menubar.add_cascade(label="Convert", menu=editmenu)


root.config(menu=menubar)
root.mainloop()
