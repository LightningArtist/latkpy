'''
The Lightning Artist Toolkit was developed with support from:
   Canada Council on the Arts
   Eyebeam Art + Technology Center
   Ontario Arts Council
   Toronto Arts Council
   
Copyright (c) 2020 Nick Fox-Gieg
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
import math
from math import sqrt
import numpy as np
from numpy import float32
from numpy import isnan
import zipfile
import io
from io import BytesIO
import os
import json
import uuid
import struct
import contextlib
from collections import defaultdict
from random import uniform
from functools import partial
import sys

from latkpy.main import Latk
from latkpy.main import LatkLayer
from latkpy.main import LatkFrame
from latkpy.main import LatkStroke
from latkpy.main import LatkPoint

from latkpy.tilt import STROKE_EXTENSION_BITS
from latkpy.tilt import STROKE_EXTENSION_BY_NAME
from latkpy.tilt import CONTROLPOINT_EXTENSION_BITS
from latkpy.tilt import memoized_property
from latkpy.tilt import binfile
from latkpy.tilt import BadTilt
from latkpy.tilt import BadMetadata
from latkpy.tilt import MissingKey
from latkpy.tilt import validate_metadata
from latkpy.tilt import Tilt
from latkpy.tilt import _make_ext_reader
from latkpy.tilt import _make_stroke_ext_reader
from latkpy.tilt import _make_cp_ext_reader
from latkpy.tilt import Sketch
from latkpy.tilt import Stroke
from latkpy.tilt import ControlPoint
from latkpy.tilt import tiltBrushJson_Grouper
from latkpy.tilt import tiltBrushJson_DecodeData

from latkpy.kmeans import kdist
from latkpy.kmeans import KMeans
from latkpy.kmeans import KCentroid
from latkpy.kmeans import KParticle
from latkpy.kmeans import KCluster

from latkpy.rdp import pldist
from latkpy.rdp import rdp_rec
from latkpy.rdp import _rdp_iter
from latkpy.rdp import rdp_iter
from latkpy.rdp import rdp

from latkpy.zip import InMemoryZip