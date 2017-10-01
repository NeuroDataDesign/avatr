
import argparse

parser = argparse.ArgumentParser(description="file name parser")
parser.add_argument('-n', dest = 'name', type = str, help = "file name", required = True)
args = parser.parse_args()
f = open(args.name, 'w')
f.write("hello world")
f.close()
