import subprocess
import shlex
import csv  
subheader = ['date', 'time', 'usr', 'sys', 'idl', 'wai', 'stl', 'read',  'writ', 'read', 'writ', 'power est.']
header = ['System', '', 'Total', 'cpu', 'usage', '', '', 'dsk/total',  '', 'io/total', '', 'power est.']
import csv

# open the file in the write mode
f = open('test.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
#writer.writerow([header[0] + header[1]] + [header[2] + ' ' + header[3] + ' ' + header[4] + header[5] + header[6]] + [header[7] + header[8]] + [header[9] + header[10]] + header[11:])
writer.writerow(header)
writer.writerow(subheader)



# system time, total-cpu-usage, dsk/total, io/total
command = "sudo dstat -tcdr" 
process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
while True:
	row = []
	output = process.stdout.readline()
	if output == '' and process.poll() is not None:
		break
	if output:
		if "system" not in output.strip().decode("utf-8") and "time" not in output.strip().decode("utf-8"):
			string = output.strip().decode("utf-8")
			result = [x.strip() for x in string.split('|')]
			for text in result:
				for x in text.split(' '):
					if x != '':
						row.append(x.strip())
			writer.writerow(row)
rc = process.poll()


# close the file
f.close()


# # powertop
# command = "sudo powertop"
run_command(command)