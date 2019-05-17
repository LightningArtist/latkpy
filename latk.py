'''
The Lightning Artist Toolkit was developed with support from:
   Canada Council on the Arts
   Eyebeam Art + Technology Center
   Ontario Arts Council
   Toronto Arts Council
   
Copyright (c) 2019 Nick Fox-Gieg
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

import json
import zipfile
from io import BytesIO
from math import sqrt
from numpy import float32
from numpy import isnan

# * * * * * * * * * * * * * * * * * * * * * * * * * *

class Latk(object):     
    def __init__(self, filepath=None, init=False, coords=None, color=None): # args string, Latk array, float tuple array, float tuple           
        self.layers = [] # LatkLayer
        self.frame_rate = 12

        if (filepath != None):
            self.read(filepath, True)
        elif (init == True):
            self.layers.append(LatkLayer())
            self.layers[0].frames.append(LatkFrame())
            if (coords != None): # 
                stroke = LatkStroke()
                stroke.setCoords(coords)
                if (color != None):
                    stroke.color = color
                self.layers[0].frames[0].strokes.append(stroke)            

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

    def read(self, filepath, clearExisting=True, yUp=False, useScaleAndOffset=False, globalScale=(1.0, 1.0, 1.0), globalOffset=(0.0, 0.0, 0.0)): # defaults to Blender Z up
        data = None

        if (clearExisting == True):
            self.layers = []
        
        fileType = self.getExtFromFileName(filepath)
        if (fileType == "latk" or fileType == "zip"):
            imz = InMemoryZip()
            imz.readFromDisk(filepath)
            data = json.loads(imz.files[0].decode("utf-8"))        
        else:
            with open(filepath) as data_file:    
                data = json.load(data_file)
                            
        for jsonGp in data["grease_pencil"]:          
            for jsonLayer in jsonGp["layers"]:
                layer = LatkLayer(jsonLayer["name"])
                
                for jsonFrame in jsonLayer["frames"]:
                    frame = LatkFrame()
                    for jsonStroke in jsonFrame["strokes"]:                       
                        color = (1,1,1)
                        try:
                            r = jsonStroke["color"][0]
                            g = jsonStroke["color"][1]
                            b = jsonStroke["color"][2]
                            color = (r,g,b)
                        except:
                            pass
                        
                        points = []
                        for jsonPoint in jsonStroke["points"]:
                            x = float(jsonPoint["co"][0])
                            y = None
                            z = None
                            if (yUp == False):
                                y = float(jsonPoint["co"][2])
                                z = float(jsonPoint["co"][1])  
                            else:
                                y = float(jsonPoint["co"][1])
                                z = float(jsonPoint["co"][2]) 
                            #~
                            if (useScaleAndOffset == True):
                                x = (x * globalScale[0]) + globalOffset[0]
                                y = (y * globalScale[1]) + globalOffset[1]
                                z = (z * globalScale[2]) + globalOffset[2]
                            #~                                                           
                            pressure = 1.0
                            strength = 1.0
                            try:
                                pressure = jsonPoint["pressure"]
                                if (isnan(pressure) == True):
                                    pressure = 1.0
                            except:
                                pass
                            try:
                                strength = jsonPoint["strength"]
                                if (isnan(strength) == True):
                                    strenght = 1.0
                            except:
                                pass
                            points.append(LatkPoint((x,y,z), pressure, strength))
                                                
                        stroke = LatkStroke(points, color)
                        frame.strokes.append(stroke)
                    layer.frames.append(frame)
                self.layers.append(layer)

    def write(self, filepath, yUp=True, useScaleAndOffset=False, zipped=True, globalScale=(1.0, 1.0, 1.0), globalOffset=(0.0, 0.0, 0.0)): # defaults to Unity, Maya Y up
        FINAL_LAYER_LIST = [] # string array

        for layer in self.layers:
            sb = [] # string array
            sbHeader = [] # string array
            sbHeader.append("\t\t\t\t\t\"frames\": [")
            sb.append("\n".join(sbHeader))

            for h, frame in enumerate(layer.frames):
                sbbHeader = [] # string array
                sbbHeader.append("\t\t\t\t\t\t{")
                sbbHeader.append("\t\t\t\t\t\t\t\"strokes\": [")
                sb.append("\n".join(sbbHeader))
                
                for i, stroke in enumerate(frame.strokes):
                    sbb = [] # string array
                    sbb.append("\t\t\t\t\t\t\t\t{")
                    color = stroke.color
                    sbb.append("\t\t\t\t\t\t\t\t\t\"color\": [" + str(float32(color[0])) + ", " + str(float32(color[1])) + ", " + str(float32(color[2])) + "],")

                    if (len(stroke.points) > 0): 
                        sbb.append("\t\t\t\t\t\t\t\t\t\"points\": [")
                        for j, point in enumerate(stroke.points):
                            x = point.co[0]
                            y = None
                            z = None
                            if (yUp == True):
                                y = point.co[2]
                                z = point.co[1]
                            else:
                                y = point.co[1]
                                z = point.co[2]  
                            #~
                            if (useScaleAndOffset == True):
                                x = (x * globalScale[0]) + globalOffset[0]
                                y = (y * globalScale[1]) + globalOffset[1]
                                z = (z * globalScale[2]) + globalOffset[2]
                            #~                                           
                            if (j == len(stroke.points) - 1):
                                sbb.append("\t\t\t\t\t\t\t\t\t\t{\"co\": [" + str(float32(x)) + ", " + str(float32(y)) + ", " + str(float32(z)) + "], \"pressure\":" + str(float32(point.pressure)) + ", \"strength\":" + str(float32(point.strength)) + "}")
                                sbb.append("\t\t\t\t\t\t\t\t\t]")
                            else:
                                sbb.append("\t\t\t\t\t\t\t\t\t\t{\"co\": [" + str(float32(x)) + ", " + str(float32(y)) + ", " + str(float32(z)) + "], \"pressure\":" + str(float32(point.pressure)) + ", \"strength\":" + str(float32(point.strength)) + "},")
                    else:
                        sbb.append("\t\t\t\t\t\t\t\t\t\"points\": []")
                    
                    if (i == len(frame.strokes) - 1):
                        sbb.append("\t\t\t\t\t\t\t\t}")
                    else:
                        sbb.append("\t\t\t\t\t\t\t\t},")
                    
                    sb.append("\n".join(sbb))
                
                sbFooter = []
                if (h == len(layer.frames) - 1): 
                    sbFooter.append("\t\t\t\t\t\t\t]")
                    sbFooter.append("\t\t\t\t\t\t}")
                else:
                    sbFooter.append("\t\t\t\t\t\t\t]")
                    sbFooter.append("\t\t\t\t\t\t},")
                sb.append("\n".join(sbFooter))
            
            FINAL_LAYER_LIST.append("\n".join(sb))
        
        s = [] # string
        s.append("{")
        s.append("\t\"creator\": \"latk.py\",")
        s.append("\t\"grease_pencil\": [")
        s.append("\t\t{")
        s.append("\t\t\t\"layers\": [")

        for i, layer in enumerate(self.layers):
            s.append("\t\t\t\t{")
            if (layer.name != None and layer.name != ""): 
                s.append("\t\t\t\t\t\"name\": \"" + layer.name + "\",")
            else:
                s.append("\t\t\t\t\t\"name\": \"layer" + str(i + 1) + "\",")
                
            s.append(FINAL_LAYER_LIST[i])

            s.append("\t\t\t\t\t]")
            if (i < len(self.layers) - 1): 
                s.append("\t\t\t\t},")
            else:
                s.append("\t\t\t\t}")
                s.append("\t\t\t]") # end layers
        s.append("\t\t}")
        s.append("\t]")
        s.append("}")
        
        fileType = self.getExtFromFileName(filepath)
        if (zipped == True or fileType == "latk" or fileType == "zip"):
            filepathNoExt = self.getFileNameNoExt(filepath)
            imz = InMemoryZip()
            imz.append(filepathNoExt + ".json", "\n".join(s))
            imz.writetofile(filepath)            
        else:
            with open(filepath, "w") as f:
                f.write("\n".join(s))
                f.closed
                
    def clean(self, epsilon=0.01):
        for layer in self.layers:
            for frame in layer.frames:
                for stroke in frame.strokes:
                    coords = []
                    pressures = []
                    strengths = []
                    for point in stroke.points:
                        coords.append(point.co)
                        pressures.append(point.pressure)
                        strengths.append(point.strength)
                    stroke.setCoords(rdp(coords, epsilon=epsilon))
                    for i in range(0, len(stroke.points)):
                        index = self.remapInt(i, 0, len(stroke.points), 0, len(pressures))
                        stroke.points[i].pressure = pressures[index]
                        stroke.points[i].strength = strengths[index]

    def filter(self, cleanMinPoints = 2, cleanMinLength = 0.1):
        if (cleanMinPoints < 2):
            cleanMinPoints = 2 
        for layer in self.layers:
            for frame in layer.frames: 
                for stroke in frame.strokes:
                    # 1. Remove the stroke if it has too few points.
                    if (len(stroke.points) < cleanMinPoints): 
                        try:
                            frame.strokes.remove(stroke)
                        except:
                            pass
                    else:
                        totalLength = 0.0
                        for i in range(1, len(stroke.points)): 
                            p1 = stroke.points[i] # float tuple
                            p2 = stroke.points[i-1] # float tuple
                            # 2. Remove the point if it's a duplicate.
                            if (self.hitDetect3D(p1.co, p2.co, 0.1)): 
                                try:
                                    stroke.points.remove(stroke)
                                except:
                                    pass
                            else:
                                totalLength += self.getDistance(p1.co, p2.co)
                        # 3. Remove the stroke if its length is too small.
                        if (totalLength < cleanMinLength): 
                            try:
                                frame.strokes.remove(stroke)
                            except:
                                pass
                        else:
                            # 4. Finally, check the number of points again.
                            if (len(stroke.points) < cleanMinPoints): 
                                try:
                                    frame.strokes.remove(stroke)
                                except:
                                    pass

    def smoothStroke(self, stroke):
        points = stroke.points
        #~
        weight = 18
        scale = 1.0 / (weight + 2)
        lower = 0
        upper = 0
        center = 0
        #~
        for i in range(1, len(points) - 2):
            lower = points[i-1].co
            center = points[i].co
            upper = points[i+1].co
            #~
            x = (lower[0] + weight * center[0] + upper[0]) * scale
            y = (lower[1] + weight * center[1] + upper[1]) * scale
            z = (lower[2] + weight * center[2] + upper[2]) * scale
            stroke.points[i].co = (x, y, z) #center = (x, y, z)
        
    def splitStroke(self, stroke): 
        points = stroke.points
        #~
        for i in range(1, len(points), 2):
            center = (points[i].co[0], points[i].co[1], points[i].co[2])
            lower = (points[i-1].co[0], points[i-1].co[1], points[i-1].co[2])
            x = (center[0] + lower[0]) / 2
            y = (center[1] + lower[1]) / 2
            z = (center[2] + lower[2]) / 2
            p = (x, y, z)
            #~
            pressure = (points[i-1].pressure + points[i].pressure) / 2
            strength = (points[i-1].strength + points[i].strength) / 2
            #~
            pt = LatkPoint(p, pressure, strength)
            stroke.points.insert(i, pt)

    def reduceStroke(self, stroke):
        for i in range(0, len(stroke.points), 2):
            stroke.points.remove(stroke.points[i])

    def refine(self, splitReps=2, smoothReps=10, reduceReps=0, doClean=True):
        if (doClean==True):
            self.clean()
        if (smoothReps < splitReps):
            smoothReps = splitReps
        for layer in self.layers:
            for frame in layer.frames: 
                for stroke in frame.strokes:   
                    points = stroke.points
                    #~
                    for i in range(0, splitReps):
                        self.splitStroke(stroke)  
                        self.smoothStroke(stroke)  
                    #~
                    for i in range(0, smoothReps - splitReps):
                        self.smoothStroke(stroke)
                    #~
                    for i in range(0, reduceReps):
                        self.reduceStroke(stroke)    

    def setStroke(self, stroke):
        lastLayer = self.layers[len(self.layers)-1]
        lastFrame = lastLayer.frames[len(lastLayer.frames)-1]
        lastFrame.strokes.append(stroke)

    def setPoints(self, points, color=(1.0,1.0,1.0)):
        lastLayer = self.layers[len(self.layers)-1]
        lastFrame = lastLayer.frames[len(lastLayer.frames)-1]
        stroke = LatkStroke()
        stroke.points = points
        stroke.color = color
        lastFrame.strokes.append(stroke)
    
    def setCoords(self, coords, color=(1.0,1.0,1.0)):
        lastLayer = self.layers[len(self.layers)-1]
        lastFrame = lastLayer.frames[len(lastLayer.frames)-1]
        stroke = LatkStroke()
        stroke.setCoords(coords)
        stroke.color = color
        lastFrame.strokes.append(stroke)

    def getDistance(self, v1, v2):
        return sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)

    def hitDetect3D(self, p1, p2, hitbox=0.01):
        if (self.getDistance(p1, p2) <= hitbox):
            return True
        else:
            return False
             
    def roundVal(self, a, b):
        formatter = "{0:." + str(b) + "f}"
        return formatter.format(a)

    def roundValInt(self, a):
        formatter = "{0:." + str(0) + "f}"
        return int(formatter.format(a))

    def remap(self, value, min1, max1, min2, max2):
        range1 = max1 - min1
        range2 = max2 - min2
        valueScaled = float(value - min1) / float(range1)
        return min2 + (valueScaled * range2)

    def remapInt(self, value, min1, max1, min2, max2):
        return int(self.remap(value, min1, max1, min2, max2))

    def writeTextFile(self, name="test.txt", lines=None):
        file = open(name,"w") 
        for line in lines:
            file.write(line) 
        file.close() 

    def readTextFile(self, name="text.txt"):
        file = open(name, "r") 
        return file.read() 

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkLayer(object):    
    def __init__(self, name="layer"): 
        self.frames = [] # LatkFrame
        self.name = name
        self.parent = None

    def getInfo(self):
        return self.name.split(".")[0]
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkFrame(object):   
    def __init__(self, frame_number=0): 
        self.strokes = [] # LatkStroke
        self.frame_number = frame_number
        self.parent_location = (0.0,0.0,0.0)
        
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkStroke(object):       
    def __init__(self, points=None, color=(1.0,1.0,1.0)): # args float tuple array, float tuple 
        self.points = []
        if (points != None):
            self.points = points
        self.color = color
        self.alpha = 1.0
        self.fill_color = color
        self.fill_alpha = 0.0

    def setCoords(self, coords):
        self.points = []
        for coord in coords:
            self.points.append(LatkPoint(coord))

    def getCoords(self):
        returns = []
        for point in self.points:
            returns.append(point.co)
        return returns

    def getPressures(self):
        returns = []
        for point in self.points:
            returns.append(point.pressure)
        return returns

    def getStrengths(self):
        returns = []
        for point in self.points:
            returns.append(point.strength)
        return returns

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class LatkPoint(object):
    def __init__(self, co, pressure=1.0, strength=1.0): # args float tuple, float, float
        self.co = co
        self.pressure = pressure
        self.strength = strength
    
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
rdp
~~~

Python implementation of the Ramer-Douglas-Peucker algorithm.

:copyright: 2014-2016 Fabian Hirschmann <fabian@hirschmann.email>
:license: MIT, see LICENSE.txt for more details.

Copyright (c) 2014 Fabian Hirschmann <fabian@hirschmann.email>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from math import sqrt
from functools import partial
import numpy as np
import sys

if sys.version_info[0] >= 3:
    xrange = range


def pldist(point, start, end):
    """
    Calculates the distance from ``point`` to the line given
    by the points ``start`` and ``end``.

    :param point: a point
    :type point: numpy array
    :param start: a point of the line
    :type start: numpy array
    :param end: another point of the line
    :type end: numpy array
    """
    if np.all(np.equal(start, end)):
        return np.linalg.norm(point - start)

    return np.divide(
            np.abs(np.linalg.norm(np.cross(end - start, start - point))),
            np.linalg.norm(end - start))


def rdp_rec(M, epsilon, dist=pldist):
    """
    Simplifies a given array of points.

    Recursive version.

    :param M: an array
    :type M: numpy array
    :param epsilon: epsilon in the rdp algorithm
    :type epsilon: float
    :param dist: distance function
    :type dist: function with signature ``f(point, start, end)`` -- see :func:`rdp.pldist`
    """
    dmax = 0.0
    index = -1

    for i in xrange(1, M.shape[0]):
        d = dist(M[i], M[0], M[-1])

        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        r1 = rdp_rec(M[:index + 1], epsilon, dist)
        r2 = rdp_rec(M[index:], epsilon, dist)

        return np.vstack((r1[:-1], r2))
    else:
        return np.vstack((M[0], M[-1]))


def _rdp_iter(M, start_index, last_index, epsilon, dist=pldist):
    stk = []
    stk.append([start_index, last_index])
    global_start_index = start_index
    indices = np.ones(last_index - start_index + 1, dtype=bool)

    while stk:
        start_index, last_index = stk.pop()

        dmax = 0.0
        index = start_index

        for i in xrange(index + 1, last_index):
            if indices[i - global_start_index]:
                d = dist(M[i], M[start_index], M[last_index])
                if d > dmax:
                    index = i
                    dmax = d

        if dmax > epsilon:
            stk.append([start_index, index])
            stk.append([index, last_index])
        else:
            for i in xrange(start_index + 1, last_index):
                indices[i - global_start_index] = False

    return indices


def rdp_iter(M, epsilon, dist=pldist, return_mask=False):
    """
    Simplifies a given array of points.

    Iterative version.

    :param M: an array
    :type M: numpy array
    :param epsilon: epsilon in the rdp algorithm
    :type epsilon: float
    :param dist: distance function
    :type dist: function with signature ``f(point, start, end)`` -- see :func:`rdp.pldist`
    :param return_mask: return the mask of points to keep instead
    :type return_mask: bool
    """
    mask = _rdp_iter(M, 0, len(M) - 1, epsilon, dist)

    if return_mask:
        return mask

    return M[mask]


def rdp(M, epsilon=0, dist=pldist, algo="iter", return_mask=False):
    """
    Simplifies a given array of points using the Ramer-Douglas-Peucker
    algorithm.

    Example:

    >>> from rdp import rdp
    >>> rdp([[1, 1], [2, 2], [3, 3], [4, 4]])
    [[1, 1], [4, 4]]

    This is a convenience wrapper around both :func:`rdp.rdp_iter` 
    and :func:`rdp.rdp_rec` that detects if the input is a numpy array
    in order to adapt the output accordingly. This means that
    when it is called using a Python list as argument, a Python
    list is returned, and in case of an invocation using a numpy
    array, a NumPy array is returned.

    The parameter ``return_mask=True`` can be used in conjunction
    with ``algo="iter"`` to return only the mask of points to keep. Example:

    >>> from rdp import rdp
    >>> import numpy as np
    >>> arr = np.array([1, 1, 2, 2, 3, 3, 4, 4]).reshape(4, 2)
    >>> arr
    array([[1, 1],
           [2, 2],
           [3, 3],
           [4, 4]])
    >>> mask = rdp(arr, algo="iter", return_mask=True)
    >>> mask
    array([ True, False, False,  True], dtype=bool)
    >>> arr[mask]
    array([[1, 1],
           [4, 4]])

    :param M: a series of points
    :type M: numpy array with shape ``(n,d)`` where ``n`` is the number of points and ``d`` their dimension
    :param epsilon: epsilon in the rdp algorithm
    :type epsilon: float
    :param dist: distance function
    :type dist: function with signature ``f(point, start, end)`` -- see :func:`rdp.pldist`
    :param algo: either ``iter`` for an iterative algorithm or ``rec`` for a recursive algorithm
    :type algo: string
    :param return_mask: return mask instead of simplified array
    :type return_mask: bool
    """

    if algo == "iter":
        algo = partial(rdp_iter, return_mask=return_mask)
    elif algo == "rec":
        if return_mask:
            raise NotImplementedError("return_mask=True not supported with algo=\"rec\"")
        algo = rdp_rec
        
    if "numpy" in str(type(M)):
        return algo(M, epsilon, dist)

    return algo(np.array(M), epsilon, dist).tolist()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# * * * * * * * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * *

