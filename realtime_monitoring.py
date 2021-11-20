import subprocess
import shlex
import csv
import pexpect
from multiprocessing import Process
from datetime import datetime
import re
import os

def init_csv_dstat():
	subheader = ['date', 'time', 'cpu.usr', 'cpu.sys', 'cpu.idl', 'cpu.wait', 'cpu.stl', 'memory.used', 'memory.free', 'memory.buff', 'memory.cach', 'dsk/total.read', 'dsk/total.write', 'io/total.read', 'io/total.write']

	# open the file in the write mode
	file = open('dstat/monitor_dstat_data.csv', 'w')

	# create the csv writer
	writer = csv.writer(file)
	#writer.writerow(header)
	writer.writerow(subheader)
	return file, writer

def init_csv_powertop():
	subheader = ['time', 'power est.']
	#header = ['System', '', 'power est.']

	# open the file in the write mode
	file = open('powertop/monitor_powertop_data.csv', 'w')

	# create the csv writer
	writer = csv.writer(file)
	#writer.writerow(header)
	writer.writerow(subheader)
	return file, writer

def init_powertop():
	child = pexpect.spawnu('sudo powertop')
	child.expect('password')
	child.sendline('db1234')
	child.expect('PowerTOP')
	child.send('s')
	child.expect('PowerTOP')
	child.expect('currently')
	child.sendline('1')
	child.send('\t\t\t')
	return child

def init_dstat():
	# system time, total-cpu-usage, dsk/total, io/total
	command = "dstat -tcmdr" 
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

def compute_unit(res,unit):
	value = 0
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
	res = float(res) * value
	return res

def powertop():
	f, writer = init_csv_powertop()
	powertop = init_powertop()
	print('Process id:', os.getpid(), ' === Start PowerTOP ===')
	index = 1
	try:
		while True:
			row = []
			# datetime object containing current date and time
			now = datetime.now()
			# dd/mm/YY H:M:S
			dt_string = now.strftime("%H:%M:%S")
			row.append(dt_string.strip())
			#power est.
			res1, res2 = power_est(powertop)
			if res1 != 'error' and res2 != 'error':
				res = compute_unit(res1,res2)
				row.append(res)
			writer.writerow(row)
			print(index, " : ", row)
			index = index + 1
	except KeyboardInterrupt:
		print('Process id:', os.getpid(), ' === Stop PowerTOP ===')
		f.close()

def dstat():
	f, writer = init_csv_dstat()
	dstat = init_dstat()
	print('Process id:', os.getpid(), ' === Start dstat ===')
	index = 1
	temp = re.compile("([0-9]+)([a-zA-Z]+)")
	try:
		while True:
			row = []
			dstat_output = dstat.stdout.readline()
			if dstat_output == '' and dstat.poll() is not None:
				break
			if dstat_output:
				if "system" not in dstat_output.strip().decode("utf-8") and "time" not in dstat_output.strip().decode("utf-8"):
					dstat_output_string = dstat_output.strip().decode("utf-8")
					result = [x.strip() for x in dstat_output_string.split('|')]
					for r in result:
						for x in r.split(' '):
							if x == 'missed':
								break
							if x != '':
								x = x.strip()
								if x.isdigit():
									row.append(x)
								elif "-" in x or ":" in x or x.replace('.', '', 1).isdigit():
									row.append(x)
								else:
									res1, res2 = temp.match(x).groups()
									res = compute_unit(res1,res2)
									row.append(res)
					writer.writerow(row)
					print(index, " : ", row)
					index = index + 1
	except KeyboardInterrupt:
		print('Process id:', os.getpid(), ' === Stop dstat ===')
		dstat.poll()
		f.close()


if __name__ == "__main__":
    try:
        p_pt = Process(target=powertop)
        p_d = Process(target=dstat)
        p_pt.start()
        p_d.start()
        p_pt.join()
        p_d.join()
    except KeyboardInterrupt:
        print("-----------------------------------------")
        process = subprocess.Popen(shlex.split('make merge'), stdout=subprocess.PIPE)
        print("the output is in the directory named 'output'")