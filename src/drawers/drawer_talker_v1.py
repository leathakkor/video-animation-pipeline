

from PIL import Image, ImageDraw, ImageOps
from PIL import Image

        

class Drawer_TalkingV1Image:

    def __init__(self, comp, parameters):
        self.__parms = parameters
        self.__comp = comp
        
    def renderImage(self, x_size, y_size, state):
        
        state_index = 0 if "state_index" not in self.__parms else self.__parms["state_index"]
        min_size = 30 if "min_size" not in self.__parms else self.__parms["min_size"]
        
        # ~ max_i = 0 if "max_i" not in self.__parms else self.__parms["max_i"]
        # ~ second_mod = 0 if "second_mod" not in self.__parms else self.__parms["second_mod"]
        # ~ second_offset = 0 if "second_offset" not in self.__parms else self.__parms["second_offset"]
        # ~ reverse = False if "reverse" not in self.__parms else self.__parms["reverse"]
        
        mySlice = state.slices[state_index]
        background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
        foreground = state.cache.getImage(self.__parms["image"], state.frame)
        foreground = foreground.resize(background.size, Image.ANTIALIAS)
        new_h = ( (background.size[1] - min_size) * mySlice.this[mySlice.frame]) / mySlice.max
        new_h += min_size
        foreground = foreground.resize((int(background.size[0]), int(new_h)))
        return foreground
        
def create1(comp, parameters):
    return Drawer_TalkingV1Image(comp, parameters).renderImage

def name(): return "talker_v1"
def provider(): return create1



