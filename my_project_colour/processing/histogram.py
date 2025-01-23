import numpy as np

class Hist(object):
    def __init__(self, img):
        self.img = img

    def get_hist(self):
        num = self.img.shape[0] * self.img.shape[1]
        hist = {i:(self.img==i).sum() / num for i in range(0,256)}

        return hist
