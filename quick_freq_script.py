import numpy as np
import os
from generate_freq_table import create_freq_table


file_name ="quick_freq_desc.txt"
my_file = open(file_name)
desc = my_file.read()

freq = create_freq_table(desc)
print(freq)