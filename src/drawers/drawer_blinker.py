

from PIL import Image, ImageDraw, ImageOps
from PIL import Image

        
class Drawer_ShrinkingImage:

    def __init__(self, comp, parameters):
        self.__parms = parameters
        self.__comp = comp
        
    def renderImage(self, x_size, y_size, state):
        background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
        
        state_index = 0 if "state_index" not in self.__parms else self.__parms["state_index"]
        min_i = 0 if "min_i" not in self.__parms else self.__parms["min_i"]
        max_i = 0 if "max_i" not in self.__parms else self.__parms["max_i"]
        second_mod = 0 if "second_mod" not in self.__parms else self.__parms["second_mod"]
        second_offset = 0 if "second_offset" not in self.__parms else self.__parms["second_offset"]
        reverse = False if "reverse" not in self.__parms else self.__parms["reverse"]
        mySlice = state.slices[state_index]
        
        foreground = state.cache.getImage(self.__parms["image"], state.frame)
        
        if (second_offset + mySlice.second) % second_mod == 0 and min_i <= mySlice.frame and mySlice.frame <= max_i:
            foreground = foreground.resize( (background.size[0], int(background.size[1] / 4)), Image.ANTIALIAS)
            if reverse: foreground = ImageOps.mirror(foreground)
            background.paste(foreground, (0, int((background.size[1] / 8) * 3)))
            return background
        else:
            foreground = foreground.resize(background.size, Image.ANTIALIAS)
            if reverse: foreground = ImageOps.mirror(foreground)
            return Image.alpha_composite(background, foreground)
        
        
def create1(comp, parameters):
    return Drawer_ShrinkingImage(comp, parameters).renderImage

def name(): return "blinker"
def provider(): return create1



