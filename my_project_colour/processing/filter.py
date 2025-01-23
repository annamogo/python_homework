import numpy as np
import math
from math import cos, sin, tan, atan, pi, sqrt
from .img_class import Img, ImgBinary, ImgGray, ImgRGB


class Convert(object):
    def __init__(self, img):
        self.img = img
    
    def stat_correction(self, hist, img = []):
        av1 = np.array([key*value for key, value in hist.items()]).sum()
        std1 = sqrt(np.array([ value * (key - av1)**2 for key, value in hist.items()]).sum())

        if np.any(img):
            av2 = img.mean()
            std2 = img.std()
            res = std1 * (img - av2) / std2 + av1
        else:
            av2 = self.img.img.mean()
            std2 = self.img.img.std()
            res = std1 * (self.img.img - av2) / std2 + av1

        res_img = ImgGray()  
        res_img.store(res.astype(np.int32))

        return res_img

    def stat_correction_3D(self, hist):
        img_R = self.img.img[:,:,0]
        img_G = self.img.img[:,:,1]
        img_B = self.img.img[:,:,2]

        res_img_R = self.stat_correction(hist[0],img_R)
        res_img_G = self.stat_correction(hist[1],img_G)
        res_img_B = self.stat_correction(hist[2],img_B)

        res = np.stack((res_img_R.img, res_img_G.img, res_img_B.img),axis=-1).astype(np.uint8)

        res_img = ImgRGB()
        res_img.store(res)

        return res_img

    def color_to_mono(self):
        res = self.img.img.sum(axis=-1)/3
        
        res_img = ImgGray()
        res_img.store(res.astype(np.int8))

        return res_img

    def mono_to_color(self):
        img = np.array(self.img.img)

        res_R = (np.arctan(20*img.astype(np.uint16)/255-10)/2/atan(10)+1/2)*255
        res_G = img
        res_B = (np.tan(3*img/255-1.5)/2/tan(1)+1/2)*255

        z = np.zeros(img.shape)
 

        res = np.stack((res_R, res_G, res_B),axis=-1).astype(np.uint8)

        res_img = ImgRGB()
        res_img.store(res)

        return res_img


     
        

        
    


        
    
        

