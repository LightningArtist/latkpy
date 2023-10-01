import sys

sys.path.insert(1, "../")

from latk import *
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

def main():
    data = Latk(inputDir)
    data.clean()
    data.write(outputDir)

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
