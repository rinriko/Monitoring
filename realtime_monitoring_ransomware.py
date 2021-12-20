import subprocess
import shlex
import csv
import pexpect
from multiprocessing import Process, Manager
from datetime import datetime
import re
import os
import pandas as pd
import time

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
	subheader = ['date', 'time', 'power est.']
	#header = ['System', '', 'power est.']

	# open the file in the write mode
	file = open('powertop/monitor_powertop_data.csv', 'w')

	# create the csv writer
	writer = csv.writer(file)
	#writer.writerow(header)
	writer.writerow(subheader)
	return file, writer

def init_csv_ransomware():
	subheader = ['date', 'time', 'is_attacked']
	#header = ['System', '', 'is_attacked']

	# open the file in the write mode
	file = open('ransomware/monitor_ransomware_data.csv', 'w')

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

def init_ransomware():
	# system time, total-cpu-usage, dsk/total, io/total
	command = "python3 ../ransomware/payload_fast.py" 
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

def ransomware(data_ransomware):
	index = 1
	print('Process id:', os.getpid(), ' === Start Ransomware ===')
	f, writer = init_csv_ransomware()
	try:
		row = []
		# datetime object containing current date and time
		now = datetime.now()
		# dd/mm/YY H:M:S
		dt_string = now.strftime("%d-%m %H:%M:%S")
		for x in dt_string.split(' '):
			row.append(x.strip())
		row.append('True')
		writer.writerow(row)
		data_ransomware.append(row)
		print(index, " : ", row)
		index = index + 1
		row = []
		# ==================================================================================================
		ran = init_ransomware()
		while True:
		ran_output = ran.stdout.readline()
			if ran_output == '' and ran.poll() is not None:
				break
		ran.poll()
		# ==================================================================================================
		# datetime object containing current date and time
		now = datetime.now()
		# dd/mm/YY H:M:S
		dt_string = now.strftime("%d-%m %H:%M:%S")
		for x in dt_string.split(' '):
			row.append(x.strip())
		row.append('True')
		writer.writerow(row)
		data_ransomware.append(row)
		print(index, " : ", row)
		print('Process id:', os.getpid(), ' === Stop Ransomware ===')
		
		f.close()
	except KeyboardInterrupt:
		print('Process id:', os.getpid(), ' === Stop Ransomware ===')
		ran.poll()
		f.close()

def powertop(data_powertop):
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
			dt_string = now.strftime("%d-%m %H:%M:%S")
			for x in dt_string.split(' '):
				row.append(x.strip())
			#power est.
			res1, res2 = power_est(powertop)
			if res1 != 'error' and res2 != 'error':
				res = compute_unit(res1,res2)
				row.append(res)
			writer.writerow(row)
			data_powertop.append(row)
			print(index, " : ", row)
			index = index + 1
	except KeyboardInterrupt:
		print('Process id:', os.getpid(), ' === Stop PowerTOP ===')
		f.close()

def dstat(data_dstat):
	f, writer = init_csv_dstat()
	dstat = init_dstat()
	print('Process id:', os.getpid(), ' === Start dstat ===')
	index = 1
	temp = re.compile("([0-9]*[.]{0,1}[0-9]*)([a-zA-Z]+)")
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
					data_dstat.append(row)
					print(index, " : ", row)
					index = index + 1
	except KeyboardInterrupt:
		print('Process id:', os.getpid(), ' === Stop dstat ===')
		dstat.poll()
		f.close()

def merge_data(data_dstat, data_powertop, data_ransomware):
	# reading csv files
	#data1 = pd.read_csv('dstat/monitor_dstat_data.csv')
	#data2 = pd.read_csv('powertop/monitor_powertop_data.csv')
	df_dstat = pd.DataFrame(data_dstat, columns=['date', 'time', 'cpu.usr', 'cpu.sys', 'cpu.idl', 'cpu.wait', 'cpu.stl', 'memory.used', 'memory.free', 'memory.buff', 'memory.cach', 'dsk/total.read', 'dsk/total.write', 'io/total.read', 'io/total.write'])
	df_powertop = pd.DataFrame(data_powertop, columns=['date', 'time', 'power est.'])
	df_ransomware = pd.DataFrame(data_ransomware, columns=['date', 'time', 'is_attacked'])
	# using merge function by setting how='left'
	output_dstat_n_powertop = pd.merge(df_dstat, df_powertop, on=['date', 'time'], how='left').fillna('')
	output = pd.merge(output_dstat_n_powertop, df_ransomware, on=['date', 'time'], how='left').fillna('')
	last = output['is_attacked'].last_valid_index()
	output['is_attacked'].loc[:last] = output['is_attacked'].loc[:last].ffill()
	# displaying result
	print(output)
	# save result
	output.to_csv('output/monitoring_ransomware.csv', index=False)

data_dstat = []
data_powertop = []
data_ransomware = []

if __name__ == "__main__":
    with Manager() as manager:
        try:
        	data_dstat = manager.list()
        	data_powertop = manager.list()
        	data_ransomware = manager.list()
        	p_dstat = Process(target=dstat, args=(data_dstat,))
        	p_powertop = Process(target=powertop, args=(data_powertop,))
        	p_ransomware = Process(target=ransomware, args=(data_ransomware,))
        	p_dstat.start()
        	p_powertop.start()
        	time.sleep(30)
        	p_ransomware.start()
        	p_ransomware.join()
        	p_dstat.join()
        	p_powertop.join()

        except KeyboardInterrupt:
        	while p_powertop.is_alive() and p_dstat.is_alive():
        	    pass
        	print("-----------------------------------------")
        	data_dstat = list(data_dstat)
        	data_powertop = list(data_powertop)
        	data_ransomware = list(data_ransomware)
        	merge_data(data_dstat, data_powertop, data_ransomware)
        	print("the output is in the directory named 'output'")