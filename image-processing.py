
from PIL import Image, ImageDraw
from PIL import Image

class Composer:
    
    def __init__(self, x, y, offset_x = 0, offset_y = 0):
        self.size = (x,y)
        self.offset = (offset_x,offset_y)
        self.parts = []
        self.generator = self.__generate
    
    def __generate(self, x, y, counter):
        return Image.new('RGBA', (int(x), int(y)), (0, 0, 0, 0))
        
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


def generateImage(x_size, y_size, counter):
    img = Image.new('RGBA', (int(x_size), int(y_size)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    shape = [0, 0, x_size, y_size]
    
    modder = len(counter["colors"])
    color = counter["colors"][counter["value"] % modder]
    
    draw.rectangle(shape, fill=color)
    counter["value"] = (counter["value"] + 1)
    
    return img

    
def renderPart(x_size, y_size, part, counter):
    img = part.generator(x_size, y_size, counter)
    for cp in part.parts:
        imageObj = renderPart(cp.size[0], cp.size[1], cp, counter)
        img.paste(imageObj, (int(cp.offset[0]), int(cp.offset[1])), imageObj)
    return img
    
    
def renderImage(left, right, composer, counter):
    img = composer.generator(composer.size[0], composer.size[1], counter)
    for part in composer.parts:
        imageObj = renderPart(part.size[0], part.size[1], part, counter)
        img.paste(imageObj, (int(part.offset[0]), int(part.offset[1])), imageObj)
    return img;


counter = {
  "value": 0,
  "colors": [
           (255, 0, 0, 255),
           (0, 255, 0, 255),
           (0, 0, 255, 255),
           
           (255, 255, 0, 255),
           (255, 0, 255, 255),
           (0, 255, 255, 255),
           
           (255, 255, 255, 255)
         ]
}

comp = Composer(1280, 720)
parts = comp.addSplitPartBySize(.5, True)

rez = renderImage(None, None, comp, counter)
rez.save('vert-split.png', 'png')

#############

comp = Composer(1280, 720)
parts = comp.addSplitPartBySize(.5, False)

rez = renderImage(None, None, comp, counter)
rez.save('horz-split.png', 'png')

##############


comp = Composer(1280, 720)
parts = comp.addSplitPartBySize(.5, False)
for part in parts:
    subparts = part.addSplitPartBySize(.5, True)

rez = renderImage(None, None, comp, counter)
rez.save('horz-sub-split.png', 'png')

#######################3

comp = Composer(1280, 720)
parts = comp.addSplitPartBySize(.5, False)
for part in parts:
    part.generator = generateImage
    subparts = part.addSplitPartBySize(.5, True)
    for cp in subparts:
        cp.generator = generateImage

rez = renderImage(None, None, comp, counter)
rez.save('horz-sub-split.png', 'png')



