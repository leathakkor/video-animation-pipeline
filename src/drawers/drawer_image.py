

from PIL import Image, ImageDraw, ImageOps
from PIL import Image


class Drawer_Image:

    def __init__(self, comp, parameters):
        self.__parms = parameters
        self.__comp = comp
    
    
        
    def renderImage(self, x_size, y_size, state):
        
        
        state_index = 0 if "state_index" not in self.__parms else self.__parms["state_index"]
        zoom_max_percent = 0 if "zoom-max-percent" not in self.__parms else self.__parms["zoom-max-percent"]
        zoom_smooting = 1 if "zoom-smoothing" not in self.__parms else self.__parms["zoom-smoothing"]
        
        if (zoom_max_percent == 0):
            background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
            foreground = state.cache.getImage(self.__parms["image"], state.frame)
            foreground = foreground.resize(background.size, Image.ANTIALIAS)
            return Image.alpha_composite(background, foreground)
        else:
            mySlice = state.slices[state_index]
            background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
            foreground = state.cache.getImage(self.__parms["image"], state.frame)
            foreground = foreground.resize(background.size, Image.ANTIALIAS)
            
            mySliceValue = mySlice.this[mySlice.frame]
            if zoom_smooting > 1:
                 #chunks = 24 / zoom_smooting
                 start_i = int (mySlice.frame / zoom_smooting)
                 mySliceValue = 0
                 for iii in range(start_i, start_i + zoom_smooting):
                     mySliceValue += mySlice.this[start_i]
                 mySliceValue = mySliceValue / zoom_smooting
                 
            old_width = background.size[0]
            old_height = background.size[1]
            ratio_expander = (zoom_max_percent + 100) /  100.0
            
            
            max_width = ratio_expander * old_width
            #new_w = ( (old_width + max_width) * mySliceValue) / mySlice.max
            new_w = (( max_width - old_width)  * mySliceValue) / mySlice.max
            new_w += old_width
            
            max_height = ratio_expander * old_height
            # ~ new_h = ( (old_height + max_height) * mySliceValue) / mySlice.max
            new_h = (( max_height - old_height)  * mySliceValue) / mySlice.max
            new_h += old_height
            
            
            
            foreground = foreground.resize((int(new_w), int(new_h)))
            left = (new_w - old_width) / 2
            top = (new_h - old_height) / 2
            right = (new_w + old_width) / 2
            bottom = (new_h + old_height) / 2
            
            foreground = foreground.crop((left, top, right, bottom))
            return foreground
            

def create1(comp, parameters):
    return Drawer_Image(comp, parameters).renderImage

def name(): return "image"
def provider(): return create1



