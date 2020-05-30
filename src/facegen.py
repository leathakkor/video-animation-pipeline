

from PIL import Image, ImageDraw, ImageOps
from PIL import Image

class Composer:
    
    def __init__(self, x, y, offset_x = 0, offset_y = 0):
        self.size = (x,y)
        self.offset = (offset_x,offset_y)
        self.parts = []
        self.generator = self.__generate
    
    def __generate(self, x, y, state):
        return Image.new('RGBA', (int(x), int(y)), (0, 0, 0, 0))
        
    
    def addPart(self, x, y, offset_x, offset_y):
        part = Composer(x, y, offset_x, offset_y)
        self.parts.append(part)
        return part
        
        
    def addSplitPartBySize(self, percent, isVertSplit=False):
        
        if isVertSplit:
            xl_size = self.size[0] * percent
            xr_size = self.size[0] - xl_size
            y_size = self.size[1]
            xl_start = 0
            y_start = 0
            self.parts = [
                           Composer(xl_size, y_size, xl_start, y_start),
                           Composer(xr_size, y_size, xl_size, 0)
                         ]
        else:
            yt_size = self.size[1] * percent
            yb_size = self.size[1] - yt_size
            x_size = self.size[0]
            yt_start = 0
            x_start = 0
            self.parts = [
                           Composer(x_size, yt_size, x_start, yt_start),
                           Composer(x_size, yb_size, x_start, yt_size)
                         ]
        return self.parts


def generateImage(x_size, y_size, state):
    img = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    shape = [0, 0, x_size, y_size]
    shape_r = [0, y_size, x_size, 0]
    
    modder = len(state.data["colors"])
    color = state.data["colors"][state.data["value"] % modder]
    
    # ~ draw.rectangle(shape, fill=color)
    draw.line(shape, fill=color)
    draw.line(shape_r, fill=color)
    state.data["value"] = (state.data["value"] + 1)
    
    return img

    
def renderPart(x_size, y_size, part, state):
    img = part.generator(x_size, y_size, state)
    for cp in part.parts:
        imageObj = renderPart(cp.size[0], cp.size[1], cp, state)
        img.paste(imageObj, (int(cp.offset[0]), int(cp.offset[1])), imageObj)
    return img
    
    
def renderImage(left, right, composer, state):
    img = composer.generator(composer.size[0], composer.size[1], state)
    for part in composer.parts:
        imageObj = renderPart(part.size[0], part.size[1], part, state)
        img.paste(imageObj, (int(part.offset[0]), int(part.offset[1])), imageObj)
    return img;


# https://www.hiclipart.com/free-transparent-background-png-clipart-dpzwh
def generateScottFace(x_size, y_size, state):
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/scott-face.png").convert("RGBA")
    foreground = foreground.resize(background.size, Image.ANTIALIAS)
    return Image.alpha_composite(background, foreground)
    # ~ img = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    # ~ draw = ImageDraw.Draw(img)
    # ~ shape = [0, 0, x_size, y_size]
    
    # ~ color = state.data["colors"][2]
    
    # ~ draw.ellipse(shape, fill=color)
    # ~ #state.data["value"] = (state.data["value"] + 1)
    
    # ~ return img


# https://www.hiclipart.com/free-transparent-background-png-clipart-dpzwh
def generateDawnFace(x_size, y_size, state):
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/dawn-face.png").convert("RGBA")
    foreground = foreground.resize(background.size, Image.ANTIALIAS)
    return Image.alpha_composite(background, foreground)
    
    # ~ img = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    # ~ draw = ImageDraw.Draw(img)
    # ~ shape = [0, 0, x_size, y_size]
    
    # ~ #modder = len(state["colors"])
    # ~ color = state.data["colors"][3]
    
    # ~ draw.ellipse(shape, fill=color)
    # ~ #state.data["value"] = (state.data["value"] + 1)
    
    # ~ return img    
    
def generatebackground(x_size, y_size, state):
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/virus.png").convert("RGBA")
    foreground = foreground.resize(background.size, Image.ANTIALIAS)
    return Image.alpha_composite(background, foreground)

    return img    
    
def generateScottEyes(x_size, y_size, state):
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/eyes.png")
    #foreground = foreground.resize(background.size, Image.ANTIALIAS)
    
    mySlice = state.slices[1]
    #return Image.alpha_composite(background, foreground)
    
    if mySlice.second % 13 == 0 and 14 <= mySlice.i and mySlice.i <= 18:
        foreground = foreground.resize( (background.size[0], int(background.size[1] / 4)), Image.ANTIALIAS)
        background.paste(foreground, (0, int((background.size[1] / 8) * 3)))
        return background
    else:
        foreground = foreground.resize(background.size, Image.ANTIALIAS)
        return Image.alpha_composite(background, foreground)


def generateScottMouth(x_size, y_size, state):
    mySlice = state.slices[1]
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/mouth.png").convert("RGBA")
    foreground = foreground.resize(background.size, Image.ANTIALIAS)
    new_h = ( (background.size[1] - 30) * mySlice.this[mySlice.i]) / mySlice.max
    #if new_h < 10: new_h = 10
    new_h += 30
    #print (new_h)
    foreground = foreground.resize((int(background.size[0]), int(new_h)))
    #state.hashes.append( ("scott.mouth.new_h", int(new_h)) )
    return foreground


    
def generateDawnEyes(x_size, y_size, state):
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/eyes.png")
    
    mySlice = state.slices[2]
    if mySlice.second % 11 == 0 and mySlice.i <= 4:
        foreground = ImageOps.mirror(foreground.resize( (background.size[0], int(background.size[1] / 4)), Image.ANTIALIAS))
        background.paste(foreground, (0, int((background.size[1] / 8) * 3)))
        return background
    else:
        foreground = ImageOps.mirror(foreground.resize(background.size, Image.ANTIALIAS))
        return Image.alpha_composite(background, foreground)
        
    


def generateDawnMouth(x_size, y_size, state):
    mySlice = state.slices[2]
    background = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    foreground = Image.open("parts/mouth.png").convert("RGBA")
    foreground = foreground.resize(background.size, Image.ANTIALIAS)
    # ~ new_h = (background.size[1] * mySlice.this[mySlice.i]) / mySlice.max
    # ~ if new_h < 10: new_h = 10
    new_h = ( (background.size[1] - 30) * mySlice.this[mySlice.i]) / mySlice.max
    new_h += 30
    #print (new_h)
    foreground = foreground.resize((int(background.size[0]), int(new_h)))
    #state.hashes.append( ("dawn.mouth.new_h", int(new_h)) )
    return foreground


def render(state):
    
    comp = Composer(1280, 720)
    parts = comp.addSplitPartBySize(.5, True)
    comp.generator = generatebackground
    
    scottPart = parts[0]
    
    scottFacePart = scottPart.addPart(scottPart.size[0] - 200, scottPart.size[1] - 200, 100, 100)
    scottFacePart.generator = generateScottFace
    scottEyes = scottPart.addPart(375, 200, (scottPart.size[0] - 375) / 2, 230)
    # ~ scottEyes = scottPart.addPart(375, 200, (scottPart.size[0] - 375) / 2, 160)
    scottMouth = scottPart.addPart(200, 150, (scottPart.size[0] - 200) / 2, 500)
    # ~ scottMouth = scottPart.addPart(375, 150, (scottPart.size[0] - 375) / 2, 400)
    scottEyes.generator = generateScottEyes
    scottMouth.generator = generateScottMouth
    
    
    dawnPart = parts[1]
    dawnPart.generator = generateDawnFace
    dawnEyes = dawnPart.addPart(300, 150, (scottPart.size[0] - 300) / 2, 200)
    dawnMouth = dawnPart.addPart(300, 250, (scottPart.size[0] - 300) / 2, 500)
    dawnEyes.generator = generateDawnEyes
    dawnMouth.generator = generateDawnMouth
    
    state.data["value"] = 0
    state.data["colors"] = [
                               (255, 0, 0, 255),
                               (0, 255, 0, 255),
                               (0, 0, 255, 255),
                               
                               (255, 255, 0, 255),
                               (255, 0, 255, 255),
                               (0, 255, 255, 255),
                               
                               (255, 255, 255, 255)
                             ]
    
    
    rez = renderImage(None, None, comp, state)
    return rez
    
