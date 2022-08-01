import os
import sys
sys.path.insert(0, r"D:\programmiUniversita\PyCharm 2022.1\progetti\best\empirical")
from empirical import CoCoS



if __name__ == '__main__':
    file_list = os.listdir('./prototipi')
    max_prop = 6
    for file in file_list:
      CoCoS("./prototipi/"+file, max_prop, write_to_file=True)