

from PIL import Image, ImageDraw, ImageOps
from PIL import Image


class Drawer_Image_Cycle:

    def __init__(self, comp, parameters):
        self.__parms = parameters
        self.__comp = comp
    
    
        
    def renderImage(self, x_size, y_size, state):
        
        state_index = 0 if "state_index" not in self.__parms else self.__parms["state_index"]
        #mySlice = state.slices[state_index]
        #print(len(self.__parms["images"]))
        parts = int(24 / len(self.__parms["images"]))
        img = self.__parms["images"][int(state.frame / parts)]
        background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
        foreground = state.cache.getImage(img, state.frame)
        foreground = foreground.resize(background.size, Image.ANTIALIAS)
        return Image.alpha_composite(background, foreground)
            

def create1(comp, parameters):
    return Drawer_Image_Cycle(comp, parameters).renderImage

def name(): return "image_cycle"
def provider(): return create1



