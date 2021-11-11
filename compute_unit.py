import csv



def init_csv_write():
	subheader = ['date', 'time', 'usr', 'sys', 'idl', 'wait', 'stl', 'read', 'write', 'read', 'write', 'power est.']
	header = ['System', '', 'Total', 'cpu', 'usage', '', '', 'dsk/total', '', 'io/total', '', 'power est.']

	# open the file in the write mode
	f = open('data_without_unit.csv', 'w')

	# create the csv writer
	writer = csv.writer(f)
	writer.writerow(header)
	writer.writerow(subheader)
	return f, writer

def init_csv_read():
	f = open('data.csv', encoding='UTF8')
	reader = csv.reader(f)
	return f, reader

def main(read, reader, write, writer):
	for line_no, line in enumerate(reader, 1):
		if line_no > 2:
			#8,10,14
			for i in [8,9,12]:
				value = 0
				unit = line.pop(i)
				#print(unit)
				if i != 12:
					#Byte
					if unit == 'p':
						value = pow(10,-12)
					elif unit == 'n': 
						value = pow(10,-9)
					elif unit == 'u': 
						value = pow(10,-6)
					elif unit == 'm': 
						value = pow(10,-3)
					elif unit == 'B': 
						value = 1
					elif unit == 'k': 
						value = pow(10,3)
					elif unit == 'M': 
						value = pow(10,6)
					elif unit == 'G': 
						value = pow(10,9)
					elif unit == 'T': 
						value = pow(10,12)
					elif unit == '': 
						value = 1
				else:
					#Watt
					if unit == 'pW':
						value = pow(10,-12)
					elif unit == 'nW': 
						value = pow(10,-9)
					elif unit == 'uW': 
						value = pow(10,-6)
					elif unit == 'mW': 
						value = pow(10,-3)
					elif unit == 'W': 
						value = 1
					elif unit == 'kW': 
						value = pow(10,3)
					elif unit == 'MW': 
						value = pow(10,6)
					elif unit == 'GW': 
						value = pow(10,9)
					elif unit == 'TW': 
						value = pow(10,12)
				line[i-1] = float(line[i-1]) * value
			writer.writerow(line)


if __name__ == "__main__":
    write, writer = init_csv_write()
    read, reader = init_csv_read()
    main(read, reader, write, writer)
    write.close()
    read.close()

