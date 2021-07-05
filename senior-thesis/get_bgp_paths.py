

bgpscanner_file = open("path_data.txt", "r")
paths = open("paths.txt", "w")
i = 0
for line in bgpscanner_file:
    path = line.split('|')[2]
    paths.write(path)
    paths.write('\n')

bgpscanner_file.close()
paths.close()

