import cv2
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.simpledialog import askfloat, askinteger
from processing.processing_factory import ProcessingFactory as pf
from processing.complex_filter import ComplexFilter as cf
from processing.filter import *
from processing.histogram import Hist
import numpy as np
from PIL import Image, ImageTk

img = None
def read_image_menu():
   global img, image, label_image, photo, root, image_label
   name = askopenfilename(initialdir="./",
                          filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),
                          title="Choose an image."
                          )
   img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
   update_image()

def save_image_menu():
   global img
   name = asksaveasfile(mode='w', filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),defaultextension=".png")
   cv2.imwrite(name.name, img)

def help_info_menu():
   pass

def empty_filter_menu():
   global img, image
   filt = cf()
   proc = pf("EmptyFilter", filt)
   img = proc.process(img)
   update_image()
   

def equalization():
   global img

   name = askopenfilename(initialdir="./",
                          filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),
                          title="Choose a reference image for equalization."
                          )
   hist_img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
   hist = Hist(hist_img).get_hist()
   
   filt = cf()
   filt.add_filter(Equalization(hist))
   proc = pf("Equalize", filt)

   img = proc.process(img)
   update_image()

def stat_correction():
   global img

   name = askopenfilename(initialdir="./",
                          filetypes=(("PNG", "*.png"), ("JPG", "*.jpg")),
                          title="Choose a reference image for stat correction."
                          )
   hist_img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
   hist = Hist(hist_img).get_hist()
   
   filt = cf()
   filt.add_filter(StatCorrection(hist))
   proc = pf("StatCorrection", filt)

   img = proc.process(img)
   update_image()

def add_gauss_noize():
   global img

   coeff = askfloat(title="Input",
                    prompt="Enter noize coefficient.",
                    parent=root
                    )

   filt = cf()
   filt.add_filter(AddGaussNoize(coeff))
   proc = pf("AddGaussNoize", filt)

   img = proc.process(img)
   update_image()

def gauss_filter():
   global img

   sigma = askfloat(title="Input",
                    prompt="Enter sigma coefficient.",
                    parent=root
                    )

   filt = cf()
   filt.add_filter(GaussFilter(sigma))
   proc = pf("GaussFilter",filt)

   img = proc.process(img)
   update_image()

def translate():
   global img

   x = askinteger(title="Input",
                    prompt="Enter X offset in picsels.",
                    parent=root
                    )
   y = askinteger(title="Input",
                    prompt="Enter Y offset in picsels.",
                    parent=root
                    )

   filt = cf()
   filt.add_filter(Translate(x,y))
   proc = pf("Translate",filt)

   img = proc.process(img)
   update_image()

def rotate():
   global img

   angle = askfloat(title="Input",
                    prompt="Enter rotation angle (grad).",
                    parent=root
                    )
   
   filt = cf()
   filt.add_filter(Rotate(angle))
   proc = pf("Rotate",filt)

   img = proc.process(img)
   update_image()

def glass():
   global img
   filt = cf()
   filt.add_filter(Glass())
   proc = pf("Glass", filt)

   img = proc.process(img)
   update_image()

def waves():
   global img
   filt = cf()
   filt.add_filter(Waves())
   proc = pf("Waves", filt)

   img = proc.process(img)
   update_image()

def motion_blur():
   global img
   filt = cf()
   filt.add_filter(MotionBlur())
   proc = pf("MotionBlur", filt)

   img = proc.process(img)
   update_image()


def outline():
   global img
   filt = cf()
   filt.add_filter(Outline())
   proc = pf("Outline", filt)

   img = proc.process(img)
   update_image()

def kluster_k_mean():
   global img

   k = askinteger(title="Input",
                    prompt="Enter number of klusters.",
                    parent=root
                    )
   filt = cf()
   filt.add_filter(ClusterKMean(k))
   proc = pf("ClusterKMean", filt)

   img = proc.process(img)
   update_image()

   
### DO NOT TOUCH THIS ###
   
def add_image_to_gui():
   global root
   image_label = tkinter.Label(root)
   image_label.pack()
   return image_label


def update_image():
   global root, image_label, img
   image = Image.fromarray(img)
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
filemenu.add_command(label="Open", command=read_image_menu)
filemenu.add_command(label="Save", command=save_image_menu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
###

# второй выпадающий список
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="EmptyFilter", command=empty_filter_menu)
editmenu.add_command(label="Equalize", command=equalization)
editmenu.add_command(label="StatCorrection", command=stat_correction)
editmenu.add_command(label="AddGaussNoize", command=add_gauss_noize)
editmenu.add_command(label="GaussFilter", command=gauss_filter)
menubar.add_cascade(label="EditStatNoize", menu=editmenu)
###

# третий выпадающий список
editmenu2 = Menu(menubar, tearoff=0)
editmenu2.add_command(label="Outline", command=outline)
editmenu2.add_command(label="ClusterKmean", command=kluster_k_mean)
menubar.add_cascade(label="Additional Two Tasks", menu=editmenu2)
###

# четвертый выпадающий список
editmenu1 = Menu(menubar, tearoff=0)
editmenu1.add_command(label="Translate", command=translate)
editmenu1.add_command(label="Rotate", command=rotate)
editmenu1.add_command(label="Glass", command=glass)
editmenu1.add_command(label="Waves", command=waves)
editmenu1.add_command(label="MotionBlur", command=motion_blur)
menubar.add_cascade(label="EditGeometry", menu=editmenu1)
###

# пятый выпадающий список
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Info", command=help_info_menu)
menubar.add_cascade(label="Help", menu=helpmenu)
###

root.config(menu=menubar)
root.mainloop()
