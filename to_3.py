import sys

read_obj = open(sys.argv[1], 'r')
line_to_read = 1
while line_to_read:
    line_to_read  = read_obj.readline()
    line = line_to_read
    line = line.replace('getiterator', 'iter')
    sys.stdout.write(line)
