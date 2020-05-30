

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
        
        
def renderPart(x_size, y_size, part, state):
    img = part.generator(x_size, y_size, state)
    for cp in part.parts:
        imageObj = renderPart(cp.size[0], cp.size[1], cp, state)
        img.paste(imageObj, (int(cp.offset[0]), int(cp.offset[1])), imageObj)
    return img

def drawerWrapper(draw_lookup, comp, name, parameters):
    
    if name.lower() in draw_lookup:
        return draw_lookup[name.lower()](comp, parameters)
    
    raise "Error";
    # ~ return Drawer_None(comp, parameters).renderImage



def findPartByAnchorLeft(cParent, anchorParms):
    percent = anchorParms["percent"] / 100.0
    xl_size = cParent.size[0] * percent
    xr_size = cParent.size[0] - xl_size
    y_size = cParent.size[1]
    xl_start = 0
    y_start = 0
    return ( (xl_size, y_size), (xl_start, y_start) )
    
def findPartByAnchorRight(cParent, anchorParms):
    percent = anchorParms["percent"] / 100.0
    xl_size = cParent.size[0] * percent
    xr_size = cParent.size[0] - xl_size
    y_size = cParent.size[1]
    xl_start = 0
    y_start = 0
    return ( (xr_size, y_size), (xl_size, 0) )


def findPartByAnchorTop(cParent, anchorParms):
    percent = anchorParms["percent"] / 100.0
    yt_size = cParent.size[1] * percent
    yb_size = cParent.size[1] - yt_size
    x_size = cParent.size[0]
    yt_start = 0
    x_start = 0
    
    return ( (x_size, yt_size), (x_start, yt_start) )
    
def findPartByAnchorBottom(cParent, anchorParms):
    percent = anchorParms["percent"] / 100.0
    yt_size = cParent.size[1] * percent
    yb_size = cParent.size[1] - yt_size
    x_size = cParent.size[0]
    yt_start = 0
    x_start = 0
    return ( (x_size, yb_size), (x_start, yt_size) )


def findPartByAnchorFill(size, offset, parms):
    
    marginTop = 0 if "margin-top-px" not in parms else parms["margin-top-px"]
    marginBottom = 0 if "margin-bottom-px" not in parms else parms["margin-bottom-px"]
    marginLeft = 0 if "margin-left-px" not in parms else parms["margin-left-px"]
    marginRight = 0 if "margin-right-px" not in parms else parms["margin-right-px"]
    
    x_size = size[0] - (marginRight + marginLeft)
    y_size = size[1] - (marginTop + marginBottom)
    
    x_size = x_size if "width" not in parms else parms["width"]
    y_size = y_size if "height" not in parms else parms["height"]
    
    if ("center-horizontal" in parms and parms["center-horizontal"] == True):
        marginLeft = (size[0] - x_size) / 2
    
    if ("center-vertical" in parms and parms["center-vertical"] == True):
        marginTop = (size[1] - y_size) / 2
    #print (size)
    return ((x_size, y_size), (marginLeft, marginTop))

def findPartByAnchor(cParent, anchorType, anchorParms):
    #print(anchorType)
    if anchorType.lower() == "fill":
        return findPartByAnchorFill(cParent.size, cParent.offset, anchorParms)
    if anchorType.lower() == "left":
        return findPartByAnchorLeft(cParent, anchorParms)
    if anchorType.lower() == "right":
        return findPartByAnchorRight(cParent, anchorParms)
        
    if anchorType.lower() == "top":
        return findPartByAnchorTop(cParent, anchorParms)
    if anchorType.lower() == "bottom":
        return findPartByAnchorBottom(cParent, anchorParms)
        
    


def appendChildren(draw_lookup, c, parentLayer):
    
    if ("layers" not in parentLayer):
        return;
    
    ls = parentLayer["layers"]
    
    if (ls == None):
        return;
    
    #print(len(ls))
    for l in ls:
        dim = findPartByAnchor(c, l["anchor"], l["anchor_parameters"])
        #print( dim )
        comp = c.addPart(dim[0][0], dim[0][1], dim[1][0], dim[1][1])
        # ~ layer = renderingData["layer"]
        comp.generator = drawerWrapper(draw_lookup, comp, l["drawer"], l["drawer_parameters"])
        appendChildren(draw_lookup, comp, l)
        
            

def render(state, renderingData, draw_lookup):
    
    comp = Composer(renderingData["width"], renderingData["height"])
    
    # ~ layers = renderingData["layers"]
    comp.generator = drawerWrapper(draw_lookup, comp, "none", {})
    
    # ~ for layer in layers:
    appendChildren(draw_lookup, comp, renderingData)
    rez = renderPart(renderingData["width"], renderingData["height"], comp, state)
    
    return rez
    
    
