import subprocess
import shlex
import csv
import pexpect
import re

def init_csv():
	subheader = ['date', 'time', 'usr', 'sys', 'idl', 'wait', 'stl', 'read', '', 'write', '', 'read', 'write', 'power est.']
	header = ['System', '', 'Total', 'cpu', 'usage', '', '', 'dsk/total',  '','','', 'io/total', '', 'power est.']

	# open the file in the write mode
	f = open('data.csv', 'w')

	# create the csv writer
	writer = csv.writer(f)

	# write a row to the csv file
	#writer.writerow([header[0] + header[1]] + [header[2] + ' ' + header[3] + ' ' + header[4] + header[5] + header[6]] + [header[7] + header[8]] + [header[9] + header[10]] + header[11:])
	writer.writerow(header)
	writer.writerow(subheader)
	return f, writer

def init_powertop():
	child = pexpect.spawnu('sudo powertop')
	child.expect('password')
	child.sendline('P@ssw0rd')
	child.expect('PowerTOP')
	child.send('s')
	child.expect('PowerTOP')
	child.expect('currently')
	child.sendline('1')
	child.send('\t\t\t')
	return child

def init_dstat():
	# system time, total-cpu-usage, dsk/total, io/total
	command = "dstat -tcdr" 
	process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
	return process

def power_est(powertop):
	status = powertop.expect(r'estimated at (.*?)\s+(.*?)\s')
	if status == 0:
		#print(powertop.match.groups())
		return powertop.match.groups()
	else:
		print("error")
		return ["error","error"]

def main(writer, dstat, powertop):
    index = 1
	temp = re.compile("([0-9]+)([a-zA-Z]+)")
	while True:
		row = []
		dstat_output = dstat.stdout.readline()
		if dstat_output == '' and dstat.poll() is not None:
			break
		if dstat_output:
			if "system" not in dstat_output.strip().decode("utf-8") and "time" not in dstat_output.strip().decode("utf-8"):
				dstat_output_string = dstat_output.strip().decode("utf-8")
				result = [x.strip() for x in dstat_output_string.split('|')]
				count = 0
				for r in result:
					for x in r.split(' '):
						if x != '':
							x = x.strip()
							if x.isdigit():
								row.append(x)
							elif "-" in x or ":" in x or x.replace('.', '', 1).isdigit():
								row.append(x)
							else:
								count = 0
								res1, res2 = temp.match(x).groups()
								row.append(res1)
								row.append(res2)
							if count == 7 or count == 8:
								row.append('')
							count = count + 1
				powertop_result = power_est(powertop)
				for x in powertop_result:
					if x != 'error':
						row.append(x.strip())
				writer.writerow(row)
                print(index, " : ", row)
                index = index + 1


if __name__ == "__main__":
    f, writer = init_csv()
    powertop = init_powertop()
    dstat = init_dstat()
    main(writer, dstat, powertop)
    dstat.poll()
    f.close()
