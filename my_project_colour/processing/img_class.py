import numpy as np
import cv2

class Img(object):
    def __init__(self):
        self.img = None

    def store(self, img):
        self.img = img

    def write(self, path):
        cv2.imwrite(path, self.img)

    def read(self, path):
        self.img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    def get_hist(self):
        pass

class ImgBinary(Img):
    def __init__(self):
        super(ImgBinary, self).__init__()
        self.thresh = 0

    def read(self, path):
        try:
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        except:
            raise Exception("Can't read this image.")
        else:
            thresh_val = 128
            max_val = 255
            self.thresh, self.img = cv2.threshold(img, thresh_val, max_val, cv2.THRESH_BINARY)



class ImgGray(Img):    
    def read(self, path):
        try:
            self.img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        except:
            raise Exception("Can't read this image.")

    def get_hist(self):
        num = self.img.shape[0] * self.img.shape[1]
        hist = {i:(self.img==i).sum() / num for i in range(0,256)}

        return hist



class ImgRGB(Img):
    def read(self, path):
        try:
            self.img = cv2.imread(path, cv2.IMREAD_COLOR)
            self.img = np.flip(self.img, axis=-1)
        except:
            raise Exception("Can't read this image.")


    def get_hist(self):
        num = self.img.shape[0] * self.img.shape[1]
        hist = [{i:(self.img[:,:,j]==i).sum()/num for i in range(0,256)} for j in range(3)]

        return hist

        
