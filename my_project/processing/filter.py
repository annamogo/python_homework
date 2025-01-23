import numpy as np
import math
from math import cos, sin, pi, sqrt


class Filter(object):
    def __init__(self):
        pass
    def processing(self):
        pass


class Equalization(Filter):
    def __init__(self, hist):
        self.hist = hist

    def processing(self, img):
        hist_temp = {i: 255*sum([item[1] for item in self.hist.items() if item[0]<=i]) for i in self.hist.keys()}  
        res_img = np.array([[hist_temp[i] for i in img_row] for img_row in img],dtype=img.dtype).reshape(img.shape)

        return res_img

class StatCorrection(Filter):
    def __init__(self, hist):
        self.hist = hist

    def processing(self, img):
        av1 = np.array([key*value for key, value in self.hist.items()]).sum()
        std1 = sqrt(np.array([ value * (key - av1)**2 for key, value in self.hist.items()]).sum())

        av2 = img.mean()
        std2 = img.std()
        res_img = std1 * (img - av2) / std2 + av1

        return res_img

class AddGaussNoize(Filter):
    def __init__(self, coeff):
        self.coeff = coeff

    def processing(self, img):
        res_img = np.clip(img + self.coeff*np.random.normal(0,1,img.shape),0,255).astype(img.dtype)

        return res_img

class GaussFilter(Filter):
    def __init__(self, sigma):
        self.sigma = sigma**2
        self.r = max(1,round(3*sigma))
        self.dim = 2*self.r + 1
        self.kernel = np.ones((self.dim,self.dim))

    def set_kernel(self):
        k_list = [i**2+j**2 for i in range(-self.r,self.r+1) for j in range(-self.r,self.r+1)]
        self.kernel = np.array(list(map(lambda x: 1/2/self.sigma/math.pi*math.exp(-x/2/self.sigma), k_list))).reshape(self.dim,self.dim)
        

        return self.kernel

    def processing(self,img):
        self.set_kernel()

        res_img = img
        for i in range(self.r,img.shape[0]-self.r):
            for j in range(self.r,img.shape[1]-self.r):
                res_img[i][j] = np.sum(img[i-self.r:i+self.r+1,j-self.r:j+self.r+1]*self.kernel).clip(0,255).astype(np.int32)

        return res_img

class Translate(Filter):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def processing(self, img):
        res_img = np.zeros(img.shape)
        res_img[0:-self.y,0:-self.x] = img[self.y:,self.x:]
        res_img[-self.y:,-self.x:] = img[0:self.y,0:self.x]
        res_img[-self.y:,0:-self.x] = img[0:self.y,self.x:]
        res_img[0:-self.y,-self.x:] = img[self.y:,0:self.x]

        return res_img

class Rotate(Filter):
    def __init__(self,angle):
        self.angle = pi*angle/180
        self.R = np.array([[cos(self.angle), -sin(self.angle)],
                           [sin(self.angle), cos(self.angle)]])
        self.h = 0
        self.w = 0

    def processing(self,img):
        x0 = img.shape[1]//2
        y0 = img.shape[0]//2

        res_img = np.zeros((int(2*abs(y0*cos(self.angle)+x0*sin(self.angle)))+1,
                            int(2*abs(x0*cos(self.angle)+y0*sin(self.angle)))+1))
        nx0 = res_img.shape[1]//2
        ny0 = res_img.shape[0]//2

        print(img.shape, res_img.shape)

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                nc = self.R.dot(np.array([x,y]) - np.array([x0,y0])) + np.array([nx0,ny0])
                res_img[int(nc[1])][int(nc[0])] = img[y][x]

        return res_img
        
class Glass(Filter):
    def __init__(self):
        pass

    def processing(self,img):
        res_img = np.zeros(img.shape)

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                try:
                    res_img[y][x] = img[y+int((np.random.randint(2)-0.5)*10)][x+int((np.random.randint(2)-0.5)*10)]
                except:
                    pass

        return res_img


class Waves(Filter):
    def __init__(self):
        pass

    def processing(self,img):
        res_img = np.zeros(img.shape)

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                try:
                    res_img[y][x] = img[y][x+int(20*sin(2*pi*x/60))]
                except:
                    pass

        return res_img

class MotionBlur(Filter):
    def __init__(self):
        self.K = np.diag(np.ones(5)*1/5)

    def processing(self,img):
        res_img = img

        for x in range(img.shape[1]-5):
            for y in range(img.shape[0]-5):
                res_img[y][x] = np.sum(img[y:y+5,x:x+5]*self.K)

        return res_img    
        

class Outline(Filter):
    def __init__(self):
        self.thresh = 150

    def processing(self,img):
        Mx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        My = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])

        res_img = np.zeros(img.shape)

        for x in range(1,img.shape[1]-1):
            for y in range(1,img.shape[0]-1):
                gx = np.sum(img[y-1:y+2,x-1:x+2]*Mx)
                gy = np.sum(img[y-1:y+2,x-1:x+2]*My)

                res_img[y,x] = (sqrt(gx**2+gy**2)//self.thresh)*255

        res_img = np.clip(res_img,0,255).astype(img.dtype)

        return res_img


class ClusterKMean(Filter):
    def __init__(self, k):
        self.k = k

    def processing(self,img):
        kluster_centers = [i*(255//self.k) for i in range(self.k)]
        kluster_centers_old = [0]*self.k
        klusters = [[] for i in range(self.k)]

        while kluster_centers != kluster_centers_old:

            for x in range(img.shape[1]):
                for y in range(img.shape[0]):
                    distances = [abs(img[y,x] - center) for center in kluster_centers]
                    min_dist = min(distances)

                    kluster_i = distances.index(min_dist)

                    klusters[kluster_i].append(img[y,x])

            kluster_centers_old = kluster_centers
            kluster_centers = [sum([i/len(kluster) for i in kluster]) if len(kluster)!=0 else 0 for kluster in klusters]
            klusters = [[] for i in range(self.k)]


        res_img = img

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                distances = [abs(img[y,x] - center) for center in kluster_centers]
                min_dist = min(distances)
                
                res_img[y,x] = kluster_centers[distances.index(min_dist)]

        return res_img

        
    
        

