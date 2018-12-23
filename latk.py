'''
The Lightning Artist Toolkit was developed with support from:
   Canada Council on the Arts
   Eyebeam Art + Technology Center
   Ontario Arts Council
   Toronto Arts Council
   
Copyright (c) 2018 Nick Fox-Gieg
http://fox-gieg.com

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''

import math
from math import sqrt
#~
import json
import xml.etree.ElementTree as etree
import base64
#~
import re
import parameter_editor
import random
import sys
import gc
import struct
import uuid
import contextlib
from collections import defaultdict
from itertools import zip_longest
from operator import itemgetter
#~
import os
import zipfile
import io
from io import BytesIO
#~
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class Latk(object):     
    def __init__(self, fileName=None, latks=None, points=None, color=None): # args string, Latk array, float tuple array, float tuple           
        self.layers = [] # LatkLayer

        if (fileName==None and latks==None and points==None): # new empty Latk
            self.layers.append(LatkLayer())
            self.layers[0].frames.append(LatkFrame())
        elif (fileName==None and latks!=None and points==None): # merge Latk array
            pass # TODO read with clear existing false
        elif (fileName==None and latks==None and points!=None): # 
            self.layers.append(LatkLayer())
            self.layers[0].frames.append(LatkFrame())
            
            st = LatkStroke(_pts, _c)
            self.layers[0].frames[0].strokes.append(st)
        else: # load from url
            self.read(fileName, True)
    
        print("Latk strokes loaded.")
        
    def getFileNameNoExt(self, s): # args string, return string
        returns = ""
        temp = s.split(".")
        if (len(temp) > 1): 
            for i in range(0, len(temp)-1):
                if (i > 0):
                    returns += "."
                returns += temp[i]
        else:
            return s
        return returns
        
    def getExtFromFileName(self, s): # args string, returns string 
        returns = ""
        temp = s.split(".")
        returns = temp[len(temp)-1]
        return returns
        
    def read(self, fileName, clearExisting=True): # args string, bool
        data = None

        if (clearExisting == True):
            self.layers = []
        
        fileType = getExtFromFileName(fileName)
        if (fileType == "latk" or fileType == "zip"):
            imz = InMemoryZip()
            imz.readFromDisk(url)
            data = json.loads(imz.files[0].decode("utf-8"))        
        else:
            with open(fileName) as data_file:    
                data = json.load(data_file)
                            
        for (int h=0 h<json.getJSONArray("grease_pencil").size() h++) 
            jsonGp = json.getJSONArray("grease_pencil").get(h)
            
            for (int i=0 i<jsonGp.getJSONArray("layers").size() i++) 
                layers.append(new LatkLayer())
                
                jsonLayer = jsonGp.getJSONArray("layers").get(i)
                for (int j=0 j<jsonLayer.getJSONArray("frames").size() j++) 
                    layers.get(layers.size()-1).frames.append(new LatkFrame())

                    jsonFrame = jsonLayer.getJSONArray("frames").get(j)
                    for (int l=0 l<jsonFrame.getJSONArray("strokes").size() l++) 
                        jsonStroke = jsonFrame.getJSONArray("strokes").get(l)
                        
                        int r = int(255.0 * jsonStroke.getJSONArray("color").getFloat(0))
                        int g = int(255.0 * jsonStroke.getJSONArray("color").getFloat(1))
                        int b = int(255.0 * jsonStroke.getJSONArray("color").getFloat(2))
                        color col = color(r,g,b)
                        
                        ArrayList<PVector> pts = new ArrayList<PVector>()
                        for (int m=0 m<jsonStroke.getJSONArray("points").size() m++) 
                            jsonPoint = jsonStroke.getJSONArray("points").get(m)
                            PVector p = new PVector(jsonPoint.getJSONArray("co").getFloat(0), jsonPoint.getJSONArray("co").getFloat(1), jsonPoint.getJSONArray("co").getFloat(2))
                            pts.append(p)#.mult(globalScale))
                                                
                        LatkStroke st = new LatkStroke(pts, col)
                        st.globalScale = globalScale
                        layers.get(layers.size()-1).frames.get(layers.get(layers.size()-1).frames.size()-1).strokes.append(st)
                                                                
    def write(self, fileName) # args string
        FINAL_LAYER_LIST = [] # string array

        for layer in layers:
            sb = [] # string array
            sbHeader = [] # string array
            sbHeader.append("\t\t\t\t\t\"frames\":[")
            sb.append(String.join("\n", sbHeader.toArray(new String[sbHeader.size()])))

            for frame in layer.frames:
                sbbHeader = [] # string array
                sbbHeader.append("\t\t\t\t\t\t")
                sbbHeader.append("\t\t\t\t\t\t\t\"strokes\":[")
                sb.append(String.join("\n", sbbHeader.toArray(new String[sbbHeader.size()])))
                for stroke in frame.strokes:
                    sbb = [] # string array
                    sbb.append("\t\t\t\t\t\t\t\t")
                    color col = layers.get(layer).frames.get(layers.get(layer).currentFrame).strokes.get(i).col
                    float r = roundVal(red(col) / 255.0, 5)
                    float g = roundVal(green(col) / 255.0, 5)
                    float b = roundVal(blue(col) / 255.0, 5)
                    sbb.append("\t\t\t\t\t\t\t\t\t\"color\":[" + r + ", " + g + ", " + b + "],")

                    if (layers.get(layer).frames.get(layers.get(layer).currentFrame).strokes.get(i).points.size() > 0) 
                            sbb.append("\t\t\t\t\t\t\t\t\t\"points\":[")
                            for (int j = 0 j < layers.get(layer).frames.get(layers.get(layer).currentFrame).strokes.get(i).points.size() j++) 
                                    PVector pt = layers.get(layer).frames.get(layers.get(layer).currentFrame).strokes.get(i).points.get(j)
                                    #pt.mult(1.0/globalScale)
                                    
                                    if (j == layers.get(layer).frames.get(layers.get(layer).currentFrame).strokes.get(i).points.size() - 1) 
                                            sbb.append("\t\t\t\t\t\t\t\t\t\t\"co\":[" + pt.x + ", " + pt.y + ", " + pt.z + "], \"pressure\":1, \"strength\":1}")
                                            sbb.append("\t\t\t\t\t\t\t\t\t]")
                                    else:
                                            sbb.append("\t\t\t\t\t\t\t\t\t\t\"co\":[" + pt.x + ", " + pt.y + ", " + pt.z + "], \"pressure\":1, \"strength\":1},")
                                                                                                            else:
                            sbb.append("\t\t\t\t\t\t\t\t\t\"points\":[]")
                    
                    if (i == layers.get(layer).frames.get(layers.get(layer).currentFrame).strokes.size() - 1) 
                        sbb.append("\t\t\t\t\t\t\t\t}")
                    else:
                        sbb.append("\t\t\t\t\t\t\t\t},")
                    
                    sb.append(String.join("\n", sbb.toArray(new String[sbb.size()])))
                    
                    ArrayList<String> sbFooter = new ArrayList<String>()
                    if (h == layers.get(layer).frames.size() - 1): 
                        sbFooter.append("\t\t\t\t\t\t\t]")
                        sbFooter.append("\t\t\t\t\t\t}")
                    else:
                        sbFooter.append("\t\t\t\t\t\t\t]")
                        sbFooter.append("\t\t\t\t\t\t},")
                    sb.append(String.join("\n", sbFooter.toArray(new String[sbFooter.size()])))
            
            FINAL_LAYER_LIST.append(String.join("\n", sb.toArray(new String[sb.size()])))
        
        s = [] # string
        s.append("")
        s.append("\t\"creator\": \"processing\",")
        s.append("\t\"grease_pencil\":[")
        s.append("\t\t")
        s.append("\t\t\t\"layers\":[")

        for layer in layers:
            s.append("\t\t\t\t")
            if (layers.get(layer).name != null && layers.get(layer).name != ""): 
                s.append("\t\t\t\t\t\"name\": \"" + layers.get(layer).name + "\",")
            else:
                s.append("\t\t\t\t\t\"name\": \"UnityLayer " + (layer + 1) + "\",")
                
                s.append(FINAL_LAYER_LIST.get(layer))

                s.append("\t\t\t\t\t]")
                if (layer < layers.size() - 1): 
                    s.append("\t\t\t\t},")
                else:
                    s.append("\t\t\t\t}")
                                s.append("                        ]") # end layers
        s.append("                }")
        s.append("        ]")
        s.append("}")
        
        fileType = getExtFromFileName(fileName)
        if (fileType == "latk" or fileType == "zip"):
            fileNameNoExt = getFileNameNoExt(fileName)
            imz = InMemoryZip()
            imz.append(fileNameNoExt + ".json", "\n".join(s))
            imz.writetofile(fileName)            
        else:
            with open(fileName, "w") as f:
                f.write("\n".join(s))
                f.closed
                             
    def clean(self, cleanMinPoints = 1, cleanMinLength = 0.1): 
        for layer in layers:
            for frame in layer.frames: 
                for stroke in frame.strokes:
                    # 1. Remove the stroke if it has too few points.
                    if (len(stroke.points) < cleanMinPoints) 
                        frame.strokes.remove(stroke)
                    else:
                        totalLength = 0.0
                        for i in range(1, len(stroke.points)): 
                            p1 = stroke.points[i] # float tuple
                            p2 = stroke.points[i-1] # float tuple
                            # 2. Remove the point if it's a duplicate.
                            if (hitDetect3D(p1, p2, 0.1)) 
                                stroke.points.remove(points[i])
                            else:
                                totalLength += getDistance(p1, p2)
                        # 3. Remove the stroke if its length is too small.
                        if (totalLength < cleanMinLength) 
                            frame.strokes.remove(stroke)
                        else:
                            # 4. Finally, check the number of points again.
                            if (len(stroke.points) < cleanMinPoints) 
                                frame.strokes.remove(stroke)
    
    def getDistance(v1, v2):
        return sqrt( (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)

    def hitDetect3D(p1, p2, hitbox=0.01):
        if (getDistance(p1, p2) <= hitbox):
            return True
        else:
            return False
             
    def roundVal(a, b):
        formatter = "{0:." + str(b) + "f}"
        return formatter.format(a)

    def roundValInt(a):
        formatter = "{0:." + str(0) + "f}"
        return int(formatter.format(a))

    def writeTextFile(name="test.txt", lines=None):
        file = open(name,"w") 
        for line in lines:
            file.write(line) 
        file.close() 

    def readTextFile(name="text.txt"):
        file = open(name, "r") 
        return file.read() 

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkLayer(object):    
    def __init__(self):    
        self.frames = [] # LatkFrame
        self.currentFrame = 0
        self.name = "layer"
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkFrame(object):   
    def __init__(self):    
        self.strokes = [] # LatkStroke
        
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkStroke(object):       
    def __init__(self, ArrayList<PVector> _p, color _c): 
        self.points = [] # Vector
        self.col = (1.0, 1.0, 1.0)
        self.globalScale = 1.0
        self.globalOffset = (0.0, 0.0, 0.0)
        self.init(_p, _c)

    def init(self, _p, _c): # args float tuple, float tuple
        setColor(_c)
        setPoints(_p)
    
    def getColor(self): 
        return self.col
    
    def setColor(self, _c): # float tuple
        self.col = _c
    
    def getPoints(self):         
        return self.points
    
    def setPoints(self, _p): # args float tuple array
        self.points = _p
    
# * * * * * * * * * * * * * * * * * * * * * * * * * *

class InMemoryZip(object):

    def __init__(self):
        # Create the in-memory file-like object for working w/imz
        self.in_memory_zip = BytesIO()
        self.files = []

    def append(self, filename_in_zip, file_contents):
        # Appends a file with name filename_in_zip and contents of
        # file_contents to the in-memory zip.
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
             zfile.create_system = 0         

        return self

    def readFromMemory(self):
        # Returns a string with the contents of the in-memory zip.
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def readFromDisk(self, url):
        zf = zipfile.ZipFile(url, 'r')
        for file in zf.infolist():
            self.files.append(zf.read(file.filename))

    def writetofile(self, filename):
        # Writes the in-memory zip to a file.
        f = open(filename, "wb")
        f.write(self.readFromMemory())
        f.close()

# * * * * * * * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * *

# END
