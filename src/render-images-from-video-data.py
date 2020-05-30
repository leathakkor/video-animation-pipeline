
# apps/audiowaveform -i /vms/tyoung/podcast/splits/s4q2e08/01-s4q2e08.ogg -o data/42-04-01.json  --pixels-per-second 24


import json, uuid
#from facegen import Composer, render
from imagegen import render
import numpy as np
import glob
import os, os.path, subprocess
import cv2
from PIL import Image
import threading
import sys
#from StringIO import StringIO
from io import BytesIO


#from importlib import import_module
import importlib, importlib.util

class Cache:
    def __init__(self):
        self.__images = [None] * 24
        for v in range(24): self.__images[v] = {}
    
    def getImage(self, name, i):
        thread_cache = self.__images[i]
        if name not in thread_cache:
            with open(name, 'rb') as fin:
                data = BytesIO(fin.read())
                data.flush()
                thread_cache[name] = data
                print ( ("preloading: ", i, name))
        
        stream = thread_cache[name]
        stream.seek(0)
        return Image.open(stream).convert("RGBA")
        

def convertData(items):
    rez = []
    rez_i = 0
    while True:
        rez_in = []
        for i in range(rez_i * 48, (rez_i + 1) * 48, 2):
            if (len(items) <= i):
                while len(rez_in) <24:
                    rez_in.append(0)
                rez.append(rez_in)
                return rez;
            rez_in.append(abs(items[i]))
        rez.append(rez_in)
        rez_i += 1
    

class SoundSlice:
    def __init__(self, prev, this, next, second, frame, max):
        self.prev = prev;
        self.this = this;
        self.next = next;
        self.frame = frame;
        self.second = second;
        self.max = max;

class State:
    def __init__(self, slices, cache, second, frame):
        self.slices = slices;
        self.data = {};
        self.hashes = [];
        self.cache = cache
        self.second = second
        self.frame = frame
        
def getItem(arr, i, offset):
    if (i + offset) < 0:
        return [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if (i + offset) >= len(arr):
        return [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return arr[i + offset]
    
def renderHolding(workingDir, wav_forms, i, x, videoConfig, frames, draw_lookup, cache):
    
    state_data = []
    
    for wav_form in wav_forms:
        introItems = wav_form["data"]
        maxIntro = wav_form["max_amplitude"]
        introSlice = SoundSlice(getItem(introItems, i, -1), getItem(introItems, i, 0), getItem(introItems, i, 1), i, x, maxIntro)
        state_data.append(introSlice)
        
    img = render(State(state_data, cache, i, x), videoConfig, draw_lookup)
    # ~ img.save(os.path.join(workingDir, "holding" + str(x) + ".png"), 'PNG')
    #print ("Saving: ", x)
    img.save(frames[x], "PNG")

def generateWaveForm(track_name, dirlook, workingDir, file):
    #onlyfiles = [f for f in os.listdir(dirlook) if os.path.isfile( os.path.join(dirlook, f) )]
    
    intro = file #next(f for f in onlyfiles if "intro" in f.lower() and f.endswith(".ogg"))
    
    introOut = os.path.join(workingDir, track_name + ".json")
    introIn = os.path.join(dirlook, intro)
    
    print (track_name, ":", intro, introOut)
    
    args = ["apps/audiowaveform", "-i", introIn, "-o", introOut, "--pixels-per-second", "24" ]
    subprocess.call(args)
    
    introdata = {}
    with open(introOut) as f:
      introData = json.load(f)
    introItems = convertData(introData["data"])
    maxIntro = 0
    
    for x in introItems:
        for y in x:
            if y > maxIntro:
                maxIntro = y
    
    return {
               "name": track_name,
               "max_amplitude": maxIntro,
               "data" : introItems,
               "data_length" : len(introItems),
               "wav_form_name": introOut,
               "track_path": introIn
           }
                
def get_opencv_img_from_buffer(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1) # , cv2.IMREAD_UNCHANGED
    return img

def generateVideo(wav_forms, workingDir, video_name, videoConfig):
    onlyfiles = [f for f in os.listdir(dirlook) if os.path.isfile( os.path.join(dirlook, f) )]
    
    maxLen = max(wav_forms, key = lambda x: x["data_length"])["data_length"]
    
    for wav_form in wav_forms:
        print(wav_form["name"], ":", wav_form["max_amplitude"], wav_form["data_length"])
    print ("max-len:", maxLen)
    
    cache = Cache();
    
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    video = cv2.VideoWriter(video_name, fourcc, 24, (1280, 720))  
    
    includes = [f for f in os.listdir('drawers') if f.endswith(".py")]
    drawers = {}
    #os.listdir("drawer");
    for include in includes:
        spec = importlib.util.spec_from_file_location("module.name", os.path.join("drawers", include))
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        drawers[foo.name()] = foo.provider()
        
    
    threads = []
    frames = [None] * 24
    for ii in range(24): frames[ii] = BytesIO()
    for x in range(24):
        t1 = threading.Thread(target=renderHolding, args=(workingDir, wav_forms, 0, x, videoConfig, frames, drawers, cache))
        threads.append(t1)
    
    [t.start() for t in threads]
    [t.join() for t in threads]
    
    for t4 in range(24):
        imgcv = get_opencv_img_from_buffer(frames[t4])
        video.write(imgcv)
        
    print ("")
    
    for i in range(1, int((maxLen - 1))):
        print(i),
        threads = []
        frames = [None] * 24
        for ii in range(24): frames[ii] = BytesIO()
        for x in range(24):
            t1 = threading.Thread(target=renderHolding, args=(workingDir, wav_forms, i, x, videoConfig, frames, drawers, cache))
            threads.append(t1)
            
        [t.start() for t in threads]
        [t.join() for t in threads]
        
        for t4 in range(24):
            imgcv = get_opencv_img_from_buffer(frames[t4])
            video.write(imgcv)
        print("")
    
    threads = []
    frames = [None] * 24
    for ii in range(24): frames[ii] = BytesIO()
    for x in range(24):
        t1 = threading.Thread(target=renderHolding, args=(workingDir, wav_forms, maxLen - 1, x, videoConfig, frames, drawers, cache))
        threads.append(t1)
    
    [t.start() for t in threads]
    [t.join() for t in threads]
    
    for t4 in range(24):
        imgcv = get_opencv_img_from_buffer(frames[t4])
        video.write(imgcv)
    
    print("")
    cv2.destroyAllWindows()  
    video.release()

def generateAudioVideo(dirlook, workingDir, wav_forms, video_name, outputPath):
    
    onlyfiles = [f for f in os.listdir(dirlook) if os.path.isfile( os.path.join(dirlook, f) )]
    
    
    # ffmpeg -i input0.mp3 -i input1.mp3 -filter_complex amix=inputs=2:duration=longest output.mp3
    args = ["ffmpeg"]
    for wav_form in wav_forms:
        args.append("-i")
        args.append(wav_form["track_path"])
    
    args.append("-filter_complex")
    args.append("amix=inputs=" + str(len(wav_forms)) + ":duration=longest")
    args.append(os.path.join(workingDir, "dual-with-intro.mp3"))
            
    subprocess.call(args)
    # ~ args = [
            # ~ "lame", 
            # ~ "--scale", "3", 
            # ~ os.path.join(workingDir, "dual-with-intro.mp3"),
            # ~ os.path.join(workingDir, "dual-with-intro-loud.mp3")
            # ~ ]
            
    #subprocess.call(args)
    #  Because.mp3 Because_loud.mp3
    args = [
            "ffmpeg", 
            "-i", video_name, 
            "-i", os.path.join(workingDir, "dual-with-intro.mp3"),
            "-c",
            "copy",
            "-map",
            "0:v:0",
            "-map", 
            "1:a:0",
            outputPath
            ]
            
    subprocess.call(args)
    


#print 'Number of arguments:', len(sys.argv), 'arguments.'
configPath = sys.argv[1];
dirlook = os.path.split(configPath)[0];

print('Processing: ', configPath)
print('Path: ', dirlook)

config = {}
with open(configPath) as f:
    config = json.load(f)
    #print(d)

#id = uuid.uuid4().hex


working = os.path.join(dirlook, "working")
if not os.path.exists(working):
    os.makedirs(working)

wav_forms = []
for track in config["tracks"]:
    name = track["name"]
    print(track["name"])
    wav_forms.append(generateWaveForm(name, dirlook, working, name))


generateVideo(wav_forms, working, os.path.join(working, "no-sound.avi"), config["rendering"])
generateAudioVideo(dirlook, working, wav_forms, os.path.join(working, "no-sound.avi"), os.path.join(dirlook, config["videoOutputName"]))


#
exit()

  





