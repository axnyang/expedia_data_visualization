import re
import random

input_file = open('world_mobile_locations.csv', 'r')
output_file = open('world_mobile_locations_short.csv', 'w')

input_file_header = input_file.readlines()[0]
output_file.write(input_file_header)

with open('world_mobile_locations.csv') as input_file_rand:
    random_lines = random.sample(input_file_rand.readlines(),100000)

for line in random_lines:
	output_file.write(line)


# for lines in range(500001):
# 	line = input_file.readline()
# 	line = line.split("\t")
# 	line = '\t'.join(line)
# 	output_file.write(line)
