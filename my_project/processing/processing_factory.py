from .complex_filter import ComplexFilter

class ProcessingFactory(object):
    def __init__(self,
                 name,
                 proc_steps: ComplexFilter):
        self.name = name
        self.proc_steps = proc_steps

    def process(self,
                img):

        img = self.proc_steps.processing(img)
        
        return img
