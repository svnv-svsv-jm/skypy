import os, sys


if sys.argv[1].endswith("json"):
    os.system("flatc -b ./" + sys.argv[2] + ".fbs " + sys.argv[1])
else:
    os.system(f'flatc --raw-binary --defaults-json --strict-json -o . -t {sys.argv[2]}.fbs -- {sys.argv[1]}')
