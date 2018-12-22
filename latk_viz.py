from latk import *

def main():
    pass
    '''
    fileName = "test.latk"

    data = Latk(fileName)

    data.draw() 
    data.write()
    '''
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
