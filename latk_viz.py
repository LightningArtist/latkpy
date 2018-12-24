import sys
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

from latk import *
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

class Renderer(object):
	def __init__(self, _width, _height):
		self.width = _width
		self.height = _height
		self.image = self.createImage(self.width, self.height)
		self.draw = self.createDraw(self.image)

	def createImage(self, _width, _height):
	    return Image.new("RGB", (_width, _height))

	def createDraw(self, _image):
	    return ImageDraw.Draw(_image)

	def render(self, _latk):
	    for layer in _latk.layers:
	        for frame in layer.frames:
	            for stroke in frame.strokes:
	                r = int(stroke.col[0] * 255)
	                g = int(stroke.col[1] * 255)
	                b = int(stroke.col[2] * 255)
	                col = (r,g,b)

	                points = []
	                for point in stroke.points:
	                    x = int(self.width/2) + int(point.co[2] * self.width/2)
	                    y = int(self.height/2) - int(point.co[1] * self.height/2)
	                    points.append((x,y))
	                if (len(points) > 1):
	                    self.draw.polygon(points, outline=col)
	    self.image.show()

def main():
    data = Latk(inputDir)

    data.write(outputDir)

    Renderer(1024, 1024).render(data) 

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
