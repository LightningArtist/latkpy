from latk import *

def main():
    data = Latk("./example/latk_logo.latk")

    #data.draw() 
    data.write("test.latk")
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
