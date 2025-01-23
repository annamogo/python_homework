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

    def mono_to_bin(self, thresh=128):
        img = self.img.img

        b = lambda x: 255 if x>thresh else 0
        res = np.array([[b(p) for p in row]for row in img]).astype(np.uint8)

        res_img = ImgBinary()
        res_img.store(res)

        return res_img

    def bin_to_mono(self):
        img = self.img.img

        res_x = np.zeros(img.shape)
        res = np.zeros(img.shape)
        
        for i in range(img.shape[0]):
            if img[i,0] == 0:
                res_x[i,0] = 0
            else:
                res_x[i,0] = img.shape[0] + img.shape[1]

            for j in range(1,img.shape[1]):
                if img[i,j] == 0:
                    res_x[i,j] = 0
                else:
                    res_x[i,j] = res_x[i,j-1]+1

            for j in reversed(range(img.shape[1]-1)):
                if res_x[i,j+1] < res_x[i,j]:
                    res_x[i,j] = 1 + res_x[i,j+1]

        print(res_x)
        norma = lambda x, y, z: (x-z)**2 + res_x[z,y]**2
        sep = lambda x, y, z: (z**2 - y**2 + res_x[z,x]**2 - res_x[y,x]**2)//(2*(z - y))
        
        #second part, colomns
        for j in range(img.shape[1]):
            q = 0
            s = [0]
            t = [0]
            for u in range(1,img.shape[0]):
                while (q>=0)and(norma(t[q],j,s[q])>norma(t[q],j,u)):
                    q = q-1
                    del s[-1]
                    del t[-1]
                if q<0:
                    q = 0
                    s.append(u)
                    t.append(0)
                else:
                    w = 1 + sep(j,s[q],u)
                    if w <= img.shape[0]:
                        q = q + 1
                        s.append(u)
                        t.append(w)

            for u in reversed(range(img.shape[0])):
                res[u,j] = norma(u,j,s[q])
                if u == t[q]:
                    q = q - 1

        print(np.array(t).astype(np.uint32))
        res = np.array(res)
        print(res)
        res_img = ImgGray()
        res_img.store((res/np.max(res)*255).astype(np.uint8))

        return res_img
                
            
        
    


        
    
        

