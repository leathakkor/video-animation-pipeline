

from PIL import Image, ImageDraw, ImageOps
from PIL import Image



class Drawer_None:

    def __init__(self, comp, parameters):
        self.__parms = parameters
        self.__comp = comp
    
    def renderImage(self, x_size, y_size, state):
        return Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
        
        
def create1(comp, parameters):
    return Drawer_None(comp, parameters).renderImage

def name(): return "none"
def provider(): return create1



